---
title: "Internet is wholesome: MVCC edition"
date: "2023-04-20T22:19:15+05:30"
categories: ["database", ""]
tags: ["database", "hekaton", "typo", "mvcc"]
slug: "hekaton-paper-typo"
summary: "It is a short story about how I hit a wall while implementing a database research paper, found a publication error and how people on the internet helped me."
---

It is a short story about how I hit a wall while implementing a database research paper, found a publication error and how people on the internet helped me. 

## Timeline

- `$whoami` I am a backend developer interested in databases, and they excite me! I dream of being a database developer one day. I have an educational side project called [CaskDB](https://github.com/avinassh/py-caskdb). It aims to teach how to build a key-value store. I always look forward to adding new database features, as it allows me to learn new things. 
- [7th Apr] Pekka Enberg [tweeted](https://twitter.com/penberg/status/1644221651293204480) about the [Hekaton MVCC paper](https://vldb.org/pvldb/vol5/p298_per-akelarson_vldb2012.pdf). This research paper was new to me, and I found it approachable. CaskDB does not have transactions yet, so I thought it would be a great learning opportunity for me to implement it.
- [8th Apr] Pekka started implementing the paper in Rust and [tweeted](https://twitter.com/penberg/status/1644676555942109185) about it. It became easy for me to follow the paper with the code. I also started working on my [Go implementation](https://github.com/avinassh/mvcc-go).
- I am a massive fan of Andy and have watched the videos from his course [CMU Advanced Database Systems](https://15721.courses.cs.cmu.edu/spring2023/). I started rewatching the lectures on Hekaton. The lecture series is quite good; go check it out!
- I started making notes. At first, it seemed easy to comprehend, but I noticed gaps in my understanding when I began thinking about the implementation. I watched Andy's lecture again to reinforce my learning.
- [Apr 9] I started working through the paper's `Version Visibility` section. This part explains an ongoing transaction's effect on a row's visibility. It addresses the questions like transaction `tx1` updated a row; can `tx2` see it? Some of the ideas around row visibility didn't make sense.
- I went back to the paper and reread it several times now. I thought maybe I had missed something from the earlier sections. I took a pencil and paper and started drawing all possible flows. I did it multiple times, but no vain.
- For a moment, I started wondering if the papers could have errors. But this is a famous paper, and since I couldn't find anything online, I thought I did not understand it correctly. I being a noob didn't help.
- I stopped sleeping.
- I started asking in Slack / Discord / Zulip groups. I explained the paper to one of my friends and asked if he saw any issues. Nothing helped!
![](/blag/images/2023/hekaton-rc.png)
- [Apr 12] I emailed one of the authors, Professor Spyros Blanas, with zero hopes of hearing anything back.
- [Apr 13] I woke up to the Professor's reply, and they acknowledged that there was indeed a typo in the paper! What a blissful morning! Not only was he kind enough to reply, but he also gave me a high-level idea of how things should be.
- From one of the groups, [Alex Miller](https://transactional.blog) saw my message. It turns out he is friends with another author Cristian, and they discussed my issue. He agreed that one of the tables needed to be corrected. My morning just got better!
- It surprised me that published papers can have typos — even the popular ones.
- [Apr 14] I discussed the issue with Pekka. I filed [an issue](https://github.com/penberg/mvcc-rs/issues/15) and submitted [a patch](https://github.com/penberg/mvcc-rs/pull/16).
- I finally slept like a baby.
- Tx Commit.

I am some rando on the internet and wasn't expecting any response. It was heartwarming to see that people were willing to take the time to help me. 

A little kindness goes a long way.

## Typo

[WIP]I have written another blog post here so search engines can pick up and help someone in the future.