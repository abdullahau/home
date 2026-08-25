+++
title = "Reference: notes"
date = 2026-01-01
description = "Optional per-page byline — shows under the title when set, on any content type"
hidden = true

[taxonomies]
tags = ["tech"]
+++

Hidden reference page for the `notes` front matter and templates
(`section.html` / `page.html`). `hidden = true` keeps it out of `~/notes`,
the homepage, "Related notes", the search index, the sitemap, and the
RSS/Atom feeds. It shares the `tech` tag with real content on purpose —
`/tags/tech/` and every real tech-tagged page's "Related notes" still
build normally, they just never list this page, since Zola filters hidden
pages out of a taxonomy term's page list before anything reads it. (A tag
used *only* by hidden pages breaks instead: the term ends up with zero
pages and `get_taxonomy_url` errors, since there's nothing left to link
to — reuse an existing tag, don't invent a hidden-only one.) The one thing
Zola does not filter is backlinks, so this page only links to the other
reference pages below — never to real content — so it can never show up
in a real page's "Linked from".

Tags render the same way as any other page:

In-post image reference, via the gitignored `media/` folder (absolute
path, works the same in every section):

![reference image](/media/reference/example.avif)

Cross-content references, using Zola's internal link syntax
(`@/section/file.md`) — this is what populates `page.backlinks` /
"Linked from" on the target page:

- [blog reference](@/blog/reference.md)
- [work reference](@/work/reference.md)
- [projects reference](@/projects/reference.md)
- [library reference](@/library/reference.md)
- [travel reference](@/travel/reference.md)
