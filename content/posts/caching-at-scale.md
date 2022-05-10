---
title: "Caching at Scale"
date: "2022-04-01T18:07:48+05:30"
categories: ["", ""]
tags: ["", ""]
slug: "caching-at-scale"
summary: "How do big tech do caching at scale? How Facebook has built a caching infra which can handle billions of queries per second?"
---

I am gonna skip the basics of caching:
- Why cache?
- How to cache, the gotchas, cache invalidation
- The best practices

## Single Cluster

- Get: 