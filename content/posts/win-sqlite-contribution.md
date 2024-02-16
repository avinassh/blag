---
title: "Win: contribution to SQLite codebase"
date: "2024-02-16T08:45:29+05:30"
categories: ["open source", "oss"]
tags: ["sqlite", ""]
slug: "win-sqlite-contribution"
summary: "I got my patches accepted into SQLite codebase!"
---

Back in November, I was exploring Vector Search with [sqlite-vss](https://github.com/asg017/sqlite-vss) extension. On Turso, I couldn't get it [to work](https://github.com/tursodatabase/libsql/issues/865). I assumed it was a problem with the extension.

This week I investigated further using `git bisect` to find the [problematic commit](https://github.com/tursodatabase/libsql/commit/e56bdbd52168b0ec96930dac3e9a20523d0eb496). Surprisingly, it was a small, seemingly innocent change. My coworkers helped a great deal in understanding the bug, taught me C, and gave a short primer on gdb.

[My pull request](https://github.com/tursodatabase/libsql/pull/1027) is now merged!