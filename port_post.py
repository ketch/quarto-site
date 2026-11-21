"""Port Jekyll posts from ../_posts into this Quarto site.

Usage: python3 port_post.py ../_posts/*.md ../_posts/*.html

Each post YYYY-MM-DD-name.{md,html} is written to YYYY/MM/DD/name.md so that
the rendered URL (/YYYY/MM/DD/name.html) matches the Jekyll permalink.

Front matter: drop `layout`, `name`, `time`; take `date` from the filename;
turn `tags` (list or space-separated string) into Quarto `categories`, plus
the Jekyll category `notebook` if present (`blog-post` is dropped).

Body:
  - `{{ site.baseurl }}` -> `/` (Quarto resolves root-relative paths from the
    project root), `{% post_url X %}` -> /YYYY/MM/DD/name.html,
    `{% highlight lang %}...{% endhighlight %}` -> fenced code blocks.
  - HTML posts are converted to Markdown with pandoc (see html_cleanup.lua).
    `$...$` math is parsed only in HTML posts that loaded MathJax; elsewhere
    `$` is treated as a dollar sign.
  - Local files referenced as /assets/... or /notebooks/... are copied from
    the Jekyll site into this project.

Posts whose destination already has a hand-written .qmd are skipped.
Anything unexpected raises an error instead of being skipped.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
JEKYLL_ROOT = Path.home() / "Research/Projects/labnotebook"  # the old Jekyll site
NAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.(md|html)$")
BASEURL_RE = re.compile(r"\{\{\s*site\.baseurl\s*\}\}/?")
POST_URL_RE = re.compile(r"\{%\s*post_url\s+(\d{4})-(\d{2})-(\d{2})-(\S+?)\s*%\}")
HIGHLIGHT_RE = re.compile(r"\{%\s*highlight\s+(\w+)\s*%\}")
ENDHIGHLIGHT_RE = re.compile(r"\{%\s*endhighlight\s*%\}")
LOCAL_REF_RE = re.compile(r"""(?<![\w.:/])/((?:assets|notebooks)/[^\s)"'<>]+)""")
KNOWN_KEYS = {"layout", "name", "time", "title", "subtitle", "tags", "categories"}


def split_front_matter(src: Path):
    text = src.read_text()
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0] != "":
        raise ValueError(f"No YAML front matter found in {src}")
    return yaml.safe_load(parts[1]), parts[2]


def convert_meta(meta: dict, date: str, src: Path) -> dict:
    unknown = set(meta) - KNOWN_KEYS
    if unknown:
        raise ValueError(f"Unexpected front matter keys in {src}: {unknown}")
    tags = meta.get("tags") or []
    if isinstance(tags, str):
        tags = tags.split()
    jekyll_cats = meta.get("categories") or []
    if isinstance(jekyll_cats, str):
        jekyll_cats = jekyll_cats.split()
    if set(jekyll_cats) - {"blog-post", "notebook"}:
        raise ValueError(f"Unexpected Jekyll categories in {src}: {jekyll_cats}")
    cats = list(tags) + [c for c in jekyll_cats if c == "notebook" and c not in tags]

    out = {"title": meta["title"]}
    if meta.get("subtitle"):
        out["subtitle"] = meta["subtitle"]
    out["date"] = date
    if cats:
        out["categories"] = cats
    return out


def replace_liquid(body: str, src: Path) -> str:
    body = POST_URL_RE.sub(lambda m: "/{}/{}/{}/{}.html".format(*m.groups()), body)
    body = BASEURL_RE.sub("/", body)
    body = HIGHLIGHT_RE.sub(lambda m: f"```{m.group(1)}", body)
    body = ENDHIGHLIGHT_RE.sub("```", body)
    leftover = re.findall(r"\{\{.*?\}\}|\{%.*?%\}", body)
    if leftover:
        raise ValueError(f"Unconverted Liquid tags in {src}: {leftover}")
    return body


MATHJAX_SCRIPT_RE = re.compile(
    r"<script[^>]*(?:x-mathjax-config|cdn\.mathjax\.org)[^>]*>.*?</script>", re.S)
GIST_SCRIPT_RE = re.compile(
    r"""<script\s+src=["'](https://gist\.github\.com/[^"']+\.js)["']\s*>\s*</script>""")
GIST_PLACEHOLDER = "GISTEMBEDPLACEHOLDER"


def html_to_markdown(body: str, src: Path) -> str:
    uses_math = "MathJax" in body or "mathjax" in body
    # Pandoc's HTML reader silently drops <script>, so handle scripts here:
    # old MathJax loaders are removed (Quarto adds MathJax), gist embeds are
    # kept as raw HTML, and anything else is an error.
    body = MATHJAX_SCRIPT_RE.sub("", body)
    gists = GIST_SCRIPT_RE.findall(body)
    body = GIST_SCRIPT_RE.sub(f"<p>{GIST_PLACEHOLDER}</p>", body)
    if "<script" in body:
        raise ValueError(f"Unhandled <script> in {src}")
    reader = "html+tex_math_dollars+tex_math_single_backslash" if uses_math else "html"
    result = subprocess.run(
        ["pandoc", "-f", reader,
         "-t", "markdown-native_divs-native_spans-header_attributes-link_attributes",
         "--wrap=none", "--lua-filter", str(HERE / "html_cleanup.lua")],
        input=body, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc failed on {src}:\n{result.stderr}")
    if result.stderr.strip():
        print(f"  pandoc warnings for {src.name}:\n{result.stderr}", file=sys.stderr)
    md = result.stdout
    if md.count(GIST_PLACEHOLDER) != len(gists):
        raise RuntimeError(f"Gist placeholders not preserved in {src}")
    for url in gists:
        md = md.replace(GIST_PLACEHOLDER, f'```{{=html}}\n<script src="{url}"></script>\n```', 1)
    return md


def copy_local_refs(body: str, src: Path):
    for rel in sorted(set(LOCAL_REF_RE.findall(body))):
        source = JEKYLL_ROOT / rel
        if not source.is_file():
            raise FileNotFoundError(f"{src} references /{rel}, which does not exist")
        dest = HERE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)


def port(src: Path):
    m = NAME_RE.match(src.name)
    if not m:
        raise ValueError(f"Filename does not match YYYY-MM-DD-name.(md|html): {src}")
    year, month, day, name, ext = m.groups()
    dest = HERE / year / month / day / f"{name}.md"
    if dest.with_suffix(".qmd").exists():
        return f"skipped {src.name} (hand-written {dest.with_suffix('.qmd').relative_to(HERE)} exists)"

    meta, body = split_front_matter(src)
    meta = convert_meta(meta, f"{year}-{month}-{day}", src)
    body = replace_liquid(body, src)
    if ext == "html":
        body = html_to_markdown(body, src)
    copy_local_refs(body, src)

    dest.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True)
    dest.write_text(f"---\n{front}---\n{body}")
    return str(dest.relative_to(HERE))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        print(port(Path(arg)))
