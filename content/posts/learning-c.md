---
title: "Learning C"
date: "2024-03-02T15:08:39+05:30"
categories: ["systems", ""]
tags: ["c", "systems"]
slug: "learning-c"
summary: "Some resources for learning C"
---

I am beginning to learn C, and I [asked for resources](https://twitter.com/iavins/status/1625896692175486976) on the same. Here is what I got:

1. K&R C book - This is the OG book. It is short and concise. However, it is old now and has some minor bad practices/incorrect code apparently.
2. Modern C by Jens Gustedt - This is a more modern book. However, the book expects that you know _some C_ and can be difficult for someone new like me to pick up. This book is also available for free online.
3. Effective C by Robert C. Seacord - Another introductory alternative. This also teaches modern practices and is beginner friendly.

## Advice

I asked my fren, Mr. xyz, a C veteran who has worked in various domains from battery controllers to databases, for advice on learning C. The advice I received:

Follow these books (in order): 
  
1. K&R C
2. Programming in the UNIX Environment
3. Programming Abstractions in C


An alternate path:

1. Effective C
2. Modern C

K&R style and modern style are different, but both are prevalent in different areas. Start with one, completely understand the philosophy, idioms, and patterns, and then move to the other.

Do the K&R and Programming Abstractions in C exercises in the modern style. These exercises are invaluable. They may seem simple, but they are a pretty good test of understanding C.

The depth comes only when you work with simple code and see how small changes can have big effects.

## Cthulhu

The very apt cover of Modern C:

<img src="/blag/images/2024/c-for-cthulhu.jpeg" alt="C for Cthulhu" style="width: 40%;"/>

My goals are:
- Port [CaskDB](https://github.com/avinassh/py-caskdb) to C
- Make a major contribution to libSQL