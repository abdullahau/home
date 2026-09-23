#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

# Generate git-based "updated" dates for project pages
json="{"
first=true
for section in projects; do
  for file in content/$section/*.md; do
    [ "$(basename "$file")" = "_index.md" ] && continue
    [ ! -f "$file" ] && continue
    git_date=$(git log -1 --format=%ad --date=format:"%b %d, %Y" -- "$file" 2>/dev/null || true)
    if [ -n "$git_date" ]; then
      key="$section/$(basename "$file")"
      if [ "$first" = true ]; then
        first=false
      else
        json="$json,"
      fi
      json="$json \"$key\": \"$git_date\""
    fi
  done
done
json="$json }"
echo "$json" > content/_git-dates.json

# Collect life/ photos into content/_photos.json for /photos (life-only, see scripts/photos.py)
uv run scripts/photos.py

# rsync into public/ — replacing the directory outright breaks Caddy's bind mount.
rm -rf public.new
zola build -o public.new "$@"

# Annotate images with dimensions (justified .photo-grid rows, no layout shift)
uv run scripts/image-meta.py public.new

# Precompress text assets. Caddy's `file_server precompressed` serves these
# directly instead of compressing per request — brotli -q 11 is far too slow
# to run per request, but cheap once per build. Runs against public.new, not
# public: siblings written after the rsync would be dropped by --delete on
# the next build, since they never exist in public.new.
#
# One `sh -c` per file rather than three chained `-exec`s: find treats each
# `-exec` as a test, so a brotli failure would skip zstd and gzip for that
# file and still exit 0 — a half-compressed build, silently. `set -e` inside
# makes that a build failure instead, and `xargs -P` spreads the files across
# all cores (~3x faster here).
if command -v brotli >/dev/null && command -v zstd >/dev/null; then
  find public.new -type f -size +1k \
    \( -name '*.html' -o -name '*.css' -o -name '*.js' \
       -o -name '*.svg' -o -name '*.xml' -o -name '*.json' \) -print0 \
    | xargs -0 -r -P "$(nproc)" -I{} sh -c \
        'set -e; brotli -q 11 -k -f "$1"; zstd -19 -q -f "$1"; gzip -9 -k -f "$1"' _ {}
else
  echo "warning: brotli/zstd not found, skipping precompression" >&2
fi

mkdir -p public
rsync -a --delete public.new/ public/
rm -rf public.new
