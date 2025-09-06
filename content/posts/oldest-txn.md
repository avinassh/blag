---
title: "Oldest recorded transaction"
date: "2025-09-05T13:13:34+05:30"
categories: ["database", "transaction"]
tags: ["database", "transaction", "tablet", "rocks db"]
slug: "oldest-txn"
summary: "The oldest recorded transaction was in 3100 BC"
---

The other day I posted a [tweet](https://x.com/iavins/status/1963597448321855793) with this image which I thought was funny:

<img src="/blag/images/2025/oldest-txn.png" alt="tablet from Sumer" style="width: 80%;"/>

*This is the oldest transaction database from 3100 BC - recording accounts of malt and barley groats. Considering this thing survived 5000 years (holy shit!) with zero downtime and has stronger durability guarantees than most databases today.*

*I call it rock solid durability.*

This got me thinking, can I insert this date in today's database? What is the oldest timestamp a database can support?

So I checked the top three databases: [MySQL](https://dev.mysql.com/doc/refman/8.4/en/datetime.html), [Postgres](https://www.postgresql.org/docs/17/datatype-datetime.html), and [SQLite](https://sqlite.org/lang_datefunc.html):

|   |   |
|---|---|
| MySQL  | 1000 AD  |
| Postgres  | 4713 BC |
| SQLite  | 4713 BC |

<br>Too bad you cannot use MySQL for this. Postgres and SQLite support the Julian calendar and the lowest date is Jan 01, 4713 BC:

```sql
sales=# INSERT INTO orders VALUES ('4713-01-01 BC'::date);
INSERT 0 1
sales=# SELECT * FROM orders;
   timestamp
---------------
 4713-01-01 BC
(1 row)
sales=# INSERT INTO orders VALUES ('4714-01-01 BC'::date);
ERROR:  date out of range: "4714-01-01 BC"
```

I wonder how people store dates older than this. Maybe if I'm a British Museum manager, and I want to keep ~theft~ inventory details. How do I do it? As an epoch? Store it as text? Use some custom system? How do I get it to support all the custom operations that a typical `TIMESTAMP` supports?

<small><i>Thanks to aku, happy_shady and Mr. Bhat for reading an early draft of this post.</i></small>

---
<small>1. Source of the image: [Sumer  civilization](https://en.wikipedia.org/wiki/Sumer#Language_and_writing)</small><br>
<small>2. I found this from the talk *1000x: The Power of an Interface for Performance* by
Joran Dirk Greef, CEO of TigerBeetle, [timestamped @ 38:10](https://www.youtube.com/watch?v=yKgfk8lTQuE&t=2290s).</small><br>
<small>3. The talk has other bangers too, [like this](https://x.com/iavins/status/1962568729671414266) or [this](https://x.com/iavins/status/1962568011728199836).</small>
