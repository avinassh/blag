---
title: "Errata in Hekaton MVCC paper"
date: "2023-04-20T22:19:15+05:30"
categories: ["database", ""]
tags: ["database", "hekaton", "typo", "mvcc"]
slug: "hekaton-paper-typo"
summary: "Hekaton MVCC Paper contains a publication error. After reviewing the paper, I confirmed the error with one of the authors. This blog post explains the mistake, the implications and the fix."
---

Hekaton MVCC Paper - [High-Performance Concurrency Control Mechanisms for Main-Memory Databases](https://vldb.org/pvldb/vol5/p298_per-akelarson_vldb2012.pdf) - contains a publication error. After reviewing the paper, I confirmed the error with one of the authors. This blog post explains the mistake, the implications and the fix. I blogged about the background story and my discovery in [another post](https://avi.im/blag/yet-to-link).

## Error

Following the conventions of the paper, here is a state diagram:

![](/blag/images/2023/hekaton-state.png)

At time 60, we observe our initial state, where the value of Larry is 170. This is a committed row.
At time 75, a transaction is started and is in `Active` state. It wants to update the value to 150, so it appended row 2
At time 80, another new transaction, Tx80 is started, and it wants to read the value of Larry. Both Tx75 and Tx80 are in `Active` state.

What is the value Tx80 going to read?

Tx80 can't see row 2 because of Table 1 rules. If Tx75 is in `Active` state, only Tx75 can see row 2. This makes sense because row 2 is fresh, and Tx75 might drop the changes later. We don't want any other transactions to see this row.

But can Tx80 see row 1? The rules from the paper contradict that since Tx75 is in `Active` state:

![](/blag/images/2023/hekaton-table-2.png)

This is a typo, and Tx80 should be able to see row 1 since it is a committed row. Also, Tx75 should not be able to see row 1 anymore; instead, only row 2, which it is updating.

## Implications
Committed rows can become invisible for new transactions
Rows become invisible to the very transactions which are updating them

## Fix

The fix is simple: 

```
V is visible only if TE is not T
```

By doing this:
- Tx80 can now see row 1 (but not row 2)
- Tx75 can now see row 2 (but not row 1)
