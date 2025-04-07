---
title: "Daily Log"
date: "2022-01-28T22:09:25+05:30"
categories: ["", ""]
tags: ["", ""]
slug: "daily-log"
summary: ""
---

## 22th Jan

MMAP is bad: http://cidrdb.org/cidr2022/program.html

## 23th Jan

how pyroscope makes use of Segment trees: https://news.ycombinator.com/item?id=26145944

Is it possible to build such a tree for disk?

Dynamo DB 10 years: https://news.ycombinator.com/item?id=30007530

## 24th Jan

Roblox Outage: https://news.ycombinator.com/item?id=30013919

The freelist issue of Bolt DB. It maintained a array (hard to serialize to disk, so it was writing 7mb at every write)

## 25th Jan

Geo Sharding https://medium.com/tinder-engineering/geosharded-recommendations-part-1-sharding-approach-d5d54e0ec77a and https://medium.com/tinder-engineering/geosharded-recommendations-part-2-architecture-3396a8a7efb

Taming of B Trees: https://www.scylladb.com/2021/11/23/the-taming-of-the-b-trees/


## 26th Jan

Internals of Postgres: https://www.interdb.jp/pg/index.html (comments have chapters to read: https://news.ycombinator.com/item?id=30086374)

Postgres indexes;: https://news.ycombinator.com/item?id=30001964

### 27th Jan 

https://twitter.com/justinjaffray/status/1485674927541817346?s=21

Learnt a nicce thing about OS writes: http://justinjaffray.com/durability-and-redo-logging/

I am just surprised that kernel still keeps the buffer even after process is exited. more over, that buffer can be resynced later when the process comes back up 🤯

how Redis does not expire keys: https://news.ycombinator.com/item?id=30099572

### 28th Jan

- Scaling Redis - https://www.youtube.com/watch?v=55TFuBMFWns TLDR: Redis Cluster and some tips on Redis can make 1M QPS under 1ms
- https://blog.twitter.com/engineering/en_us/topics/infrastructure/2019/improving-key-expiration-in-redis
- https://news.ycombinator.com/item?id=19662501 -- why radix tree?