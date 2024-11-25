---
title: "Zero Disk Architecture"
date: "2024-11-24T17:20:31+05:30"
categories: ["distributed systems"]
tags: ["database", "distributed systems", "infrastructure", "disaggregated storage", "zero disk", "diskless"]
slug: "zero-disk-architecture"
summary: "State is pain. The next generation of infrastructure tools will be built on diskless paradigm. In this short post I will explain what is Diskless / Zero Disk Architecture"
---

<small>This is a follow up to my post: [Disaggregated Storage - a brief introduction](https://avi.im/blag/2024/disaggregated-storage/)</small>

## State is pain

In my [previous post](https://avi.im/blag/2024/disaggregated-storage/), I explained how a disk attached to a machine makes things difficult. Vertical scaling has its limits, and when you hit that limit, you can't do horizontal scaling right away because of the attached disk. Mainstream databases like Postgres or MySQL don't scale horizontally. I recently learned that BlueSky team switched from Postgres to a combination of Scylla and SQLite. One of the reasons was because (vanilla) Postgres is not horizontally scalable, but Scylla is.

State is pain. Since the machine is stateful, you lose elasticity and scalability. So, the solution was to separate state from compute, so that they become independently scalable.

## Disaggregated Storage

Disaggregated Storage solves many problems associated with the traditional coupled architecture:

- Scalable and elastic. Limits of vertical scaling do not apply
- Databases are 'serverless' - instant startup and shutdown
- Instant failover without any need of a hot standby 

But there was a big cliffhanger at the end of the post. The storage server. If I am writing a storage server, then won't I need to manage the state? It looks like we are back where we started. We need a storage server which is strongly consistent, elastic, horizontally scalable, and preferably has auto sharding.

So...what are my options? 

1. In large companies, you can offload the storage server problem to another team and live peacefully. For example, Amazon has a transaction log service (the details aren't public) which is used by Aurora and MemoryKV.

2. Use an existing open source storage engine. For Disaggregated Storage on SQLite, I went with this route and used Foundation DB. One problem with this approach is, you need to run and manage the cluster by yourself. I don't know any hosted KV Store providers.

3. Become a cracked engineer and build my own storage server. But this will take years! We want to ship fast and ship yesterday, so not an option.

It seems most database companies roll their own storage server. However, there is one more option which is a mix of #1 and #2: Amazon S3.

## Zero Disk Architecture

<img src="/blag/images/2024/zero-disk-arch.svg" alt="zero disk architecture" style="width: 80%;"/>

The idea is simple. Instead of writing to a storage server, we will write to S3. Thus we will not manage any storage server, rather we offload it to the smart folks at AWS. S3 meets all our requirements. As a bonus, you get infinite storage space. S3 came out in 2006 and it has proven test of time. It is designed to provide [99.999999999% (that's eleven nines) durability](https://x.com/iavins/status/1860621569355030696) and 99.99% availability guarantees. I believe the next generation of infrastructure systems will be built on zero disk paradigm.

This idea is not new. In 2008, there was a research paper ['Building a Database on S3'](https://people.csail.mit.edu/kraska/pub/sigmod08-s3.pdf) - a paper way ahead of its time, with lots of interesting ideas for today's cloud computing. The researchers experimented with storing a B-tree on S3 using SQS as a Write-Ahead Log (WAL). They also provided analysis on latency when writing to S3 and the associated costs. The paper had some flaws, like they dropped ACID properties. However, we are in 2025, and we can do better.

Then, why has no one built such a system until now? My guess: latency and cost. However, S3 keeps getting better. They keep reducing the price all the time. The cost and latency are both going down as technology improves! Amazon S3 Express One Zone was launched last year and it's supposed to be 10x faster. Another reason I think is B-Tree vs LSM Tree. LSM Tree workload is more suited for S3. As most newer databases adapt to LSM, they're closer to S3. In the paper also they map B-Tree on S3.

Another reason I suspect is lack of features like conditional writes. Without this, you need an external system to provide transactional and ACID properties. S3 recently added this which gives you CAS-style operations on S3 objects.

Databases typically operate with pages, which are 4KiB in size. But object storages operate at much bigger sizes. The cost will be insanely high if we write every 4KiB object. So we will batch them at the compute layer till say 512KiB and then write all the pages as a single object. Suppose a transaction has sent a commit request, when do you acknowledge it as committed? If the local batch is not full, then do you make the client wait or cache the writes at compute and return success? If you do the latter, there is a risk of data loss. If you wait, then latency shoots up. Like everything in engineering, there is a trade-off: latency vs durability.

Smaller payloads also mean more requests, but that increases both cost and provides better durability and latency. This adds one more parameter: cost vs latency vs durability.

<img src="/blag/images/2024/latency-cost-durability.svg" alt="latency cost durability trade off" style="width: 80%;"/>

I stole this trade-off diagram from [Jack Vanlightly's excellent article](https://jack-vanlightly.com/blog/2023/11/29/s3-express-one-zone-not-quite-what-i-hoped-for). Chris Riccomini also [explored](https://materializedview.io/p/cloud-storage-triad-latency-cost-durability) this concept and coined catchy 'LCD model' term.

<img src="/blag/images/2024/s3-express-cache.svg" alt="s3 express as a cache"/>

If you want to optimize for latency, you can first write to S3 Express One Zone (supposedly has single digit millisecond latency) and then offload that data to S3 later. In this case, One Zone becomes an intermediate cache server.

<img src="/blag/images/2024/raft-cache.svg" alt="raft cluster as a cache"/>

For OLTP databases, this can be still slow. That's why databases like [Neon](https://neon.tech/blog/architecture-decisions-in-neon), [TiDB](https://aws.amazon.com/blogs/storage/how-pingcap-transformed-tidb-into-a-serverless-dbaas-using-amazon-s3-and-amazon-ebs) etc. have a Raft cluster setup which receives the writes. Then they are written to S3. This also saves on cost because instead of many smaller writes, you can make one large write to S3.

So depending on the trade-offs you want to make, you can write directly to S3 (standard or Express One Zone) or use a write through cache server. Zero disk architecture is also very attractive for systems where you don't care about latency. For example, OLAP databases, data warehouse systems.

Here are some systems which use S3 (or similar) as a primary store: [Snowflake](https://event.cwi.nl/lsde/papers/p215-dageville-snowflake.pdf), [WarpStream](https://www.warpstream.com/blog/zero-disks-is-better-for-kafka), [SlateDB](https://slatedb.io/docs/architecture), [Turbo Puffer](https://turbopuffer.com/architecture), [Clickhouse](https://aws.amazon.com/blogs/storage/clickhouse-cloud-amazon-s3-express-one-zone-making-a-blazing-fast-analytical-database-even-faster/), [Quickwit](https://quickwit.io/docs/main-branch/overview/architecture), [Milvus](https://milvus.io/docs/architecture_overview.md).

Zero Disk Architeture is a very compelling because you are not managing any storage server. You are not managing the state. The problem is for AWS S3 to deal with now. On top of it, you get all the benefits of disaggregated storage I highlighted earlier. 

It's time we use the S3 as the brother Bezos intended. The malloc of the web.

---

<small>1. Any object store would work. But I like S3.</small><br>
<small>2. If any Amazon engineers would like to share more details about the Transaction Log, hit me up please.</small><br>
<small>3. Jack also wrote an excellent cost analysis: [A Cost Analysis of Replication vs S3 Express One Zone in Transactional Data Systems](https://jack-vanlightly.com/blog/2024/6/10/a-cost-analysis-of-replication-vs-s3-express-one-zone-in-transactional-data-systems)</small><br>
<small>4. In S3, if you store 100 billion objects, you *might* lose one in a year. To put it another way: if you store 10 million objects, you might lose one in 10,000 years. If a dinosaur had stored 1,000 objects, they may be still intact after 65 million years 🦖</small><br>

<small><i>Thanks to Mr. Bhat, and Rishi for reading an early draft of this post.</i></small>
