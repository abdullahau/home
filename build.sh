#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

# Generate git-based "updated" dates for wiki pages
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

# Stage then rsync into public/ — replacing the directory outright would
# break Caddy's bind mount on it.
rm -rf public.new
zola build -o public.new "$@"
mkdir -p public
rsync -a --delete public.new/ public/
rm -rf public.new
