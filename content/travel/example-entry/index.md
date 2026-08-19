+++
title = "Example trip"
date = 2026-01-01
description = "Country or region"

[extra]
# thumbnail = "/media/travel/example-entry/cover.jpg"

[taxonomies]
tags = ["example"]
+++

This is an example travel entry. Delete it once you have real trip
write-ups.

Trip photos add up fast, so put them in `media/travel/example-entry/`
(gitignored, served from `/media/...` — see CLAUDE.md) rather than in this
folder. Reference them in the Markdown below the same way, e.g.
`![a temple](/media/travel/example-entry/temple.jpg)`. Set
`extra.thumbnail` above to one of those photos to show it on the homepage
and the `/travel/` list next to this entry — leave it unset and the entry
just renders as text, same as an example library entry with no thumbnail.

More notes about the trip go here, with as many inline photos as you want.
