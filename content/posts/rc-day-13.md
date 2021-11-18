---
title: "Recurse Center Day 13: Why 'Raft'?"
date: "2021-11-18T17:39:30+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-13"
summary: "I started re-reading Raft and I learned why it is called so!"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## Papers We Love

I don't have much to blog, yesterday I spent most of my day reading [Raft paper](https://raft.github.io/raft.pdf). I have so many questions and I need to spend more time understanding the safety features of the log replication.

However, I learned something entirely new! Why call it Raft? This is a humorous take on the name, explained by Prof. John Ousterhout in [Designing for Understandability: The Raft Consensus Algorithm
](https://www.youtube.com/watch?v=vYp4LYbnnW8&t=3598s) video.

1. It stands for Replicated And Fault Tolerant

![](/blag/images/2021/why-raft-1.png)

2. Raft is something you build out of a collection of logs <3

![](/blag/images/2021/why-raft-2.png)

3. (the best one) Raft is something you could use to get away from the island of Paxos

![](/blag/images/2021/why-raft-3.png)

From the same video, John also says how difficult it was for them to have the paper accepted at the conferences. It was rejected three times because the paper seemed too simple and people love complexity!

## Coffee Chat

I had a coffee chat with Layla, we shared ideas, discussed so many things from distributed systems to building an Instagram clone.
