---
title: "Galloping Search"
date: "2024-12-07T16:41:34+05:30"
categories: ["algorithms"]
tags: ["distributed systems", "search", "algorithms", "zero disk", "diskless", "wal", "log"]
slug: "galloping-search"
summary: "I recently learned Galloping Search while building a distributed log s3-log. It's used to search sorted items when the upper bound is unknown. It's like binary search but without the 'high' value. In this short post, I will share my notes on it"
---

I recently learned about an algorithm called Galloping Search. It's used to search sorted items when the upper bound is unknown. It's like binary search but without the 'high' value. In this short post, I'll explain my problem and how I solved it.

I am building a [distributed log over S3](https://avi.im/blag/2024/s3-log). In a bucket or directory, I continuously add files named with sequential integers:

<img src="/blag/images/2024/s3-bucket.svg" alt="s3 bucket" style="width: 80%;"/>

The writer keeps a counter in memory. On each insert request, the writer increments the counter, assigning a unique sequential number to the new object. There are no gaps. If the machine crashes, I need a way to locate the last inserted object—the one with the highest number.

S3's limitations make this challenging:

- S3 has no API to fetch the last inserted item.
- The LIST API doesn't support sorting; it always returns results in lexicographical order.
- I don't want to scan the entire bucket of hundreds of thousands of items because the S3 LIST API is expensive (it costs the same as a PUT!).

### Solution

Here’s what I came up with: I search for objects at exponential intervals (1,000th, 10k, 50k, 100k) in parallel. When I find a gap (e.g., 100k missing but 50k exists), I binary search that range (e.g., 60k, 75k, 90k) until I narrow it to a manageable gap (5–10k objects). Then I use S3's LIST API to fetch objects from that point.

<img src="/blag/images/2024/galloping-search.svg" alt="galloping search"/>

Turns out this is called [Exponential Search (or Galloping Search)](https://en.wikipedia.org/wiki/Exponential_search):

> Exponential search allows for searching through a sorted, unbounded list for a specified input value (the search "key"). The algorithm consists of two stages. The first stage determines a range in which the search key would reside if it were in the list. In the second stage, a binary search is performed on this range.

When I posted [this online](https://x.com/iavins/status/1863205355443953930), there were lots of questions, and many people offered alternative solutions to find the largest number:

- The most common (and boring) answer was to keep a counter in a local file or SQLite database. This doesn’t work because it’s not helpful if my machine crashes and I need to recover from S3.
- Use DynamoDB, Redis, or another database: This works but also kinda sucks because I don't want to add another dependency to my library. It’s better if everything is self-contained in S3.
- Store a counter in S3 and update it at every write: This adds write amplification, and S3 PUT costs are expensive. I’d essentially pay twice for each write!
- Use ULID/UUID/Timestamps: This doesn’t work because I would lose point lookups. I want numbers to be sequential.

### Alternate Solutions

- Inverse Sequencing: Store a counter starting from the maximum value (`u64::max`) and decrement it with each insert. The S3 LIST API is lexicographical, so you always get the last inserted filename with a single list call. I am split on this solution as I find it cognitively taxing.

- [Partitioning and Hierarchical Search](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html): Store objects with partitioning using a delimiter like `000/042/001`. When you partition, the LIST API returns only the top hierarchy results (if you pass the delimiter `/` in the search request). For 100,000,000 (100M) files, it only takes 3 requests to find the largest number since the LIST API can return up to 1,000 items. For comparison, it is 50+ calls even when I use Galloping Search.

### What I’m Doing

1. At every 10k or 50k writes, I write the current count in a file called `.metadata`. This reduces both cost and write amplification. I call this the checkpointing operation.
2. While searching, I start from the counter in the `.metadata` file. Then I perform the Galloping Search. Even if the metadata file doesn’t exist, the approach still works.

After checkpointing, gaps may exist in the files preceding the last checkpointed number, but this does not impact its effectiveness. For now, I’m happy with the approach, though I may move to checkpointing + partitioning in the future.

---

<small>1. Thanks to folks @0xriggler and @JustinWaugh on X (formerly known as Twitter) for telling me about partitioning search.</small><br>
<small>2. The [s3-log project](https://github.com/avinassh/s3-log) is open source.</small><br>
<small>3. I use S3's conditional write to "append" and add a new object with the next sequence number.</small><br>
<small>4. Having gaps in the log can be catastrophic. A writer may add a new object at the gap and return success to the client 💀</small><br>