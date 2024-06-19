---
title: "Why does SQLite (in production) have such a bad rep?"
date: "2024-06-19T20:00:09+05:30"
categories: ["database", "sqlite"]
tags: ["database", "sqlite", "wal", "litestream"]
slug: "sqlite-bad-rep"
summary: "My answer to a question online, why?"
---

Why?

- Most people see it from a web workload perspective. Typically, we use Client-Server databases like PostgreSQL. But, SQLite absolutely shines in many other cases like mobile or embedded devices.

- For a long time, SQLite did not allow concurrent writes along with readers. This was changed in the WAL mode, where you could have a writer with multiple readers.

- You still cannot have multiple concurrent writers. That immediately puts off people. Your workload might or might not need this.

- SQLite did not have a good backup and replication story. This was a major issue, but [Ben Johnson](https://x.com/benbjohnson) changed the entire scene with [Litestream](https://litestream.io/). I would say this was one of the most impactful contributions to SQLite ecosystem.

- Some ORMs / libraries come with terrible defaults. For example, not setting `PRAGMA busy_timeout`.

- Funny little story: I started learning programming with Django, and the docs straight up said SQLite isn't suitable for production. I had a wrong impression for a long time. Then I started using it for my own use cases and realized the trade-offs.

SQLite, like any other database, has its pros and cons. For the majority of applications and scales, it is perfect. You always have PostgreSQL for anything else.

TLDR: SQLite slaps. You will be fine.

---

<small>The original question, the title, asked by [Jason Leow](https://x.com/jasonleowsg/status/1803030457166270806) and my [xeet](https://x.com/iavins/status/1803429828768764016).</small><br>