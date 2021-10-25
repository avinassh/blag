---
title: "What I want to do at Recurse Center"
date: "2021-10-24T19:46:15+05:30"
categories: ["recurse-center", "projects"]
tags: ["rc", "recurse", "recurse-center"]
slug: "rc-plans"
summary: "Projects I want to work on at RC"
---

I will be [joining the Recurse Center]({{< ref "posts/rc-accepted-woooooooo" >}}) for their Winter 1 '21 batch (Nov 2021 – Feb 2022). I want to use this time learning about systems programming: storage, compilers, networking. I dream of becoming a systems programmer, hacking on databases or message queues, one day 🧑‍💻.

RC is a self-directed programme, so everyone is free to work on things that interest them. They [recommend](https://www.recurse.com/manual#sec-advice) working on things that are challenging to do. This aligns with [Andrew NG's advice](https://twitter.com/AndrewYNg/status/841076327931236352) on taking on projects you are only 70% qualified for.

I don't think I will be able to work on all of the following, but I am keeping my options open. Keeping an exhaustive list would also help me to switch to something else if I am stuck on or bored. 

## A simple KV Store 

I want to understand how exactly databases store the data on disk. I would like to explore the different ways it is being done in different databases and implement a simple KV store backed by a B Tree. I find the implementation of a  B Tree quite daunting, especially the doubly linked list at the leaf nodes. I am hoping this will also give me an opportunity to learn more about [zero-copy](https://developer.ibm.com/articles/j-zerocopy/).

Implementing a B Tree would also help me with [my side project with SQLite](https://github.com/avinassh/fast-sqlite3-inserts). Perhaps, I could exploit the [SQLite B Tree API](https://sqlite.org/btreemodule.html) to insert a billion rows if I understand the file format and storage layout.

## Hack Go Compiler

I would like to study the Go compiler internals, maybe [add a new keyword](https://eli.thegreenplace.net/2019/go-compiler-internals-adding-a-new-statement-to-go-part-1/) for fun (e.g. Python style for/else). 

## A multiplayer game

I want to learn more about sockets, firewalls, NATs etc and make two computers talk, without a central server. Topics to explore: P2P protocols, WebRTC. 


## Few more ideas

- Learn about async programming, multi-threading and write a toy green threads implementation
- Build a toy code search engine, learn about Kythe and Zoekt etc.

Some general aspects I would like to improve upon

- My low-level design (LLD) skills aren't good, I'd like to get better at it. I want to learn about how to modularise the code properly, make interfaces, abstractions, and learn about OOPs
- I would like to get better at communicating my ideas succinctly
- Writing. Write faster, better and clear
- Give talks and share ideas

I have never pair programmed with anyone, so looking to pair and collaborate as much as possible. I am planning to allocate 30% of my time for collaboration. 

