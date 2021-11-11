---
title: "Recurse Center Day 8: B Tree Fill Factor (Part 2)"
date: "2021-11-11T16:00:32+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin", "btree"]
slug: "rc-day-8-old"
summary: "I found out the answer to B tree fill factor "
---

<div style="font-size: 0.7rem; margin: 2rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## B Tree Fill Factor

[Earlier]({{< ref "posts/rc-day-4" >}}), I was wondering how does B Tree have a constant or same fill factor across all the nodes. I found various answers.

From Database Internals book:

1. Once the fill factor and number of keys are fixed, the nodes can use an overflow node if it cannot fit all those keys in a single node
1. B Tree also stores just the prefixes in the internal nodes, because full keys are not necessary. If prefixes are of the same size, then we can have the same fill factor for all the nodes

I was watching Berkeley's [CS148](https://cs186berkeley.net/) lectures and they say instead of using keys for fill factor, we could use bytes. That is, each node is considered full when it reaches a certain percentage of bytes.

## Coffee Chat

The [virtual RC](https://www.youtube.com/watch?v=Qv801wYJoXQ) has a feature called Coffee Chat where it matches two people to chat. I spoke with Trevor today, who is currently at RC from the (previous) Fall 2 batch. We discussed quite many things from general RC things, career, work culture etc. 

Coffee Chats are a great way to meet new people and I look forward to meeting more interesting folks!
