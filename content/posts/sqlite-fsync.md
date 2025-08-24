---
title: "SQLite (with WAL) doesn't do `fsync` on each commit under default settings"
date: "2025-08-24T20:46:20+05:30"
categories: ["database", "sqlite"]
tags: ["sqlite", "checksum", "bit rot", "database", "corruption", "torn writes", "atomicity", "fsync"]
slug: "sqlite-fsync"
summary: "SQLite when used with WAL doesn't do fsync unless specified."
---

**edit**: the title is incorrect, may be applies to macOS or specific compilations. Check the update below.

SQLite has a WAL mode (the default is journal mode), but you're likely using it if you want higher write throughput. SQLite also has a PRAGMA called `synchronous` which configures how `fsync` is called. The default is `NORMAL`. This is what the docs say:

> [..] but WAL mode does lose durability. A transaction committed in WAL mode with `synchronous=NORMAL` might roll back following a power loss or system crash.

> In WAL mode when synchronous is `NORMAL (1)`, the WAL file is synchronized before each checkpoint and the database file is synchronized after each completed checkpoint and the WAL file header is synchronized when a WAL file begins to be reused after a checkpoint, but no sync operations occur during most transactions.

> If durability is not a concern, then synchronous=NORMAL is normally all one needs in WAL mode.

If you want `fsync` to be called on each commit, use `FULL`:

> With `synchronous=FULL` in WAL mode, an additional sync operation of the WAL file happens after each transaction commit. The extra WAL sync following each transaction helps ensure that transactions are durable across a power loss. Transactions are consistent with or without the extra syncs provided by `synchronous=FULL`.

https://www.sqlite.org/pragma.html#pragma_synchronous

### **update**:

I was wrong about this one! It seems the default SQLite3 on macOS behaves like this:

```
$ sqlite3 test.db

SQLite version 3.43.2 2023-10-10 13:08:14
Enter ".help" for usage hints.
sqlite> PRAGMA journal_mode=wal;
wal
sqlite> PRAGMA synchronous;
1
sqlite>
```

but a fresh copy from homebrew behaved differently:

```
$ /opt/homebrew/opt/sqlite/bin/sqlite3 test.db

SQLite version 3.50.4 2025-07-30 19:33:53
Enter ".help" for usage hints.
sqlite> PRAGMA journal_mode=wal;
wal
sqlite> PRAGMA synchronous;
2
sqlite>
```

Furthermore, as pointed out by charleslmunger on HN, the compile time options do set it to `FULL`:

> `SQLITE_DEFAULT_SYNCHRONOUS=<0-3>` This macro determines the default value of the PRAGMA synchronous setting. If not overridden at compile-time, the default setting is 2 (FULL).

> `SQLITE_DEFAULT_WAL_SYNCHRONOUS=<0-3>` This macro determines the default value of the PRAGMA synchronous setting for database files that open in WAL mode. If not overridden at compile-time, this value is the same as `SQLITE_DEFAULT_SYNCHRONOUS`.

https://sqlite.org/compile.html#default_synchronous

---

<small>Someone passed me this post [SurrealDB is sacrificing data durability to make benchmarks look better](https://blog.cf8.gg/surrealdbs-ch/) and asked me how SQLite works.</small>
