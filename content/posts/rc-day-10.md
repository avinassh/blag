---
title: "Recurse Center Day 10: Learning Distributed Systems"
date: "2021-11-13T23:22:10+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-10"
summary: "How does one start learning to build distributed systems?"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

Most of my day went into trying to understand more of Dynamo paper and making notes. 

## Distributed Systems

I read this splendid [article](https://brooker.co.za/blog/2019/04/03/learning.html) on "Learning to build distributed systems" by Marc Brooker (leads engineering on AWS Lambda). Key takeaways:

- Learn internals and practical patterns for Distributed Systems from the multiple resources: papers, open source code and YouTube videos
- Write your own: Get your hands dirty and write one, test it using [Jepsen](https://jepsen.io/)
- Work with a team/company that builds similar systems at scale
- Volunteer for pager duty/on-call and for debugging the hard issues

## B Tree

I was having difficulty with the insertion algorithm. The difficulty I was dealing with was, how do I propagate the changes like splits from children to the parent. Phil who had implemented a B Tree earlier suggested looking into CLRS for the algorithm. Till now, I was trying to implement it from the descriptions I read on the internet and explanations I saw in videos. Seeing the algorithm and pseudocode helped a lot!
