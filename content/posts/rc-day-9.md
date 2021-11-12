---
title: "Recurse Center Day 9: Papers We Love"
date: "2021-11-12T16:35:35+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-9"
summary: "I learnt a few things about Dynamo"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## Papers We Love

RC has a Papers We Love group where we meet every Wednesday to discuss a paper. Yesterday, we discussed the Dynamo paper. I had this paper on my to-read list for a long time and I finally had a chance to read it. 

The Dynamo paper introduces lots of brilliant yet simple ideas, which I think itself deserves a separate post:

- Consistent Hashing with a twist of virtual nodes
- Sloppy quorum for consistency and performance
- Hinted Handoff
- Merkle Trees to detect inconsistencies between replicas (anti entropy)
- Read repair
- Write buffer to increase write performance
- Simple yet powerful config of (N, W, R)

## B Tree Node

I had posted about the design of storing B Tree nodes earlier ([day 2]({{< ref "posts/rc-day-2" >}}), [day 3]({{< ref "posts/rc-day-3" >}})), Oliver suggested another alternative to it! We store an array with single pointers like earlier, just that in the last item we won't store any key:

```
[(7, *1), (16, *9), (*18)]
```

With this design, in the last struct, we should never store any key. The only drawback I can think of with this design is while iterating, for insertion we have to be extra careful to not check the array to its full length. Probably, any kind of loop iteration which I am doing, I have to skip the last item in the array.


## People

I paired with Oliver and Phil today for the B Tree project. I explained to them the basics of B Tree and we discussed the insertion algorithm,  brainstormed on how to recursively do the insertion and propagate the changes to the parent nodes.

Phil also introduced me to [Nightmare](https://guyinatuxedo.github.io/), which is an intro to binary exploitation / reverse engineering course. He also went on to solve [one of the exercises](https://guyinatuxedo.github.io/05-bof_callfunction/csaw18_getit/index.html) in which you had to exploit stack buffer overflow to get access to the shell. It was magic!
