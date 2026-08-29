# Abdullah Mahmood — Personal Site

Static site built with [Zola](https://www.getzola.org/) and theme inspired
by Ellie Huxtable's [page](https://ellie.wtf/). Live at
[abdullah.run](https://abdullah.run) / [abdullah.diy](https://abdullah.diy).

Content lives in six sections — `notes`, `projects`, `blog`, `work`,
`library`, `life` — plus a top-level `/about` page and a `/photos` gallery
generated from `life/` (see CLAUDE.md for both).

## Setup

Install [Zola](https://www.getzola.org/) and [`just`](https://just.systems/)
— any package manager works, e.g. with Homebrew:

```
brew install zola just
```

No npm/node toolchain, nothing else to install.

## Preview

```
just serve
```

Dev server at `http://127.0.0.1:1111` with live reload. Editing over VS
Code Remote-SSH: open the **Ports** tab and forward `1111` to preview in
your local browser.

## Build

```
just build
```

Runs `build.sh` — regenerates `content/_git-dates.json`, builds with Zola,
syncs the result into `public/`.

```
just clean
```

Removes `public/` and the generated git-dates file. Don't run this while
the Caddy container is up (see Deploy).

## Deploy

Caddy, running in Docker (`deploy/`), serves `public/` at the two domains
above. It sends `Cache-Control: max-age=0` for HTML (always fresh) and a
4-hour cache for static assets like CSS and images before they revalidate.

**First time, bring the server up:**

```
cd deploy
docker compose up -d
```

**Every time after, to ship a change:**

```
git pull        # if the change was made elsewhere
just build
cd deploy
docker compose down
docker compose up -d
```

Always recreate the container after a build, not just restart/reload —
the bind mount to `public/` can otherwise end up stale.

**Stop the server:**

```
cd deploy
docker compose down
```

## Images

Use AVIF or WebP. [ImageMagick](https://imagemagick.org/) converts,
compresses, resizes, and strips metadata in one command:

```
magick input.jpg -resize 'WxH>' -quality Q +profile 'exif,xmp,8bim,iptc' output.avif
```

**Thumbnails** (fit a 1200x630 box):

```
magick input.jpg -resize '1200x630>' -quality 50 +profile 'exif,xmp,8bim,iptc' output.avif
```

**Body images** (cap the width at 1600):

```
magick input.jpg -resize '1600x>' -quality 50 +profile 'exif,xmp,8bim,iptc' output.avif
```

`WxH>` fits the image inside a box. `Wx>` caps the width only. Both keep
the aspect ratio and never upscale or crop.

`-quality 50` is the site default. `+profile 'exif,xmp,8bim,iptc'` drops
camera and GPS data but keeps the ICC color profile — don't use `-strip`,
which removes the profile too and can shift colors.

To strip an AVIF that is already converted, use `exiftool` — ImageMagick
would re-encode it:

```
exiftool -all= -tagsFromFile @ -icc_profile:all -overwrite_original file.avif
```

### Embedding images in post content

Four patterns, all raw HTML in the markdown body (no shortcode):

**A normal photo** — full width of the column:

```html
<img src="/media/life/trip/photo.avif" alt="Optional hidden caption" />
```

**A justified photo grid** (`.photo-grid`) — a run of photos packed into
rows, no cropping:

```html
<div class="photo-grid">
<img src="/media/life/trip/a.avif" />
<img src="/media/life/trip/b.avif" alt="Hidden caption" />
<figure>
  <img src="/media/life/trip/c.avif" />
  <figcaption>Visible caption</figcaption>
</figure>
</div>
```

`scripts/image-meta.py` sets each image's aspect ratio (`--ar`) at build
time — don't set `width`/`height`/`style` by hand. Every image in
`content/life/*.md` also goes into the `/photos` gallery (see CLAUDE.md).

**A tall (portrait) shot** (`img.tall-img`) — caps the height and centers
the image:

```html
<img class="tall-img" src="/media/life/trip/portrait.avif" alt="…" />
```

**Two images side by side** (`.img-pair`) — capped height, stacks to one
column on narrow screens:

```html
<div class="img-pair">
<img src="/media/life/trip/left.avif" />
<img src="/media/life/trip/right.avif" />
</div>
```

**Captions.** A `<figure>`/`<figcaption>` caption shows under the photo and
in the lightbox. A bare `alt="…"` shows only in the lightbox.
