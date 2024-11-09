---
title: "PSA: Most databases do not do checksums"
date: "2024-11-09T21:11:18+05:30"
categories: ["database", ""]
tags: ["checksum", "bit rot", "database", "corruption"]
slug: "databases-checksum"
summary: "Most databases don't do checksums by default. Disk corruptions go silently unnoticed."
---

<small>This is a follow up to my post: [PSA: SQLite does not do checksums](https://avi.im/blag/2024/sqlite-bit-flip/)</small>

My friend, who claims to be a bigger fan of SQLite than me (debatable), said that my previous [blog post](https://avi.im/blag/2024/sqlite-bit-flip/) was unfair. He's right in a way. So here's a follow-up: most databases don't have checksums enabled by default. As explained earlier, even a single bit flip can be devastating, and your database or application won't even know about it. Alice would have lost money even on Postgres.

I thought I would make a list of databases which don't have checksums, but it turns out it's easier to make a list of databases which enable it by default. Postgres, MySQL, and many others don't have checksums by default!

So, here's a short list of databases that do enable checksums by default:

- TigerBeetle
- FoundationDB
- Oracle (I have no idea which version, check the documentation)
- MongoDB
- ClickHouse

Did I miss any? [Let me know](https://x.com/iavins/status/1855256734400663597).

## Reading

- TigerBeetle's [safety page](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/about/safety.md) is a great read on this topic.
- Redundancy Does Not Imply Fault Tolerance: Analysis of Distributed Storage Reactions to Single Errors and Corruptions - [link](https://www.usenix.org/conference/fast17/technical-sessions/presentation/ganesan)
