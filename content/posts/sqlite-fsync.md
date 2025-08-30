---
title: "SQLite commits are not durable under default settings"
date: "2025-08-24T20:46:20+05:30"
categories: ["database", "sqlite"]
tags: ["sqlite", "checksum", "bit rot", "database", "corruption", "torn writes", "atomicity", "fsync"]
slug: "sqlite-fsync"
summary: "SQLite doesn't do fsync unless specified."
---

Previously, I claimed that transactions in SQLite with WAL are not durable under default settings. Turns out, I was only half wrong but technically correct; the issue is actually with SQLite in rollback journal mode (the default). This post is now amended with the changes.

Here's what I mean by durability: when the database acknowledges that a transaction is committed, it's 'durably' saved to disk. That is, neither an application crash nor an OS crash should make that transaction disappear. Imagine you make a new commit, the db acknowledges success, and suddenly your OS reboots. Do you expect your transaction changes to be persisted? For example, in Postgres you can expect your changes to be there. This is how most OLTP databases behave.

## SQLite Journal Mode

Under the default settings, SQLite operates in rollback journal mode. SQLite also has a PRAGMA called `synchronous` which configures how `fsync` is called. The synchronous setting has many modes: `OFF`, `NORMAL`, `FULL`, `EXTRA`. The default is set to `FULL`:

```
$ sqlite3 test.db

SQLite version 3.50.4 2025-07-30 19:33:53
Enter ".help" for usage hints.
sqlite> PRAGMA journal_mode;
delete
sqlite> PRAGMA synchronous;
2
```

Unfortunately, in journal mode, `FULL` isn't enough to make transactions durable. Here's what the documentation states:

> **EXTRA (3)**
> EXTRA synchronous is like FULL with the addition that the directory containing a rollback journal is synced after that journal is unlinked to commit a transaction in DELETE mode. **EXTRA provides additional durability if the commit is followed closely by a power loss.**

> **FULL (2)**
> When synchronous is FULL (2), the SQLite database engine will use the xSync method of the VFS to ensure that all content is safely written to the disk surface prior to continuing. This ensures that an operating system crash or power failure will not corrupt the database.

Notice that it says `FULL` ensures that the database isn't corrupted, but NOT that the last transaction is durable. The highlighted part in `EXTRA` provides that durability.

## SQLite with WAL

SQLite also has a WAL mode, and you're likely using it if you want higher write throughput. The `synchronous` PRAGMA also applies to WAL. The default is `FULL`:

> With `synchronous=FULL` in WAL mode, an additional sync operation of the WAL file happens after each transaction commit. The extra WAL sync following each transaction helps ensure that transactions are durable across a power loss. Transactions are consistent with or without the extra syncs provided by `synchronous=FULL`.

However, `NORMAL` seems misnamed, as it doesn't seem normal to me:

> [..] but WAL mode does lose durability. A transaction committed in WAL mode with `synchronous=NORMAL` might roll back following a power loss or system crash.

> In WAL mode when synchronous is `NORMAL (1)`, the WAL file is synchronized before each checkpoint and the database file is synchronized after each completed checkpoint and the WAL file header is synchronized when a WAL file begins to be reused after a checkpoint, but no sync operations occur during most transactions.

> If durability is not a concern, then synchronous=NORMAL is normally all one needs in WAL mode.

So, if you're using WAL, stick with `FULL`. If durability isn't a concern, then `NORMAL` may be preferred for higher performance. While this is what the documentation says, [DRH, the creator of SQLite, said the following](https://news.ycombinator.com/item?id=45014296) which contradicts the documentation:

> If you switch to WAL mode, the default behavior is that transactions are durable across application crashes (or SIGKILL or similar) but are not necessarily durable across OS crashes or power failures. Transactions are atomic across OS crashes and power failures. But if you commit a transaction in WAL mode and take a power loss shortly thereafter, the transaction might be rolled back after power is restored.

I'll leave it up to you to decide which is correct 🤷‍♂️

## SQLite on macOS

The situation on macOS is quite fucked up. The SQLite shipped with macOS has the following:

```
$ sqlite3 test.db

SQLite version 3.43.2 2023-10-10 13:08:14
Enter ".help" for usage hints.
sqlite> PRAGMA journal_mode=wal;
wal
sqlite> PRAGMA synchronous;
1
sqlite> PRAGMA fullfsync;
0
sqlite>
```

That is, the default is `NORMAL`. So, commits are not durable. But even if you use `FULL`, it's not enough. You'll want to [set `fullfsync`](https://www.sqlite.org/pragma.html#pragma_fullfsync) to true. This is false by default. Apparently, [Apple has purposely fucked up fsync](https://bonsaidb.io/blog/acid-on-apple/) and you always want to use `fullfsync`. This setting has no effect on non-macOS machines.

## Compile Time Options

SQLite decides all this config through compile-time defaults:

> `SQLITE_DEFAULT_SYNCHRONOUS=<0-3>` This macro determines the default value of the PRAGMA synchronous setting. If not overridden at compile-time, the default setting is 2 (FULL).

> `SQLITE_DEFAULT_WAL_SYNCHRONOUS=<0-3>` This macro determines the default value of the PRAGMA synchronous setting for database files that open in WAL mode. If not overridden at compile-time, this value is the same as `SQLITE_DEFAULT_SYNCHRONOUS`.

There's no compile-time option for fullfsync, so by default it's false.

So it's totally possible that your distribution might be shipping SQLite with default `synchronous` as `NORMAL`.

The lesson here should be that you should always check the setting and make sure it's what you want. Here's a small chart to help you set:

| Journal Mode | Synchronous | fullfsync |
|--------------|-------------|-----------|
| `DELETE` (rollback) | `EXTRA` | 1 |
| `WAL` | `FULL` | 1 |

---

<small>Thanks to all the people who commented and discussed the original version of this article on [Hacker News](https://news.ycombinator.com/item?id=45005071). Their comments helped me make this post better.</small>

<small>Someone passed me this post [SurrealDB is sacrificing data durability to make benchmarks look better](https://blog.cf8.gg/surrealdbs-ch/) and asked me how SQLite works.</small>
