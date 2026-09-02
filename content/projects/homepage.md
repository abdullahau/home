+++
title = "Personal website"
date = 2026-07-25
description = ""

[taxonomies]
tags = ["tech"]
+++

Repo → [https://github.com/abdullahau/home](https://github.com/abdullahau/home)

- Meaning to create my own website to post blogs, notes, and watched/read list using as few a dependencies as possible. 
- In particular I wanted to stay away from proprietary website builders or the entire JS/node/npm tool chain and stack
- Given the purpose of the website, it made sense that I needed a static website as opposed to a dynamic site. There is simply no need for a CMS system
- I stumbled across Ellie’s website. I was impressed by the terminal theme, speed, and the low resource usage that it took to render the page,
- In particular I liked the Zettelkasten-style interconnected pages that was akin to my note taking workflow on Logseq or obsidian. 
- Luckily, I found her repo on github and decided I would get Claude to go to town modifying the codebase with my modifications.
- The choice of using an LLM to code up this website with little oversight was obvious — I’m not a website developer and I do not foresee myself making websites as an intellectual endeavor or a professional one at that.
- The technology, hosting, and server stack is pretty straight forward and delivers my objective of low maintenance, easy to use, low resource usage, speed/optimization, fast build time, open source tools, no vendor lock in, low to free cost tools and application, and simple to deploy and port. 
    - Zola - no dependencies, batteries included (markdown rendering - intuitive content drafting, syntax highlighting, sass compilation for styling, search index generation, image processing, tags/categories, etc)
    - Just
    - Caddy (for pages and images) 
    - Cloudflare - authoritative DNS 
    - VS Code/Zed - editor