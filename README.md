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
2. Runs `zola build`, producing the static site in `public/`.

`just clean` removes both `public/` and the generated git-dates file.

## Deploy

The site is served from this VPS by [Caddy](https://caddyserver.com/)
running in Docker (`deploy/docker-compose.yml` + `deploy/Caddyfile`) —
Docker so the whole setup is portable to another host if needed. Caddy only
serves the static `public/` folder; it has no idea Zola exists.

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
docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
```

**Stop the server:**

```
cd deploy
docker compose down
```

### Going from bare IP to a real domain

`deploy/Caddyfile` currently serves plain HTTP on `:80` (the VPS's bare IP),
with a commented-out block for a real domain. Once you've bought a domain
and pointed its A/AAAA record at this VPS:

1. Update `base_url` in `config.toml`.
2. In `deploy/Caddyfile`, comment out the `:80` block and uncomment the
   domain block.
3. Reload: `docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile`.

Caddy requests and renews the HTTPS certificate automatically the first
time it serves that domain — no separate certbot step.
