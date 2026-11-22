"""Supplementary pages for publications: papers/<citekey>/ (called by build_publications.py).

Each paper listed on the publications page gets a directory papers/<citekey>/
holding three files:

  _metadata.yml  generated: page title and authors (Quarto applies it to the directory).
  _info.qmd      generated: venue, links, image, abstract, reproducibility repository.
  index.qmd      written only if missing; it includes _info.qmd.  Add supplementary
                 material (animations, interactive figures) here by hand.

The generated files are rewritten on every build; index.qmd never is.

Abstracts come from, in order of preference:
  1. the .bib entry's `abstract` field;
  2. arXiv, by the entry's `arxivid`, or else by a search for the exact title
     (accepted only if the normalized titles match and Ketcheson is an author);
  3. Crossref (the publisher's metadata), by the entry's DOI.
(publication_tags.yml `abstract_overrides` take precedence over all of these.)
Results are cached in paper_abstracts.yml so later builds don't query arXiv or
Crossref.  A cached entry with `arxiv: null` means the title search found
nothing, and one with `crossref_result: no abstract` that Crossref had none;
delete the entry to look again.

Reproducibility repositories come from the Jekyll site's paperlinks.txt
("Reproducibility repository" entries) and the `repos` section of
publication_tags.yml.
"""
import codecs
import datetime
import html
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import latexcodec  # noqa: F401  (registers the "ulatex" codec)
import yaml

HERE = Path(__file__).resolve().parent
PAGES_DIR = HERE / "papers"
ABSTRACT_CACHE = HERE / "paper_abstracts.yml"
ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = {"a": "http://www.w3.org/2005/Atom"}
CROSSREF_API = "https://api.crossref.org/works/"
ARXIV_DELAY = 3.0   # seconds between requests, as arXiv's API terms ask
# The order in which the generator writes the sections of the publication list.
SECTION_TYPES = ["unpublished", "article", "book", "inproceedings", "techreport", "phdthesis"]

INDEX_TEMPLATE = """\
{{{{< include _info.qmd >}}}}

<!--
Supplementary material for this paper goes below (animations, interactive
figures, ...).  The title, authors, abstract and links above come from
build_publications.py; edit {key} in the .bib file or publication_tags.yml
to change them.
-->
"""


# ---------------------------------------------------------------- page order

def listed_keys(gen, pubs) -> list:
    """Citation keys in the order the generator writes the publication list."""
    return [p["pid"] for t in SECTION_TYPES
            for p in gen.sort_by_year([p for p in pubs if p["reference_type"] == t])]


ENTRY_RE = re.compile(r'(<div class="pub filterable[^"]*">\n)(.*?)(\n</div>\n)', re.S)
VENUE_RE = re.compile(r'<span class="pub-authors">.*?</span>,\n(.*?)(?:<br>\n)?'
                      r'(?=<span class="pub-links">|<div style="clear:both">)', re.S)
LINKS_RE = re.compile(r'<span class="pub-links">(.*?)</span>', re.S)


def norm(s: str) -> str:
    return " ".join(html.unescape(s).replace("{", "").replace("}", "").split())


def split_entries(body: str, keys: list, pubs_by_key: dict) -> list:
    """Match each entry of the cleaned list HTML to its citation key; return (key, html) pairs."""
    entries = ENTRY_RE.findall(body)
    if len(entries) != len(keys):
        raise ValueError(f"{len(entries)} entries in the list but {len(keys)} listed keys")
    out = []
    for key, (_, entry, _) in zip(keys, entries):
        title = re.search(r'<span class="pub-title">(.*?)</span>', entry, re.S)
        if not title or norm(title.group(1)) != norm(pubs_by_key[key]["title"]):
            raise ValueError(f"List entry does not match {key} ({pubs_by_key[key]['title']!r}):\n{entry}")
        out.append((key, entry))
    return out


ANCHOR_RE = re.compile(r'<a href="([^"]+)">(.*?)</a>', re.S)
TITLE_LINK_RE = re.compile(r'(?:<a href="([^"]+)">)?<span class="pub-title">(.*?)</span><br>\n(?:</a>\n)?', re.S)
IMG_RE = re.compile(r'(?:<a href="[^"]+">)?(<img [^>]*/>)(?:</a>)?')
MORE_INFO = "More information"
REPO_LABEL = "Reproducibility repository"


def url_key(url: str) -> str:
    """Normalized URL, so that e.g. dx.doi.org/X and https://doi.org/X compare equal."""
    u = re.sub(r"^https?://(www\.)?", "", url.strip().lower()).rstrip("/")
    return re.sub(r"^(dx\.doi\.org|doi\.org|doi\.wiley\.com)/", "doi:", u)


def parse_links(span: str, where: str) -> list:
    """The (url, label) pairs of a links line; error if it holds anything but " | "-separated links."""
    links = ANCHOR_RE.findall(span)
    if " | ".join(f'<a href="{u}">{t}</a>' for u, t in links) != span.strip():
        raise ValueError(f"Unexpected links line for {where}: {span!r}")
    return links


def format_links(links: list) -> str:
    return " | ".join(f'<a href="{u}">{t}</a>' for u, t in links)


def link_entries(body: str, keys: list, pubs_by_key: dict, repos: dict, hidden: dict) -> str:
    """Point each entry's title and image at its supplementary page and fill in its links line.

    The links line gets, in order: "More information" (the supplementary page);
    the title's former target, as "Paper" (or "Book"), unless another link already
    goes there; the generator's links, minus those in `hidden` (key -> URL); and
    the reproducibility repository from `repos` (relabeled if already linked).
    """
    it = iter(keys)

    def entry(m):
        key = next(it)
        page = f"/papers/{key}/"
        html_ = m.group(2)

        title = TITLE_LINK_RE.search(html_)
        if not title:
            raise ValueError(f"No title found for {key}:\n{html_}")
        old_target = title.group(1)
        html_ = (html_[:title.start()] + f'<a href="{page}"><span class="pub-title">{title.group(2)}</span></a><br>\n'
                 + html_[title.end():])
        html_, n_img = IMG_RE.subn(rf'<a href="{page}">\1</a>', html_)
        if n_img > 1:
            raise ValueError(f"Several images for {key}")

        span = LINKS_RE.search(html_)
        links = parse_links(span.group(1), key) if span else []
        if key in hidden:
            dead = [x for x in links if url_key(x[0]) == url_key(hidden[key])]
            if not dead:
                raise ValueError(f"{key}: hidden repository {hidden[key]} is not in its links line")
            links = [x for x in links if x not in dead]
        seen = {url_key(u) for u, _ in links}
        if old_target and url_key(old_target) not in seen:
            label = "Book" if pubs_by_key[key]["reference_type"] == "book" else "Paper"
            links.insert(0, (old_target, label))
        if key in repos:
            if url_key(repos[key]) in seen:   # e.g. listed as "Code" in paperlinks.txt
                links = [(u, REPO_LABEL if url_key(u) == url_key(repos[key]) else t) for u, t in links]
            else:
                links.append((repos[key], REPO_LABEL))
        links.insert(0, (page, MORE_INFO))
        line = f'<span class="pub-links">{format_links(links)}</span>'
        if span:
            html_ = html_[:span.start()] + line + html_[span.end():]
        else:
            if html_.count('<div style="clear:both">') != 1:
                raise ValueError(f"Could not add a links line for {key}:\n{m.group(2)}")
            html_ = html_.replace('<div style="clear:both">', f'<br>\n{line}<div style="clear:both">')
        return m.group(1) + html_ + m.group(3)

    body = ENTRY_RE.sub(entry, body)
    if next(it, None) is not None:
        raise ValueError("Fewer list entries than keys")
    return body


# ------------------------------------------------------------------ abstracts

MATH_RE = re.compile(r"(\$\$.+?\$\$|\$.+?\$|\\\(.+?\\\)|\\\[.+?\\\])", re.S)
FONT_RE = re.compile(r"\\(emph|textit|textbf)\s*\{([^{}]*)\}|\{\\(em|it|bf)\s+([^{}]*)\}")
MD_SPECIAL_RE = re.compile(r"([\\*_`\[\]<>#@|~^])")


def abstract_markdown(text: str, where: str) -> str:
    """Convert a LaTeX-flavored abstract to one Markdown paragraph (math kept for MathJax)."""
    text = " ".join(text.split())
    parts = MATH_RE.split(text)
    out = []
    for i, part in enumerate(parts):
        if i % 2:   # math
            if part.startswith(("\\(", "\\[")):
                part = ("$" if part[1] == "(" else "$$") + part[2:-2] + ("$" if part[1] == "(" else "$$")
            d = "$$" if part.startswith("$$") else "$"
            out.append(d + part[len(d):-len(d)].strip() + d)
            continue
        fonts = []

        def font(m):
            cmd, arg = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            fonts.append(("**" if cmd in ("textbf", "bf") else "*", arg))
            return f"\x00{len(fonts) - 1}\x00"
        part = FONT_RE.sub(font, part)
        part = part.replace("\\%", "%").replace("\\&", "&").replace("~", " ")
        # latexcodec drops leading whitespace, which would join text to preceding math.
        lead, trail = part[:len(part) - len(part.lstrip())], part[len(part.rstrip()):]
        part = lead + codecs.decode(part.strip(), "ulatex+utf8").replace("{", "").replace("}", "") + trail
        if "\\" in part or "$" in part:
            raise ValueError(f"LaTeX left in the abstract of {where} after decoding: {part!r}")
        part = MD_SPECIAL_RE.sub(r"\\\1", part)
        part = re.sub(r"\x00(\d+)\x00",
                      lambda m: fonts[int(m.group(1))][0]
                      + MD_SPECIAL_RE.sub(r"\\\1", codecs.decode(fonts[int(m.group(1))][1], "ulatex+utf8"))
                      + fonts[int(m.group(1))][0], part)
        out.append(part)
    return "".join(out).strip()


def bare_arxiv_id(s: str) -> str:
    s = re.sub(r"^(https?://arxiv\.org/abs/|arXiv:)", "", s.strip(), flags=re.I)
    return re.sub(r"v\d+$", "", s)


def arxiv_query(params: dict) -> list:
    url = ARXIV_API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        root = ET.fromstring(r.read())
    entries = []
    for e in root.findall("a:entry", ATOM):
        aid = e.findtext("a:id", "", ATOM)
        title = e.findtext("a:title", "", ATOM)
        if not aid.startswith("http") or title == "Error":
            raise RuntimeError(f"arXiv API error for {url}: {e.findtext('a:summary', '', ATOM)}")
        entries.append({"id": bare_arxiv_id(aid), "title": " ".join(title.split()),
                        "summary": e.findtext("a:summary", "", ATOM).strip(),
                        "authors": [a.findtext("a:name", "", ATOM) for a in e.findall("a:author", ATOM)]})
    return entries


def title_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", norm(s).lower())


JATS_TAG_RE = re.compile(r"<(/?)(?:\w+:)?(\w+)[^>]*>")
JATS_KEEP = {"p": ("", " "), "bold": ("\\textbf{", "}"), "italic": ("\\emph{", "}"),
             "sec": ("", " "), "sup": ("$^{", "}$"), "sub": ("$_{", "}$")}


def jats_to_latexish(s: str, where: str) -> str:
    """Crossref's JATS abstract -> text in the form abstract_markdown() takes.

    Only the tags in JATS_KEEP (and <title>, dropped with its text) are handled;
    anything else, such as MathML, raises an error.
    """
    s = re.sub(r"<(?:\w+:)?title>.*?</(?:\w+:)?title>", " ", s, flags=re.S)

    def tag(m):
        if m.group(2) not in JATS_KEEP:
            raise ValueError(f"Unhandled tag <{m.group(2)}> in the Crossref abstract of {where}")
        return JATS_KEEP[m.group(2)][1 if m.group(1) else 0]
    s = html.unescape(JATS_TAG_RE.sub(tag, s))
    return " ".join(s.split())


def update_abstract_cache(pubs: list, keys: list) -> dict:
    """Fetch arXiv (and else Crossref) abstracts not yet cached; return the cache."""
    cache = yaml.safe_load(ABSTRACT_CACHE.read_text()) if ABSTRACT_CACHE.exists() else {}
    cache = cache or {}
    by_key = {p["pid"]: p for p in pubs}
    stale = set(cache) - set(keys)
    if stale:
        raise KeyError(f"{ABSTRACT_CACHE.name} has keys not in the publication list: {sorted(stale)}")
    need = [k for k in keys if "abstract" not in by_key[k]]

    by_id = {k: bare_arxiv_id(by_key[k]["arxivid"]) for k in need if "arxivid" in by_key[k]}
    fetch = [k for k, aid in by_id.items() if (cache.get(k) or {}).get("arxiv") != aid]
    for i in range(0, len(fetch), 50):
        chunk = fetch[i:i + 50]
        ids = [by_id[k] for k in chunk]
        found = {e["id"]: e for e in arxiv_query({"id_list": ",".join(ids), "max_results": len(ids)})}
        for k in chunk:
            if by_id[k] not in found:
                raise RuntimeError(f"arXiv returned nothing for {k} (arXiv:{by_id[k]})")
            cache[k] = {"arxiv": by_id[k], "abstract": found[by_id[k]]["summary"]}
        time.sleep(ARXIV_DELAY)

    search = [k for k in need if k not in by_id and k not in cache]
    for k in search:
        title = norm(by_key[k]["title"])
        words = re.sub(r"[^\w\s-]", " ", title)
        results = arxiv_query({"search_query": f'ti:"{words}"', "max_results": 10})
        match = [e for e in results if title_key(e["title"]) == title_key(title)
                 and any("Ketcheson" in a for a in e["authors"])]
        if len(match) > 1:
            raise RuntimeError(f"Several arXiv matches for {k}: {[e['id'] for e in match]}")
        cache[k] = ({"arxiv": match[0]["id"], "found_by": "title search",
                     "abstract": match[0]["summary"]} if match else
                    {"arxiv": None, "found_by": f"title search, nothing found {datetime.date.today()}"})
        time.sleep(ARXIV_DELAY)

    # Crossref (publisher metadata), for papers with a DOI that arXiv didn't give an abstract for.
    crossref = [k for k in need if "doi" in by_key[k] and not cache[k].get("abstract")
                and "crossref" not in cache[k]]
    for k in crossref:
        doi = by_key[k]["doi"]
        url = CROSSREF_API + urllib.parse.quote(doi)
        with urllib.request.urlopen(url, timeout=60) as r:
            msg = json.load(r)["message"]
        cache[k]["crossref"] = doi
        if msg.get("abstract") and "inline-graphic" in msg["abstract"]:
            # Formulas given as images; the text alone would have gaps.
            cache[k]["crossref_result"] = "abstract has formulas as images; not used"
        elif msg.get("abstract"):
            cache[k]["abstract"] = jats_to_latexish(msg["abstract"], k)
        else:
            cache[k]["crossref_result"] = f"no abstract {datetime.date.today()}"
        time.sleep(1)

    if fetch or search or crossref:
        ABSTRACT_CACHE.write_text(
            "# arXiv and Crossref abstracts for build_publications.py; see paper_pages.py.\n"
            + yaml.safe_dump(dict(sorted(cache.items())), allow_unicode=True, width=float("inf"),
                             sort_keys=False))
    return cache


# ---------------------------------------------------------------------- pages

def write_if_changed(path: Path, text: str) -> None:
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def write_pages(entries: list, pubs_by_key: dict, abstracts: dict, repos: dict) -> dict:
    """Write papers/<key>/; return counts for the build summary."""
    keys = [k for k, _ in entries]
    PAGES_DIR.mkdir(exist_ok=True)
    orphans = sorted(d.name for d in PAGES_DIR.iterdir() if d.is_dir() and d.name not in keys)
    if orphans:
        raise FileNotFoundError(f"Directories in {PAGES_DIR.name}/ for keys not in the publication "
                                f"list (renamed or removed .bib entries?): {orphans}")
    counts = {"new": 0, "bib": 0, "arxiv": 0, "crossref": 0, "none": [], "repo": 0}
    for key, entry in entries:
        p = pubs_by_key[key]
        d = PAGES_DIR / key
        d.mkdir(exist_ok=True)
        meta = {"title": norm(p["title"]), "author": [" ".join(a.split()) for a in p["authors_list"]]}
        write_if_changed(d / "_metadata.yml",
                         "# Generated by build_publications.py; do not edit by hand.\n"
                         + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=float("inf")))

        img = re.search(r'<img [^>]*/>', entry)
        venue = VENUE_RE.search(entry)
        if not venue:
            raise ValueError(f"No venue found in the list entry for {key}:\n{entry}")
        links = LINKS_RE.search(entry)
        # The page shows its repository in its own section, and is itself the "More information" link.
        page_links = [x for x in parse_links(links.group(1), key) if x[1] != MORE_INFO
                      and not (key in repos and url_key(x[0]) == url_key(repos[key]))] if links else []
        info = ["<!-- Generated by build_publications.py; do not edit by hand. -->", "",
                "```{=html}", '<div class="paper-info">']
        if img:
            info.append(img.group(0).replace("<img ", '<img class="paper-image" ', 1))
        info.append(f'<p class="paper-venue">{" ".join(venue.group(1).split())}</p>')
        if page_links:
            info.append(f'<p class="pub-links">{format_links(page_links)}</p>')
        info += ['<div style="clear:both"></div>', "</div>", "```", ""]

        cached = abstracts.get(key) or {}
        if "abstract" in p:
            info += ["## Abstract", "", abstract_markdown(p["abstract"], key), ""]
            counts["bib"] += 1
        elif cached.get("abstract") and cached.get("arxiv"):
            aid = cached["arxiv"]
            info += ["## Abstract", "", abstract_markdown(cached["abstract"], key), "",
                     f'<p class="abstract-source">Abstract of the arXiv version, '
                     f'<a href="https://arxiv.org/abs/{aid}">arXiv:{aid}</a>.</p>', ""]
            counts["arxiv"] += 1
        elif cached.get("abstract"):
            info += ["## Abstract", "", abstract_markdown(cached["abstract"], key), "",
                     '<p class="abstract-source">Abstract from the publisher\'s metadata '
                     '(via Crossref).</p>', ""]
            counts["crossref"] += 1
        else:
            counts["none"].append(key)

        if key in repos:
            url = repos[key]
            info += ["## Code and data", "", f"Reproducibility repository: <{url}>", ""]
            counts["repo"] += 1
        write_if_changed(d / "_info.qmd", "\n".join(info))

        index = d / "index.qmd"
        if not index.exists():
            index.write_text(INDEX_TEMPLATE.format(key=key))
            counts["new"] += 1
    return counts
