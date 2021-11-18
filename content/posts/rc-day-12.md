---
title: "Recurse Center Day 12: Isolation Anomalies"
date: "2021-11-17T17:39:27+05:30"
categories: ["recurse-center", "database"]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-12"
summary: "Anomalies which define transaction isolation levels"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## Read and Write Anomalies

I was researching concurrency and isolation levels, I read about Read Anomalies which are also referred to as Phenomena.

1. Dirty read: Say transaction T1 made changes to some row and transaction T2 read or updated it before T1 committed. Now if T1 aborts, T2 read something which never existed in the first place.

1. Non-repeatable read (or fuzzy read): is when a transaction queries the same row twice and gets different results

1. Phantoms: pretty much the same as fuzzy read but when applied over a range of queries. Fuzzy read applies to a single record and phantoms to a range of records.

How do these affect isolation levels? Here is a handy chart:

![](/blag/images/2021/anomalies.png)

Source: [Transaction Isolation Levels](https://docs.microsoft.com/en-us/sql/odbc/reference/develop-app/transaction-isolation-levels?view=sql-server-ver15) (this page is also a good reference on the topic)

I also started reading a related paper: [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf)

## People

I paired with Jake earlier, to work on my B Tree project. Some thoughts:

1. I spent way too much explaining the B Tree. I am not sure if I am bad at explaining or B Tree is too complex.
2. I am adding tests as I am writing. This helped a lot during the pairing session, we were quick to write, test and reiterate.
