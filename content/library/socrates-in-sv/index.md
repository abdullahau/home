+++
title = "Reading Socrates in Silicon Valley"
date = 2026-03-24
description = "Jemima Kelly"

[extra]
type = "Article"
link = "https://www.ft.com/content/f9e57ed6-ad07-491c-830a-88ba92d77add"
thumbnail = "/media/library/socrates-in-sv/thumbnail.avif"

[taxonomies]
tags = ["art & culture", "tech", "philosophy"]
+++

This is an example library entry. Delete it once you have real entries.

`extra.thumbnail` is a path served from `media/` (gitignored — see
CLAUDE.md), not committed to the repo: drop an image at
`media/library/example-entry/thumbnail.jpg` on the VPS and set
`thumbnail` to `/media/library/example-entry/thumbnail.jpg` as above.
Leave it unset (as here) and the entry just renders without one — no
placeholder box. To pull one automatically from the `link` above instead
of adding it by hand, run:

```
uv run scripts/fetch-thumbnail.py content/library/example-entry
```

(A bare filename like `cover.jpg` also works and is resolved as a
colocated page-bundle image next to this `index.md` instead — fine for a
one-off, but committed to git, unlike `media/`.)

`extra.type` becomes the "Book:", "Article:", "Video:", "Movie:" (etc.)
prefix on the title. `description` doubles as the author/creator, shown in
the meta line. Everything below the front matter is your own notes and
comments about it, as normal Markdown.
