---
title: "Recurse Center Day 6: B Tree Root"
date: "2021-11-09T16:20:15+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-6"
summary: "B Tree Root: how would you design it?"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## B Tree

I feel I have spent plenty of time with B Tree internals and now I can start coding. Here is my plan:

1. Implement an in-memory B Tree. This will help me learn the B Tree insertion, split, and merge algorithms better. (Also, this will be single threaded. Adding in-memory locks is easy, I see no point in doing them)
1. Add linked lists at the leaf nodes
1. Port it to disk
1. Implement the WAL
1. Explore latch crabbing and support concurrency

Here are some of the documents which helped me learn about B Tree better:

## B Tree Root

B Tree root is a special case. At first, it starts as a leaf node. Once filled, it will split and a new root gets added. 

B Tree grows, like a real tree, from bottom to top. Not top to bottom ;) 

## Tags

I use a [fork](https://github.com/avinassh/hugo-skyfall) of [journal](https://github.com/dashdashzako/hugo-journal) theme. The theme is minimal and did not support tags. So, I added them now.

Adding tags was fairly simple. For tags and categories, Hugo already generates content by default. All you need to do is add a template that says how to render the tags page.

I found these articles to be helpful: [1](https://www.jakewiesler.com/blog/hugo-taxonomies), [2](https://phrye.com/code/tag-cloud), [3](https://www.sidorenko.io/post/2017/07/nice-tagcloud-with-hugo)
