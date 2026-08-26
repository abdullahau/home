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

To load images faster with the lowest memory footprint, use AVIF/WebP
formats with appropriate quality compression and image sizing.

Use [ImageMagick](https://imagemagick.org/) to convert image format, set
the quality compression level, resize, and strip metadata, all in one
command:

```
magick input.jpg -resize 'WxH>' -quality Q +profile 'exif,xmp,8bim,iptc' output.avif
```

Its `-resize` geometry controls how width and height combine:

- `WxH>` — fit inside a box of that width and height, aspect ratio
  preserved (shrinks only, never crops, never upscales)
- `Wx>` — cap the width only; height follows the aspect ratio
  automatically

Use `WxH>` for thumbnails, `Wx>` for images inside post content.

**Thumbnails** (~1200x630 box):

```
magick input.jpg -resize '1200x630>' -quality 50 +profile 'exif,xmp,8bim,iptc' output.avif
```

**Body images** (~1600 wide):

```
magick input.jpg -resize '1600x>' -quality 50 +profile 'exif,xmp,8bim,iptc' output.avif
```

`-quality 50` is the AVIF default used across this site. `+profile
'exif,xmp,8bim,iptc'` strips camera/GPS/software metadata — phone photos
carry exact GPS coordinates by default — while keeping the ICC color
profile (`-strip` removes everything including that; iPhone photos are
often tagged Display P3, not sRGB, so dropping it can shift colors on
wide-gamut screens).

Already-converted AVIFs can't be re-stripped with ImageMagick without
another lossy re-encode. Use `exiftool` instead, which edits metadata
without touching pixel data:

```
exiftool -all= -tagsFromFile @ -icc_profile:all -overwrite_original file.avif
```

### Embedding images in post content

Four patterns, all raw HTML in the markdown body (no shortcode) — pick
whichever fits the image:

**A normal photo.** Just an `<img>` (or plain markdown `![]()`), full width
of the column:

```html
<img src="/media/life/trip/photo.avif" alt="Optional hidden caption" />
```

`alt` isn't shown inline — it only surfaces as a caption if the image is
opened in the lightbox (see "Captions" below).

**A justified photo grid** (`.photo-grid`) — for a run of photos from the
same moment, packed into rows with no cropping:

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

Row heights and each image's aspect ratio (`--ar`) come from
`scripts/image-meta.py` at build time — don't set `width`/`height`/`style`
by hand here. Every image inside `content/life/*.md` also gets pulled into
the `/photos` gallery automatically (see CLAUDE.md).

**A tall (portrait) shot** (`img.tall-img`) — outside a grid, when a
full-width portrait photo would run too tall. Caps the height and centers
it instead of stretching to the column width:

```html
<img class="tall-img" src="/media/life/trip/portrait.avif" alt="…" />
```

**Two images side by side** (`.img-pair`) — a before/after or two related
shots, capped height, stacking to one column on narrow screens:

```html
<div class="img-pair">
<img src="/media/life/trip/left.avif" />
<img src="/media/life/trip/right.avif" />
</div>
```

**Captions.** Wrap an image in `<figure>…<figcaption>…</figcaption></figure>`
for a caption shown under the photo *and* in the lightbox. Use a bare
`alt="…"` (no `<figcaption>`) for a caption that's hidden inline and only
shows up in the lightbox, styled small and grey like a footnote — good for
a detail that's not worth breaking the flow of the post for.
