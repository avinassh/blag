---
title: "Recurse Center Day 14: NoSQL Transactions"
date: "2021-11-19T20:15:44+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-14"
summary: "I learned how using MongoDB was fatal for a startup"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## Transactions in NoSQL

I was researching about transactions, watched [this lecture](https://www.youtube.com/watch?v=mYFo1aE47xE) on concurrency, learned a couple of fascinating things:

1. I haven't found any supporting articles online, but [in the lecture](https://youtu.be/mYFo1aE47xE?t=1378), Andy humour about the ACID acronym. One, the creator of ACID added `C` deliberately to make it "ACID", even though it doesn't fit. Secondly, his wife didn't like candies, and she was a bitter woman, so he named ACID after her!

2. Database transaction properties are quite crucial when it involves anything related to money. Some bitcoin exchange was using MongoDB (Mongo did not have transactions at that time), so some hacker drained out money from everyone's account, which wiped the exchange in a single day! [What a crazy story](https://youtu.be/mYFo1aE47xE?t=3421). I found some articles on this: [1](https://hackingdistributed.com/2014/04/06/another-one-bites-the-dust-flexcoin), [2](https://www.infoq.com/news/2014/04/bitcoin-banking-mongodb/)

> On March 2, 2014 Flexcoin lost all its bitcoins due to a code flaw. The attacker issued thousands of concurrent requests ordering transfers from one of his accounts to another. He then repeated the operation with other accounts until all bitcoins were withdrawn. This was possible because the code was not written to deal with multiple concurrent requests, and all the transfers happened before the balances were updated. If a balance is not updated in time, a new request could be granted even if the account normally is empty. As a result, Flexcoin shut down operations after losing 896 BTC valued at about half a million dollars.

# People

I had a coffee chat with Sydney, who is a faculty at RC. She was in the office when our call happened, and I got a virtual real tour of RC space (or real virtual tour? :P)
