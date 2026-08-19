# Abdullah Mahmood — Personal Site

Static site built with [Zola](https://www.getzola.org/). Live at
[abdullah.diy](https://abdullah.diy) / [abdullah.run](https://abdullah.run).

Content lives in six sections — `notes`, `projects`, `blog`, `work`,
`library`, `travel` — plus a top-level `/about` page. See `CLAUDE.md` for
how content, templates, and hosting are organized in more depth than this
file covers.

## Setup

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
above.

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
the bind mount to `public/` can otherwise end up stale. See `CLAUDE.md`
for why, plus other Caddy/Docker gotchas (Caddyfile edits, Cloudflare's
separate edge cache, etc.).

**Stop the server:**

```
cd deploy
docker compose down
```
