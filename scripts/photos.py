#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
"""Collect photos from content/life/ into content/_photos.json for /photos.

Unlike a general per-page photo-grid (any page can use one — see the
figure/figcaption convention documented in CLAUDE.md), the /photos gallery
itself only draws from content/life/*.md: other sections carry diagrams,
screenshots, and thumbnails, not photos. hidden pages (reference.md) and
_index.md are skipped, same as everywhere else on the site.

Every image in a life/ post's body counts — no opt-in tag needed, since the
whole section is already photo content. A photo's caption is its
<figcaption> text when it's wrapped in a <figure> (matching what's shown
inline in the post), else its alt text (shown only in the lightbox).

life/ front matter convention: `tags` is a high-level grouping, `title`
grabs attention, `description` names the country/restaurant/place — so the
gallery filters by `description`, not `tags` (tags are often shared across
unrelated posts and aren't a useful gallery filter).
"""
import json
import re
import tomllib
from pathlib import Path

root = Path(__file__).resolve().parent.parent
life = root / "content" / "life"

FRONT = re.compile(r'^\+\+\+\n(.*?)\n\+\+\+\n?', re.S)
INLINE_CODE = re.compile(r'`[^`\n]*`')
FIGURE = re.compile(r'<figure\b[^>]*>\s*<img\b([^>]*?)/?>\s*<figcaption>(.*?)</figcaption>\s*</figure>', re.S)
IMG = re.compile(r'<img\b([^>]*?)/?>')
MD_IMG = re.compile(r'!\[([^\]]*)\]\(([^)\s]+?)(?:\s+"[^"]*")?\)')
SRC = re.compile(r'\bsrc\s*=\s*"([^"]+)"')
ALT = re.compile(r'\balt\s*=\s*"([^"]*)"')


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()


def extract(body, title, date, description, href):
    # Blank inline code spans first — a `![caption](src)` shown as a syntax
    # example in prose isn't an embedded photo.
    body = INLINE_CODE.sub(lambda m: " " * len(m.group(0)), body)

    photos = []
    consumed = []

    for m in FIGURE.finditer(body):
        s = SRC.search(m.group(1))
        if s:
            photos.append(dict(src=s.group(1), caption=strip_tags(m.group(2)),
                                title=title, date=date, description=description, href=href))
        consumed.append((m.start(), m.end()))

    # Blank out matched <figure> spans so the img inside isn't double-counted.
    remainder = body
    for start, end in sorted(consumed, reverse=True):
        remainder = remainder[:start] + " " * (end - start) + remainder[end:]

    for m in MD_IMG.finditer(remainder):
        photos.append(dict(src=m.group(2), caption=m.group(1),
                            title=title, date=date, description=description, href=href))

    for m in IMG.finditer(remainder):
        s = SRC.search(m.group(1))
        if not s:
            continue
        alt = ALT.search(m.group(1))
        photos.append(dict(src=s.group(1), caption=alt.group(1) if alt else "",
                            title=title, date=date, description=description, href=href))

    return photos


photos = []
for md in sorted(life.glob("*.md")):
    if md.name in ("_index.md", "reference.md"):
        continue
    text = md.read_text()
    fm = FRONT.match(text)
    if not fm:
        continue
    fm_meta = tomllib.loads(fm.group(1))
    if not fm_meta.get("date"):
        continue

    slug = fm_meta.get("slug") or md.stem
    href = f"/life/{slug}/"
    title = fm_meta.get("title", "")
    date = str(fm_meta["date"])[:10]
    description = fm_meta.get("description", "")

    photos += extract(text[fm.end():], title, date, description, href)

photos.sort(key=lambda p: p["date"], reverse=True)

years = []
for p in photos:
    year = p["date"][:4]
    if not years or years[-1]["year"] != year:
        years.append({"year": year, "photos": []})
    years[-1]["photos"].append(p)

(root / "content" / "_photos.json").write_text(json.dumps({"years": years}, indent=2) + "\n")
print(f"photos: {len(photos)} photo(s) across {len(years)} year(s)")
