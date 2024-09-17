---
title: "Recurse Center Day 34: Regex Engine under 30 lines"
date: "2022-01-12T19:50:09+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin", ""]
slug: "rc-day-34"
summary: ""
---

## Build your own Regex Engine

I ran into this [article](https://www.cs.princeton.edu/courses/archive/spr09/cos333/beautiful.html) by Brian Kernighan which talks about Rob Pike's implementation. When they were working on *The Practice of Programming* book, they needed a simple and small implementation of a regex engine. 

> The problem was that any existing regular expression package was far too big. The local grep was over 500 lines long (about 10 book pages). Open-source regular expression packages tended to be huge, roughly the size of the entire book, because they were engineered for generality, flexibility, and speed; none was remotely suitable for pedagogy.
>
> I suggested to Rob that we needed to find the smallest regular expression package that would illustrate the basic ideas while still recognizing a useful and non-trivial class of patterns. Ideally, the code would fit on a single page.
>
> Rob disappeared into his office, and at least as I remember it now, appeared again in no more than an hour or two with the 30 lines of C code that subsequently appeared in Chapter 9 of TPOP.

In the rest of the article, I am going to port the C version to Go.

## Constructs

The regex engine we are going to write is a small subset with following constructs:

	c    matches any literal character c
    .    matches any single character
    ^    matches the beginning of the input string
    $    matches the end of the input string
    *    matches zero or more occurrences of the previous character

## Coffee Chat

I had a coffee chat with Swagnik today, we discussed so many things from interviews, Leet Code, B Trees, databases, and the book *Designing Data-Intensive Applications*.