---
title: "Debugging and developing on SQLite codebase"
date: "2024-03-31T17:25:06+05:30"
categories: ["sqlite"]
tags: ["sqlite", "open source"]
slug: "debugging-sqlite"
summary: "Some notes for hacking on SQLite codebase"
---

To gain a deeper understanding of the SQLite codebase, I often modify the source code and test my hypotheses. Here are some of the things I've learned.

## Amalgamation

SQLite has a step called amalgamation, which produces a large `sqlite.c` file. While debugging, I find it difficult to follow the source code in a single file, jump around, and then locate the same lines in the actual source files located in `src/`. One problem is that any small change will require a full compilation of the modules to generate a single file. Fortunately, there is a way to [avoid amalgamation process](https://sqlite.org/forum/forumpost/722232fc5fc0f3b5) altogether.

Instead of using the default `Makefile`, use `Makefile.linux-gcc`. I have made some changes to this:

```makefile
TOP = ./

BCC = gcc -g -O0 -ggdb

OPTS += -DSQLITE_DEBUG=1
```

## Compilation

I have a simple test script in C:

```c
#include <stdio.h>
#include <sqlite3.h>

static int callback(void *NotUsed, int argc, char **argv, char **azColName)
{
    int i;
    for (i = 0; i < argc; i++)
    {
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    }
    printf("\n");
    return 0;
}

int main()
{
    sqlite3 *db;
    char *zErrMsg = 0;
    sqlite3_open("users.db", &db);
    `sqlite3_exec(db, "PRAGMA journal_mode = WAL;", 0, 0, 0);`
    sqlite3_exec(db, "SELECT * FROM t", callback, 0, &zErrMsg);
    sqlite3_close(db);
    return 0;
}
```

I have omitted error handling for brevity. Full code is [here](https://gist.github.com/avinassh/01315875aef4fd8c93808c233b4e65a8). Save this file as `mytest.c` in the same directory as the SQLite source (on my machine it is `/code/sqlite`). Then I use the following command to compile and run:

```bash
 gcc -g -fPIC -I/code/sqlite -L/code/sqlite mytest.c -o mytest -lsqlite3 -ldl -O0 -g -ggdb
```

## VDBE Trace

SQLite has a cool feature where it prints the VDBE instructions and register contents as it executes an SQL statement. There are various options like `vdbe_addoptrace`, `vdbe_debug`, `vdbe_listing`, and `vdbe_trace`. You can find explanations of these on the [PRAGMA Statements](https://www.sqlite.org/pragma.html) page. I usually find `vdbe_trace` to be sufficient. For VDBE traces to work, SQLite needs to be compiled with the [`SQLITE_DEBUG`](https://www.sqlite.org/compile.html#debug) flag.

Output of the previous script with tracing:

```
SQL: [PRAGMA vdbe_trace=1]
VDBE Trace:
   0 Init             0    4    0               00 Start at 4
   4 Goto             0    1    0               00
   1 Expire           1    1    0               00
   2 Expire           0    0    0               00
   3 Halt             0    0    0               00
SQL: [SELECT * FROM t]
VDBE Trace:
   0 Init             0    9    0               00 Start at 9
   9 Transaction      0    0    3 0             01 usesStmtJournal=0
  10 TableLock        0    2    0 t             00 iDb=0 root=2 write=0
  11 Goto             0    1    0               00
   1 OpenRead         0    2    0 2             00 root=2 iDb=0; t
   2 Explain          2    0    0 SCAN t        00
   3 Rewind           0    8    0               00
   4 Rowid            0    1    0               00 r[1]=t.rowid
R[1] =  i:1
   5 Column           0    1    2               00 r[2]= cursor 0 column 1
R[2] =   s1[f](8)(0-term)
   6 ResultRow        1    2    0               00 output=r[1..2]
R[1] =  i:1
R[2] =   s1[f](8)(0-term)
   7 Next             0    4    0               01
   8 Halt             0    0    0               00
```

If you are debugging something using the shell, you can use [`.eqp trace`](https://www.sqlite.org/debugging.html) for a similar effect.

Also check [Debugging Hints](https://www.sqlite.org/debugging.html) from the SQLite documentation.