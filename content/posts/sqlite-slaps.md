---
title: "SQLite Slaps"
date: "2024-06-18T14:50:02+05:30"
categories: ["database", "sqlite"]
tags: ["database", "sqlite", "wal", "testing"]
slug: "sqlite-slaps"
summary: "why SQLite is cracked"
---

Fun fact: SQLite is the most deployed and most used database. There are over one trillion (1000000000000 or a million million) SQLite databases in active use.

It is maintained by [three people](https://www.sqlite.org/crew.html). They don't allow [outside contributions](https://www.sqlite.org/copyright.html).

## It is everywhere

SQLite is likely used more than all other database engines combined. Billions and billions of copies of SQLite exist in the wild. SQLite is in:

- Every Mobile (Android, iOS, Windows) device
- Every Mac or Windows10 machine
- Every Web browser
- Every instance of Skype, iTunes, and Dropbox client
- PHP and Python
- Most TV, set-top cable boxes and automotive multimedia systems
- Countless millions of other applications

## How do they cook?

There are over 600 lines of test code for every line of code in SQLite. Tests cover 100% of branches in the library. The test suite is extremely diverse, including fuzz tests, boundary value tests, regression tests, and tests that simulate operating system crashes, power losses, I/O errors, and out-of-memory errors.

---

<small>This writing is not my own. The first section is a rehash of the words from [SQLite Most Deployed](https://www.sqlite.org/mostdeployed.html) page. The testing section paragraph entirely taken verbatim from [SQLite: past, present, and future](https://dl.acm.org/doi/abs/10.14778/3554821.3554842) paper.</small><br>