---
title: "Replacing a cache service with a database"
date: "2025-08-31T19:30:10+05:30"
categories: ["database", ""]
tags: ["database", "cache", "redis", "valkey", "libsql", "sqlite", "noria", "readyset", "ivm"]
slug: "db-cache"
summary: "Why do we use caches at all? Can databases fully replace them?"
---

I’ve been thinking about this: will we ever replace caches entirely with databases? In this post I will share some ideas and how we are moving towards it. tl;dr we are still not there, yet.

## Why do we even use caches?

<img src="/blag/images/2025/cache-pattern.svg" alt="typical cache service" style="width: 60%;"/>

Caches solve one important problem: providing pre-computed data at insanely low latencies, compared to databases. I am talking about typical use cases where we use a cache along with the db ([cache aside pattern](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html#cache-aside-lazy-loading)), where the application always talks with cache and database, tries to keep the cache up to date with the db. There are other patterns where cache itself talks with DBs, but I think this is the more common pattern where application talks to both cache and database.

I'd like to keep my systems simple, and try to reduce dependencies, if possible. If databases can provide the same benefits as cache, it can go a long way before we decide to add an external caching service.

Instead of using a cache, like Valkey (or Redis), you could just set up a read replica and use it like a cache. Databases already keep some data in-memory (in [buffer pool](https://www1.columbia.edu/sec/acis/db2/db2d0/db2d0122.htm)). Caches aren't expected to be strongly consistent with the DB, and neither are read replicas. As an added benefit, you can use the same SQL queries instead of whatever custom interface the cache provides. Not using a cache would make things operationally so much simpler; and I'd never have to worry about cache invalidation.

If you use an embedded database (like SQLite, PGLite) with replication (like Litestream or libSQL), you’d even get zero network latency.

However, caches are still very prominent and can't be replaced with just read replicas. I often think about how we can bridge the gap, but I think the workloads are so different that it's not going to happen anytime soon. The closest we've come, I think, is [Noria + MySQL](https://github.com/mit-pdos/noria) (now ReadySet).

So why are caches still preferred? Comparatively, here are a few things caches do better than databases:

1. Setting up and destroying a cache is cheap; both operationally and cost-wise.

2. Most workloads only cache a subset of the data, and developers have control over what that subset is. It uses fewer resources. With a DB + buffer pool, that level of control doesn't exist today.

3. Caches keep pre-computed data. I could do a complex join and then save the results in a cache. How could I achieve the same with a db?

4. I don't know of any database that lets me assign priority to specific rows to always keep them in the buffer pool. Caches also provide eviction policies (and TTL), which I can't do with the DB buffer pool.

5. Databases are orders of magnitude larger than caches. Using a full read replica that consumes terabytes of storage just to access a few gigabytes of hot data feels wasteful. Some cloud providers won't even let you use larger SSDs without also upgrading CPU/memory.

6. Cache services can handle hundreds of thousands of concurrent connections, whereas databases generally don’t scale that way. Database connections are expensive.

## Cache → Database

What needs to happen to close the gap?

1. Since I'm only interested in a subset of the data, setting up a full read replica feels like overkill. It would be great to have a read replica with just partial data.

2. I don't know of any database built to handle hundreds of thousands of read replicas constantly pulling data. Would they even behave sanely if I kept plugging in new replicas as if they were caches? Interestingly, with databases that use disaggregated storage, replicas could pull directly from storage without ever contacting the master.

3. [IVM (Incremental View Maintenance)](https://wiki.postgresql.org/wiki/Incremental_View_Maintenance) is the hot new stuff. They can be used to precompute the results to cache. e.g. [Noria](https://jon.thesquareplanet.com/papers/osdi18-noria.pdf) saves results of a join query. So we also need some fancy data structures rather than a simple buffer pool. I’d also love to use WASM extensions to aid in pre computation. The trick is making this work without paying the full cost of query planning. And note: pre-computation does not really help if you have multiple data sources.

4. Most mainstream databases don't let me fetch just the subset I care about. If IVM were easier, and we could combine it with partial read replicas, maybe then a replica could truly replace a cache*.

If we look at this from another angle, we could use an IVM engine to populate and update an external cache service; but that might be a topic for another day.

<small><i>Thanks to Gowtham for reading a draft of this.</i></small>

---

<small>1. This blog is a [rehash of a tweet](https://x.com/iavins/status/1944416630727159874) I wrote earlier, which itself was a rehash of a [reply](https://x.com/iavins/status/1944034504886431974) I made to [Phil Eaton's tweet](https://x.com/eatonphil/status/1943423886554497427). FWIW, my fren thinks [the tweet](https://x.com/iavins/status/1944416630727159874) was better than this post.</small><br>
<small>2. This of course does not fit all the use cases, majority of them yes</small><br>
<small>3. Weirdly, there’s no Wikipedia page for 'buffer pool'. btw, Andy Pavlo has a killer [lecture video](https://www.youtube.com/watch?v=BS5h8QZHCPk) on them.</small><br>
<small>4. Many new companies doing some insane stuff around IVM: ReadySet, Materialize, and Feldera</small><br>
<small>5. If you are new to IVM / Materialized views, then Sophie Alpert has an excellent post on the topic [Materialized views are obviously useful](https://sophiebits.com/2025/08/22/materialized-views-are-obviously-useful).</small><br><br>
<small>*at least for my use cases</small><br>
