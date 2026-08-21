+++
title = "Reference: travel"
date = 2026-01-01
description = "Shows as a byline, and as the og:image/homepage thumbnail source"
hidden = true

[extra]
thumbnail = "/media/travel/reference/cover.avif"

[taxonomies]
tags = ["tech"]
+++

Hidden reference page for the `travel` front matter and templates
(`thumb-section.html` / default `page.html`). `extra.thumbnail` feeds the
homepage/list thumbnail and `og:image`, but deliberately never renders as
a heading image on this page — unlike `library`. See
[notes reference](@/notes/reference.md) for the full explanation of what
`hidden = true` does and why this only links to other reference pages.

In-post image reference:

![reference image](/media/reference/example.avif)

Cross-content references:

- [notes reference](@/notes/reference.md)
- [blog reference](@/blog/reference.md)
- [work reference](@/work/reference.md)
- [projects reference](@/projects/reference.md)
- [library reference](@/library/reference/index.md)
