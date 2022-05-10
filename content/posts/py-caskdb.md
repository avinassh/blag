---
title: "Introducing CaskDB – a project to teach you writing a key-value store"
date: "2022-05-10T21:46:11+05:30"
categories: ["", ""]
tags: ["", ""]
slug: "py-caskdb"
summary: "CaskDB is an educational project which aims to guide you in writing a persistent, embeddable database from scratch."
---

For the past few months, I have been learning about the internals of database systems. After doing a batch at [Recurse Center (Nov 2021)](https://avi.im/blag/tags/recurse-center/) researching databases, I have been working on writing my toy database. I found many excellent articles on building compilers, but I could not find many practical resources for databases. So I wrote one. [CaskDB](https://github.com/avinassh/py-caskdb) is the project I wish I had started with.

CaskDB is based on Riak's Bitcask paper. The idea of Bitcask is brilliant yet straightforward, which makes it attractive for newbies to learn about key-value store internals and implement one.

I have set up this project in TDD fashion with the tests. So, you start with simple functions, pass the tests, and the difficulty level goes up. There are [hints](https://github.com/avinassh/py-caskdb/blob/d80cacb/hints.md) if you get stuck. When all the tests pass, in the end, you would have written a persistent key-value store.

I had great fun implementing this, and I hope you do too. And I hope this makes you dig deep into the fantastic world of database engineering.

link - https://github.com/avinassh/py-caskdb