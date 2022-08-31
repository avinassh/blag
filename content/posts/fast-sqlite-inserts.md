---
title: "Towards Inserting One Billion Rows in SQLite Under A Minute"
date: "2021-07-17T22:10:44+05:30"
categories: ["database"]
tags: ["database", "sqlite", "optimisation", "performance"]
slug: "fast-sqlite-inserts"
summary: "This is a chronicle of my experiment where I set out to insert 1B rows in SQLite"
---

**Current Best**: 100M rows inserts in 33 seconds. (you can check the [source code on Github](https://github.com/avinassh/fast-sqlite3-inserts))

---


Recently, I ran into a situation where I needed a test database with lots of rows and needed it fast. So I did what any programmer would do: wrote a Python script to generate the DB. Unfortunately, it was slow. Really slow. So I did what any programmer would do: went down the rabbit hole of learning more about SQLite, Python, and eventually Rust... in my quest to get a 1B row database under a minute. This blog post is a summary of this fun and educational exercise.


# Goal 

The goal of this experiment is to generate an SQLite database with one billion rows under a minute, on my machine, with the table having the following schema:

```sql
create table IF NOT EXISTS user
(
    id INTEGER not null primary key,
    area CHAR(6),
    age INTEGER not null,
    active INTEGER not null
);
```

The generated data would be random with following constraints: 
The `area` column would hold six digits area code (any six digits would do, no validation).
The `age` would be any of 5, 10, or 15. 
The `active` column is either 0 or 1.

The machine I am using is MacBook Pro, 2019 (2.4 GHz Quad Core i5, 8GB, 256GB SSD, Big Sur 11.1)

Aspects I was willing to compromise on were:

- I don't need the durability guarantee. That is, it is fine if the process crashes and all the data is lost. I could just run the script again.
- It may use my machine resources to the fullest: 100% CPU, 8GB Memory and gigabytes of SSD space.
- No need of using true random methods, pseudo-random methods from stdlib are just fine.

# Python Prototype

Python is my go to language for any kind of scripting. The standard library provides a nice SQLite module, using which I wrote my first version. Here is the [full code](https://github.com/avinassh/fast-sqlite3-inserts/blob/f26951ea/naive.py). In this script, I tried to insert 10M rows, one by one, in a for loop. This version took close to 15 minutes, sparked my curiosity and made me explore further to reduce the time.

In SQLite, each insertion is atomic and is a transaction. Each transaction guarantees that it is written to disk thus could be slow. I tried different sizes of batch inserts, found out 100,000 to be a sweet spot. With this simple change, the running time was reduced to 10 minutes. Here is the [full code](https://github.com/avinassh/fast-sqlite3-inserts/blob/f26951ea/naive_batched.py)


# SQLite Optimisations

The script I had written is very simple, so I assumed there isn't much room for optimisation. Secondly, I wanted the code to be simple and near to the daily usage version. The next logical step was to look for database optimisations and I started diving into the amazing world of SQLite. 

The internet is filled with many SQLite optimisation posts. Based on them, I made following changes:

```sql
PRAGMA journal_mode = OFF;
PRAGMA synchronous = 0;
PRAGMA cache_size = 1000000;
PRAGMA locking_mode = EXCLUSIVE;
PRAGMA temp_store = MEMORY;
```

What do these do?
- Turning off `journal_mode` will result in no rollback journal, thus we cannot go back if any of the transactions fail. This disables the atomic commit and rollback capabilities of SQLite. Do not use this in production.
- By turning off `synchronous`, SQLite does not care about writing to disk reliably and hands off that responsibility to the OS. A write to SQLite, may not mean it is flushed to the disk. Do not use this in production.
- The `cache_size` specifies how many memory pages SQLite is allowed to hold in the memory. Do not set this to a high value in production.
- In `EXCLUSIVE` locking mode, the lock held by the SQLite connection is never released.
- Setting `temp_store` to `MEMORY` will make it behave like an in-memory database.

The SQLite docs have a [full page dedicated on these parameters](https://www.sqlite.org/pragma.html), they also list a bunch of other parameters. I haven't tried all of them, the ones I selected provided a decent running time.

Here are some of the articles I read on the internet which helped me with these optimisation parameters: [1](https://remusao.github.io/posts/few-tips-sqlite-perf.html), [2](https://stackoverflow.com/Questions/364017/faster-bulk-inserts-in-sqlite3), [3](https://stackoverflow.com/questions/1711631/improve-insert-per-second-performance-of-sqlite), [4](https://github.com/the-lean-crate/criner/issues/1), [5](https://stackoverflow.com/questions/25427769/how-does-executemany-work).

# Python Revisited

I rewrote the Python script again, this time including the fine-tuned SQLite parameters which gave a huge boost and the running time was reduced drastically.

- The [naive for loop version](https://github.com/avinassh/fast-sqlite3-inserts/blob/3b9850a/sqlite3_opt.py) took about 10 minutes to insert 100M rows.
- The [batched version](https://github.com/avinassh/fast-sqlite3-inserts/blob/e126bd6/sqlite3_opt_batched.py) took about 8.5 minutes to insert 100M rows. 

# PyPy

I have never used PyPy and [PyPy homepage](https://www.pypy.org/) highlight that it is 4x faster than CPython, I felt this is a good opportunity to try it and test out their claims. I was also wondering if I had to make changes to make it run, however, my existing code ran smoothly. 

All I had to do was run my existing code, without any change, using PyPy. It worked and the speed bump was phenomenal. The batched version took only 2.5 minutes to insert 100M rows. I got close to 3.5x speed :)

(I am not affiliated with PyPy but I would request you [consider donating to PyPy](https://opencollective.com/pypy) for their efforts.)

# Busy Loop(?)

I wanted to get some idea of how much time Python is spending just in loops. So I removed the SQL instructions and ran [the code](https://github.com/avinassh/fast-sqlite3-inserts/blob/d27601a/busy_loop.py):

- The batched version took 5.5 minutes in CPython
- The batched version took 1.5 minutes in PyPy (again a 3.5x speed bump)

I [rewrote the same in Rust](https://github.com/avinassh/fast-sqlite3-inserts/blob/47fd81f/src/bin/busy.rs), the loop took only 17 seconds. I decided to move from Python and experiment further in Rust.

(Note: This is NOT a speed comparison post between Python and Rust. Both have very different goals and places in your toolkit.)


# Rust

Just like Python, I wrote a [naive Rust version](https://github.com/avinassh/fast-sqlite3-inserts/blob/bdda921/src/bin/basic.rs) where I inserted each row in a loop. However, I included all the SQLite optimisations. This version took about 3 minutes. Then I did further experiments:

- The previous version had used `rusqlite`, I [switched to](https://github.com/avinassh/fast-sqlite3-inserts/blob/ebce33f/src/bin/basic_async.rs) `sqlx` which runs asynchronously. This version took about 14 mins. I was expecting this degraded performance. But it is worth noting that it performed worse than any of the Python iterations I had come up with so far. 
- I was executing raw SQL statements, [switched to prepared statements](https://github.com/avinassh/fast-sqlite3-inserts/blob/cbe53fd/src/bin/basic_prep.rs) and inserted the rows in a loop, but reusing the prepared statement. This version took about only a minute.
- Also tried creating a [long string with an insert statement](https://github.com/avinassh/fast-sqlite3-inserts/blob/9cc1ea1/src/bin/basic_batched_wp.rs), I don't think this performed any better. The [repository](https://github.com/avinassh/fast-sqlite3-inserts) has few other versions as well.

# The (Current) Best Version

- I used prepared statements and inserted them in a batch of 50 rows. To insert 100M rows, took 34.3 seconds. [source code](https://github.com/avinassh/fast-sqlite3-inserts/blob/009694f/src/bin/basic_batched.rs)
- I created a threaded version, where I had one writer thread that received data from a channel and four other threads which pushed data to the channel. This is the current best version which took about 32.37 seconds. [source code](https://github.com/avinassh/fast-sqlite3-inserts/blob/bd8414f/src/bin/threaded_batched.rs)

# IO Time

Good folks at the SQLite forum gave me an interesting idea, measure the time it takes for in-memory DB. I ran the code again giving the DB location as `:memory:`, the rust version took two seconds less to complete (29 seconds). I guess it is fair to assume that it takes 2 seconds to flush 100M rows to disk. This also shows that there might not be any more SQLite optimisations possible to write to disk in a faster way, since 99% of time is being spent in generating and adding rows.

# Leaderboard

(\*at the time of writing. The repo has the upto date numbers)

| Variant           | Time             |
| ------------------| -----------------|
| Rust              | 33 seconds       |
| PyPy              | 150 seconds      |
| CPython           | 510 seconds      |

# Key Takeaways

- Make use of SQLite [PRAGMA statements](https://www.sqlite.org/pragma.html) when possible
- Use prepared statements
- Do a batched insertions
- PyPy is actually 4x faster than CPython
- Threads / async may not be faster always

# Further Ideas

Here are a few directions I plan to explore next to improve performance:

1. I haven't run the code through a profiler. It might give us hints about the slow parts and help us optimising the code further.
2. The second fastest version runs single threaded, on a single process. Since I have a four-core machine, I could launch 4 processes, get up to 800M rows under a minute. Then I would have to merge these in few seconds, so that the overall time taken is still less than a minute.
3. Write a go version with the garbage collector completely disabled.
4. It is entirely possible that rust compiler might have optimised the busy loop code and removed the allocations, calls to random functions since it had no side effects. Analysis of the generated binary might shed more light.
5. Here is a really crazy idea: learn about SQLite file format then generate the pages and write to disk directly. 

Looking forward to discussions and/or collaborations with curious souls in my quest to generate a billion record SQLite DB quickly. If this sounds interesting to you, reach out to me on [Twitter](https://twitter.com/iavins) or [submit a PR](https://github.com/avinassh/fast-sqlite3-inserts).

<small><i>Thanks to Bhargav, Rishi, Saad, Sumesh, Archana, and Aarush for reading a draft of this.</i></small><!--Also thanks to Mishraji, who promised to read-->

---

<small>1. Why? In [a telegram bot](https://github.com/avinassh/cowin-assist), I wrote, one of the SQL queries required a partial index. I have used partial indexes in Postgres/Mongo, but I was pleasantly surprised to know that SQLite also supported them. I decided to write a blog post (spoiler: which I never did), with numbers showing the effectiveness of partial indexes. I wrote a quick script and generated a DB, but the data was too small to show the power of partial indexes and queries were fast without them. The larger DB required more than 30 minutes to generate. So I spent 30+ hours to reduce the 30 mins of running time :p</small><br>
<small>2. If you liked this post, then you may like [my experiment with MongoDB](https://avi.im/blag/2021/mongo-dupes-in-unique-index/) where I inserted duplicate records in a collection with a unique index - [link](https://avi.im/blag/2021/mongo-dupes-in-unique-index/).</small><br>
<small>update (19, July): prefixed the title with 'towards' to make the intention more clear</small>

