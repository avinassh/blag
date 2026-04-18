---
title: "SQLite prefixes its temp files with `etilqs_`"
date: "2026-04-18T19:40:33+05:30"
categories: ["database", "sqlite"]
tags: ["database", "sqlite", "vacuum", "easter egg"]
slug: "etilqs"
summary: "Here's some wild lore inside SQLite's source code explaining why temp files start with `etilqs_`"
---

[Turso](https://github.com/tursodatabase/turso) is a rewrite of SQLite in Rust, fully compatible with SQLite. I've been working on implementing `VACUUM` and studying their (beautiful) code. `VACUUM` rebuilds the database into a fresh temporary file to reclaim space and defragment pages. SQLite prefixes this temp file with `etilqs_`.

Here's why:

```c
/*
** 2006-10-31:  The default prefix used to be "sqlite_".  But then
** Mcafee started using SQLite in their anti-virus product and it
** started putting files with the "sqlite" name in the c:/temp folder.
** This annoyed many windows users.  Those users would then do a 
** Google search for "sqlite", find the telephone numbers of the
** developers and call to wake them up at night and complain.
** For this reason, the default name prefix is changed to be "sqlite" 
** spelled backwards.  So the temp files are still identified, but
** anybody smart enough to figure out the code is also likely smart
** enough to know that calling the developer will not help get rid
** of the file.
*/
#ifndef SQLITE_TEMP_FILE_PREFIX
# define SQLITE_TEMP_FILE_PREFIX "etilqs_"
#endif
```

It's here: [os.h](https://github.com/sqlite/sqlite/blob/version-3.53.0/src/os.h#L65,%23L79).