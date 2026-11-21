#!/bin/bash
# Render the site and copy it to the web server.
#
#   ./publish.sh        render, then show what rsync WOULD change (dry run)
#   ./publish.sh --go   render, then actually copy
#
# rsync runs with --delete, so files on the server that are not in _site/
# are removed.  Always look at the dry run before using --go.
set -euo pipefail
cd "$(dirname "$0")"

DEST="dketch@davidketcheson.info:~/davidketcheson.info/"

# (A plain string, not an array: macOS's bash 3.2 treats an empty array as
# unset under "set -u".)
case "${1:-}" in
  "")   DRY=--dry-run ;;
  --go) DRY= ;;
  *)    echo "usage: $0 [--go]" >&2; exit 2 ;;
esac

if [ -n "$(git status --porcelain)" ]; then
  echo "Uncommitted changes in $(pwd); commit them before publishing:" >&2
  git status --short >&2
  exit 1
fi

rm -rf _site
quarto render

for f in index.html posts.xml publications.html 404.html .htaccess favicon.ico; do
  [ -e "_site/$f" ] || { echo "Render is missing _site/$f; not publishing." >&2; exit 1; }
done

# .well-known/ holds DreamHost's HTTPS certificate (Let's Encrypt) challenge
# files; it is not part of the site and must survive --delete.
rsync -avz --delete --exclude=/.well-known/ --itemize-changes ${DRY:+"$DRY"} _site/ "$DEST"

if [ -n "$DRY" ]; then
  echo
  echo "Dry run only: nothing was copied.  Lines starting with *deleting are files"
  echo "that --go would remove from the server."
fi
