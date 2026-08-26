#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow"]
# ///
"""Annotate <img> tags in the build output with width/height and an --ar var,
so .photo-grid can lay out justified rows with no layout shift.

/media/... resolves to the gitignored, VPS-only media/ dir; anything else to
the build output. Dimensions cache in image-meta.json (gitignored).
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parent.parent
public = root / (sys.argv[1] if len(sys.argv) > 1 else "public")
cache_path = root / "image-meta.json"
cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

IMG = re.compile(r'<img\b([^>]*?)\s*/?>')
SRC = re.compile(r'\bsrc\s*=\s*"([^"]+)"')
STYLE = re.compile(r'\bstyle\s*=\s*"([^"]*)"')
HAS_SIZE = re.compile(r'\b(width|height)\s*=')
FIGURE = re.compile(r'<figure\b((?:(?!style=)[^>])*)>(\s*<img\b[^>]*--ar:([\d.]+)[^>]*>)')


def resolve(url):
    if "://" in url:
        return None  # no remote images on this site (yet)
    if url.startswith("/media/"):
        return root / "media" / url[len("/media/"):]
    if url.startswith("/"):
        return public / url.lstrip("/")
    return None  # relative path — flat content files must use absolute ones


def fetch(url):
    if url in cache:
        return cache[url]
    path = resolve(url)
    if path is None or not path.is_file():
        print(f"image-meta: could not read {url} (missing: {path})", file=sys.stderr)
        return None
    try:
        with Image.open(path) as img:
            meta = {"width": img.width, "height": img.height}
    except Exception as e:
        print(f"image-meta: could not read {url}: {e}", file=sys.stderr)
        return None
    cache[url] = meta
    print(f"image-meta: {url} -> {meta['width']}x{meta['height']}")
    return meta


def annotate(m):
    attrs = m.group(1)
    s = SRC.search(attrs)
    if not s or "--ar" in attrs:
        return m.group(0)
    meta = fetch(s.group(1))
    if not meta:
        return m.group(0)
    ar = f'--ar:{meta["width"] / meta["height"]:.4f}'

    # Merge into an existing style="" rather than emitting a second one —
    # duplicate attributes are invalid and the browser keeps only the first.
    style = STYLE.search(attrs)
    if style:
        existing = style.group(1).rstrip().rstrip(";")
        merged = f'{existing};{ar}' if existing else ar
        attrs = attrs[:style.start()] + f'style="{merged}"' + attrs[style.end():]
    else:
        attrs = f'{attrs} style="{ar}"'

    # Author-set width/height wins; don't duplicate it.
    if not HAS_SIZE.search(attrs):
        attrs = f'{attrs} width="{meta["width"]}" height="{meta["height"]}"'
    return f'<img{attrs}>'


changed = 0
for html in public.rglob("*.html"):
    text = html.read_text()
    new = IMG.sub(annotate, text)
    # A <figure> wrapping an image inherits its --ar so it can be a grid item.
    new = FIGURE.sub(lambda m: f'<figure{m.group(1)} style="--ar:{m.group(3)}">{m.group(2)}', new)
    if new != text:
        html.write_text(new)
        changed += 1

cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n")
print(f"image-meta: updated {changed} file(s)")
