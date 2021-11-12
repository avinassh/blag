---
title: "Recurse Center Day 5: Garbage Collection Algorithms"
date: "2021-11-06T16:59:29+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-5"
summary: "Learning the basics of GC, mark-sweep algorithm"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## Meet & Greets

We had another meet and greet session! I had one on one with a few, break out room chat with a few others. This is the last session arranged by RC, however, if people are interested there can be more. I am hoping we will have a few more of these and do them more often. I enjoy these because it's fun to meet new people, learn their experiences and hear about all the interesting things they want to do at RC.

I also found a few people who are interested in my database project. I am hoping to talk with them more and collaborate.

## Garbage Collection Algorithms

Today I learned about the basics of garbage collection algorithms, from the [Crafting Interpreters](https://www.craftinginterpreters.com/garbage-collection.html) by Bob Nystrom. It seems there are two kinds of them, Conservative and Precise, but I don't think I fully understood the distinction. Crafting Interpreters implements a precise garbage collector.

One of the easy algorithms is Mark and Sweep, which was introduced by John McCarthy (who also coined the term garbage collection) in the seminal Lisp paper. The algorithm is fairly simple, which involves two phases:

1. Mark: Find all the root things and mark them. Recursively find all the things which are pointed by the roots, mark them
1. Sweep: Anything which is unmarked, should be freed and garbage collected

The book does an amazing job explaining the basics and the algorithm, so go check it out!

## B Tree

I spent some time thinking about the B Tree, nodes, and paging. It suddenly dawned on me that I need to write a memory management system too, which

1. Maintains a list of empty, not full and full pages
2. Does garbage collection of pages (?)
3. Does defragmentation of pages, to fill the gaps 

My background is in writing web services. Most web programming languages do all these with in-memory data structures. Now I am writing an on-disk data structure, I need to do all of these chores.

Are there any programming languages that come with built in support for disks too?

I also found two good resources which teach about data structures for external memory:

1. Algorithms and Data Structures for External Memory by Jeffrey Scott Vitter - [(pdf)](https://www.ittc.ku.edu/~jsv/Papers/Vit.IO_book.pdf)
1. A data structures book which has two chapters specifically for external storage - [link](http://orion.lcg.ufrj.br/Dr.Dobbs/books/book9/toc.htm)


## People

I paired with David today who is writing a compiler for Lisp in C. He was re-implementing the garbage collector. This was a precise garbage collector and [this article](https://maplant.com/gc.html) provided a good starting point. While all these things were new to me, David was kind and incredibly patient, explained new things and provided enough context.

Few things I learned:
1. [A hack](https://stackoverflow.com/a/39719156) to find current stack pointer
2. [Tagged pointers](https://en.wikipedia.org/wiki/Tagged_pointer) which were used in marking the objects in the mark phase

## Presentations

I attended the Presentation session, which happens every Friday (at 1:30 am. my sleep: 😐) where everyone gets five minutes to present on things. This event is open to the current batch of RC and also to alumni. People are free to present to anything, as long as it is technical, it can be about the project they are working on, a tricky bug they run into or something new they learned.

This was a great session, had people talking about a variety of things: someone built a custom keyboard, CSS/Design, meme generator, elixir, handmade hero etc. 

I was fully inspired and pumped up to work on my projects.

...and that wrapped [my first week]({{< ref "posts/rc-week-1" >}}) at the Recurse Center.