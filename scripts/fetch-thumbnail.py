#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["httpx", "beautifulsoup4"]
# ///
"""Pull an og:image (or twitter:image) from a library/travel entry's `link`
and save it into media/ (gitignored, served at /media/...). See README.md
for image sizing guidance.

Usage: uv run scripts/fetch-thumbnail.py content/library/some-entry [--convert webp|avif] [--quality 50] [--resize 1200x630]
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


def read_link(entry_dir: Path) -> str:
    text = (entry_dir / "index.md").read_text()
    match = re.search(r'^\s*link\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise SystemExit(f"No `link` field found in {entry_dir / 'index.md'}")
    return match.group(1)


def find_image_url(page_url: str, html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for prop in ("og:image", "twitter:image"):
        tag = soup.find("meta", attrs={"property": prop}) or soup.find(
            "meta", attrs={"name": prop}
        )
        if tag and tag.get("content"):
            return urljoin(page_url, tag["content"])
    raise SystemExit(f"No og:image or twitter:image found at {page_url}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("entry_dir", type=Path)
    parser.add_argument(
        "--convert", choices=["webp", "avif"], help="also convert to this format via ImageMagick"
    )
    parser.add_argument(
        "--quality", type=int, default=50, help="quality for --convert, e.g. 40/50/60 (default: 50)"
    )
    parser.add_argument(
        "--resize", help="max WxH to shrink to before converting, e.g. 1200x630 (never upscales)"
    )
    args = parser.parse_args()

    entry_dir = args.entry_dir
    if entry_dir.parts[:1] != ("content",):
        raise SystemExit("Path must start with content/, e.g. content/library/some-entry")

    link = read_link(entry_dir)

    headers = {"User-Agent": "Mozilla/5.0 (compatible; fetch-thumbnail/1.0)"}
    with httpx.Client(follow_redirects=True, timeout=15, headers=headers) as client:
        page = client.get(link)
        page.raise_for_status()
        image_url = find_image_url(str(page.url), page.text)

        image = client.get(image_url)
        image.raise_for_status()

    ext = Path(urlparse(image_url).path).suffix or ".jpg"
    media_dir = Path("media", *entry_dir.parts[1:])
    media_dir.mkdir(parents=True, exist_ok=True)
    out_path = media_dir / f"thumbnail{ext}"
    out_path.write_bytes(image.content)

    if args.convert:
        converted_path = media_dir / f"thumbnail.{args.convert}"
        cmd = ["magick", str(out_path)]
        if args.resize:
            cmd += ["-resize", f"{args.resize}>"]
        cmd += ["-quality", str(args.quality), str(converted_path)]
        subprocess.run(cmd, check=True)
        out_path.unlink()
        out_path = converted_path

    url_path = f"/media/{'/'.join(entry_dir.parts[1:])}/{out_path.name}"
    print(f"Saved {out_path}")
    print(f"Add this to {entry_dir / 'index.md'}'s [extra] block:")
    print(f'  thumbnail = "{url_path}"')


if __name__ == "__main__":
    main()
