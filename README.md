# abdullahau/home

Personal website. Static site built using [Zola](https://www.getzola.org/)
and theme inspired by Ellie Huxtable's [page](https://ellie.wtf/).

Content lives in four sections — `work`, `notes`, `projects`, `blog` — plus
a top-level `/about` page (bio and CV). See `CLAUDE.md` for how the content
and templates are organized.

## Setup

Install [Zola](https://www.getzola.org/) and [`just`](https://just.systems/)
with Homebrew:

```
brew install zola just
```

There is no npm/node toolchain and nothing else to install for local
development.

## Preview

```
just serve
```

This builds the site and starts Zola's dev server at `http://127.0.0.1:1111`
with live reload — saving any file in `content/`, `templates/`, or `sass/`
rebuilds and refreshes the browser automatically.

If you're editing over VS Code's Remote-SSH extension (connected to the VPS
this site is hosted on), run `just serve` in the integrated terminal, then:

1. VS Code should pop up "Your application running on port 1111 is
   available. Open in Browser?" — click it, or
2. Open the **Ports** tab (next to Terminal, bottom panel), find `1111`,
   click the globe icon to open it.

VS Code tunnels the port over the existing SSH connection. Nothing is
exposed publicly and this dev server is unrelated to the production Caddy
setup below.

## Build

```
just build
```

Runs `build.sh`, which:

1. Regenerates `content/_git-dates.json` — a git-commit-date lookup for
   `work`/`projects` pages, read by `templates/wiki-page.html` to show an
   "updated" date without you having to maintain it by hand. Gitignored,
   rebuilt every time — never edit it directly.
2. Builds with Zola into a staging directory, then `rsync --delete`s the
   result into `public/`, instead of letting `zola build` delete and
   recreate `public/` itself. That matters once Caddy is running: its
   Docker container bind-mounts `public/`, and swapping the directory out
   (rather than just its contents) breaks that bind mount out from under
   the running container.

`just clean` removes both `public/` and the generated git-dates file. Don't
run it while the Caddy container is up — it deletes `public/` outright,
which breaks the bind mount the same way a plain `zola build` would. If you
do, recreate the container: `cd deploy && docker compose down && docker compose up -d`.

## Deploy

The site is served from this VPS by [Caddy](https://caddyserver.com/)
running in Docker (`deploy/docker-compose.yml` + `deploy/Caddyfile`) —
Docker so the whole setup is portable to another host if needed. Caddy only
serves the static `public/` folder; it has no idea Zola exists.

The Caddyfile sets `Cache-Control` differently for HTML vs. static assets
(CSS, images, the CV PDF), matching what ellie.wtf actually does in
production: HTML always revalidates (`max-age=0, must-revalidate`) so a
deploy is visible immediately, while static assets get a 4-hour cache
window before they revalidate too — since none of them have cache-busting
filenames, a much longer window would risk showing stale CSS/images after
a deploy. Worth knowing if an HTML change ever "doesn't show up" until a
hard refresh, though asset changes should now show up within 4 hours even
without one.

**Bring the server up** (from the repo root):

```
cd deploy
docker compose up -d
```

**Ship a content or template change:**

```
git pull
just build
```

That regenerates `public/`, which is bind-mounted read-only into the Caddy
container — Caddy picks up the new files immediately, no restart needed.

**Change the Caddyfile itself** (e.g. switching from the placeholder `:80`
block to a real domain once one is bought):

```
cd deploy
docker compose down
docker compose up -d
```

Recreate the container rather than `caddy reload`. If you ran
`caddy fmt --overwrite` on the Caddyfile (recommended — keeps it tab-indented
the way Caddy expects), that rewrites the file via an atomic rename, which
leaves an already-running container's bind mount pointing at the old,
now-deleted file. `caddy reload` alone won't pick up the change in that
case; recreating the container will.

**Stop the server:**

```
cd deploy
docker compose down
```

### Going from bare IP to a real domain

`deploy/Caddyfile` currently serves plain HTTP on `:80` (the VPS's bare IP),
with a commented-out block for `abdullah.diy` and `abdullah.run` (both
domains share one block since they serve identical content). Once their
A/AAAA records point at this VPS — check with `dig +short A abdullah.diy`,
you're ready when it returns this VPS's IP:

1. Update `base_url` in `config.toml`.
2. In `deploy/Caddyfile`, comment out the `:80` block and uncomment the
   domain block.
3. Recreate the container: `cd deploy && docker compose down && docker compose up -d`.

Caddy requests and renews the HTTPS certificate for both domains
automatically the first time it serves them — no separate certbot step.
