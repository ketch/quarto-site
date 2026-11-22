"""Post-render step: mark the correct navbar item as the current page.

Quarto marks as active the first navbar link whose target also appears in the
sidebar.  Our single sidebar lists every navbar page, so Quarto marks "Home"
as current on every page.  This script recomputes it after each render:

  * a navbar link is current if it points to the page itself;
  * posts (pages under a YYYY/ directory) count as part of "Posts";
  * paper pages (under papers/) count as part of "Publications";
  * pages under interactives/ count as part of "Interactives".

Run by Quarto via `post-render` in _quarto.yml.  It raises an error on pages
whose header doesn't look the way it expects instead of skipping them.
"""
import os
import posixpath
import re
import sys
from pathlib import Path

SITE = Path("_site").resolve()
POSTS_PAGE = "posts.html"
PUBLICATIONS_PAGE = "publications.html"
INTERACTIVES_PAGE = "interactives.html"

HEADER_RE = re.compile(r'<header id="quarto-header".*?</header>', re.S)
LINK_RE = re.compile(r'<a class="nav-link( active)?" href="([^"]*)"( aria-current="page")?>')
YEAR_DIR_RE = re.compile(r"^(19|20)\d\d/")


def current_target(page_rel: str) -> str:
    """Site-relative path of the page the navbar should mark as current."""
    if YEAR_DIR_RE.match(page_rel):
        return POSTS_PAGE
    if page_rel.startswith("papers/"):
        return PUBLICATIONS_PAGE
    if page_rel.startswith("interactives/"):
        return INTERACTIVES_PAGE
    return page_rel


def fix_page(path: Path) -> None:
    page_rel = path.relative_to(SITE).as_posix()
    html = path.read_text(encoding="utf-8")
    header = HEADER_RE.search(html)
    if header is None:
        raise RuntimeError(f"{path}: no <header id=\"quarto-header\"> found")
    links = LINK_RE.findall(header.group(0))
    if not links:
        raise RuntimeError(f"{path}: no navbar links found in header")

    target = current_target(page_rel)
    page_dir = posixpath.dirname(page_rel)

    def replace(m: re.Match) -> str:
        href = m.group(2)
        resolved = posixpath.normpath(posixpath.join(page_dir, href))
        if resolved == target:
            return f'<a class="nav-link active" href="{href}" aria-current="page">'
        return f'<a class="nav-link" href="{href}">'

    new_header = LINK_RE.sub(replace, header.group(0))
    path.write_text(html[: header.start()] + new_header + html[header.end():], encoding="utf-8")


def main() -> None:
    if not SITE.is_dir():
        sys.exit(f"{SITE}/ not found; run from the project root after rendering")
    # Quarto lists the files it just rendered (newline-separated); fall back to
    # every page when the script is run by hand.
    listed = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES")
    if listed:
        pages = [Path(p).resolve() for p in listed.splitlines() if p.endswith(".html")]
    else:
        pages = sorted(SITE.rglob("*.html"))
    for p in pages:
        fix_page(p)
    print(f"fix_nav_active: updated {len(pages)} pages")


if __name__ == "__main__":
    main()
