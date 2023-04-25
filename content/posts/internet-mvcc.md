---
title: "Internet is wholesome: MVCC edition"
date: "2023-04-20T22:19:15+05:30"
categories: ["database", ""]
tags: ["database", "hekaton", "typo", "mvcc"]
slug: "internet-mvcc"
summary: "This is a short story about how I hit a wall while implementing a database research paper, found a publication error and how people on the internet helped me."
---

This is a short story about how I hit a wall while implementing a database research paper, found a publication error and how people on the internet helped me. 

The paper is Hekaton MVCC - [High-Performance Concurrency Control Mechanisms for Main-Memory Databases](https://vldb.org/pvldb/vol5/p298_per-akelarson_vldb2012.pdf). Scroll down to the bottom if you are interested in knowing the errata.

## Timeline

- `$whoami` I am a backend developer, and databases excite me! I dream of being a database developer one day. I have an educational side project called [CaskDB](https://github.com/avinassh/py-caskdb) which aims to teach how to build a key-value store. I always look forward to adding new database features, as it allows me to learn new things. 
- [Apr 7] Pekka Enberg [tweeted](https://twitter.com/penberg/status/1644221651293204480) about the Hekaton MVCC paper. This research paper was new to me, and I found it approachable. CaskDB does not have transactions yet, so this gave me a great learning opportunity to implement it.
- [Apr 8] Pekka started implementing the paper in Rust and [tweeted](https://twitter.com/penberg/status/1644676555942109185) about it. It became easy for me to follow the paper with the code. I also started working on my [Go implementation](https://github.com/avinassh/mvcc-go).
- I am a massive fan of Andy and have watched the videos from his course [CMU Advanced Database Systems](https://15721.courses.cs.cmu.edu/spring2023/). I started rewatching the [Hekaton lectures](https://www.youtube.com/watch?v=9EY0vYFNWxY). The lecture series is excellent; go check it out!
- Reading the paper was straightforward, but when I began thinking about code, I noticed gaps in my understanding. Code is fun; that's when you see the unexpected challenges and nuances.
- [Apr 9] I started working through the paper's `Version Visibility` section. This part explains an ongoing transaction's effect on a row's visibility. It addresses the questions like transaction `tx1` updated a row; can `tx2` see it? Some of the ideas around row visibility didn't make sense.
- I went back to the paper and reread it several times now. I thought maybe I had missed something from the earlier sections. I took a pencil and paper and started drawing all possible flows. I did it multiple times, but in vain.
- For a moment, I started wondering if the paper could have errors. But this is a famous paper, and I couldn't find any errata online. I was uncertain whether I had misunderstood the paper or if it was flawed.
- I started asking in Slack / Discord / Zulip groups. People were helpful, but the answers were related to general MVCC, not particular to the Hekaton MVCC. I explained the paper to one of my friends and asked if he saw any issues. Nothing helped!
![](/blag/images/2023/hekaton-rc.png)
- [Apr 12] I emailed one of the authors, Professor Spyros Blanas, with zero hopes of hearing anything back.
- [Apr 13] I woke up to the Professor's reply, and they acknowledged that there was indeed a typo in the paper! What a blissful morning! Not only was he kind enough to reply, but he also gave me a high-level idea of how things should be.
- From one of the groups, [Alex Miller](https://transactional.blog) saw my message. It turns out he is friends with another author Cristian, and they discussed my issue. He agreed that one of the tables needed to be corrected. My morning just got better!
- I was surprised to learn even popular research papers can have typos.
- [Apr 14] I discussed the issue with Pekka. I filed [an issue](https://github.com/penberg/mvcc-rs/issues/15) and submitted [a patch](https://github.com/penberg/mvcc-rs/pull/16).
- Tx Commit.

I was humbled by the responses I received, given that I didn't expect much as just some random person on the internet. It was heartwarming to see that people were willing to take the time to help me out.

A little kindness goes a long way.

## Errata

I have written another detailed blog post [here]({{< ref "posts/hekaton-paper-typo" >}}) so search engines can pick up and help someone in the future. The paper contains two tables, which decide the row visibility during a transaction. One of the tables, `Table 2`, has a typo:

![](/blag/images/2023/hekaton-table-2.png)

According to the above rules, a committed row becomes invisible for new transactions. The fix is simple, the entire column should read:


> V is visible only if TE is not T


Check the [errata]({{< ref "posts/hekaton-paper-typo" >}}) blog post to read the error's implications and the fix in detail.

Have comments? Share your thoughts here on [the Twitter thread](https://twitter.com/iavins/status/1650890780121399296).

<small><i>Thanks to Bhargav, Hari, Satan, Saad, Sumesh, Piyush, and Gautam for reading a draft of this.</i></small>