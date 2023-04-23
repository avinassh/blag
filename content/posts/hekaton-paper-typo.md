---
title: "Errata in Hekaton MVCC paper"
date: "2023-04-20T22:59:15+05:30"
categories: ["database", ""]
tags: ["database", "hekaton", "typo", "mvcc"]
slug: "hekaton-paper-typo"
summary: "Hekaton MVCC Paper contains a publication error. After reviewing the paper, I confirmed the error with one of the authors. This blog post explains the mistake, the implications and the fix."
---

Hekaton MVCC Paper - [High-Performance Concurrency Control Mechanisms for Main-Memory Databases](https://vldb.org/pvldb/vol5/p298_per-akelarson_vldb2012.pdf) - contains a publication error. After reviewing the paper, I confirmed the error with one of the authors. This blog post explains the mistake, the implications and the fix. I blogged about the background story and my discovery in [another post]({{< ref "posts/internet-mvcc" >}}).

## Error

Following the conventions of the paper, here is a state diagram:

![](/blag/images/2023/hekaton-state.png)

1. At time 60, we observe our initial state, where the value of Larry is 170. This is a committed row.
2. At time 75, a transaction is started and is in `Active` state. It wants to update the value to 150, so it appended row<sub>2</sub>
3. At time 80, another new transaction, Tx80 is started, and it wants to read the value of Larry. Both Tx75 and Tx80 are in `Active` state.

What is the value Tx80 going to read?

Tx80 can't see row<sub>2</sub> because of Table 1 rules. If Tx75 is in `Active` state, only Tx75 can see row<sub>2</sub>. This makes sense because row<sub>2</sub> is fresh, and Tx75 might drop the changes later. We don't want any other transactions to see this row.

But can Tx80 see row<sub>1</sub>? The rules from the paper contradict that since Tx75 is in `Active` state:

<img src="{filename}/images/2023/hekaton-table-2.png" alt="makey makey offer page" style="width: 50%;"/>

![](/blag/images/2023/hekaton-table-2.png)

{{ $image := .Resources.GetMatch "sunset.jpg" }}

This is a typo, and Tx80 should be able to see row<sub>1</sub> since it is a committed row. Also, Tx75 should not be able to see row<sub>1</sub> anymore; instead, only row<sub>2</sub>, which it is updating.

## Implications
- Committed rows can become invisible for new transactions
- Uncommitted rows can become invisible to the very transactions which are updating them

## Fix

The fix is simple: 

> V is visible only if TE is not T

By doing this:
- Tx80 can now see row<sub>1</sub> (but not row<sub>2</sub>)
- Tx75 can now see row<sub>2</sub> (but not row<sub>1</sub>)
