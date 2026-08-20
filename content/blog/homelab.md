+++
title = "Tinkering with my homelab setup"
date = 2026-07-20

[taxonomies]
tags = ["homelab", "tech"]
+++

I have spent the last year tinkering with and assembling tools for my work.
In the process, I learned a bit about docker, self-hosted servers, and ways 
to deliver those services to users. 

Eventually, I decides I could repurpose my old macbook, run services through this
always-on computer, and take the load of my daily driver to run everything from 
media, adblocker, and remote development.

Here is a snapshot of my service right now:

![homelab setup](/media/projects/homelab/homelab-network-diagram.png) 

You can find details of my docker services on my [homelab repo](https://github.com/abdullahau/homelab).
Which can be used along with my [dotfiles repo](https://github.com/abdullahau/dotfiles) (`git switch homelab`) 
to setup your own homelab. Dotfiles repo setups Docker, Tailscale, samba and other configurations
on a fresh Linux Ubuntu machine.

In my case, because I am using a laptop, it sets a lid switch config to allow the laptop run in clamshell mode.