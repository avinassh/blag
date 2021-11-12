---
title: "Recurse Center Day 3: Hammock Driven Development"
date: "2021-11-04T01:36:42+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-3"
summary: "TIL Hammock Driven Development"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## Pairing Workshop

I attended the pairing workshop today, it was fun! First, there was a talk that introduced us to the concept of pair programming. The talk was very thorough, from general guidelines to do's and don'ts. Next, we were randomly paired with each other, put in a break out room. I paired with Debo to solve the [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

I will write another detailed article on pair programming, but if you want to get started (you should!), [Martin Fowler's guide](https://martinfowler.com/articles/on-pair-programming.html) on pairing is pretty good.

## B Tree Node

I paired with Taylor who suggested a simpler solution, just use a single pointer:

```
[(7, *1), (16, *9)]
```

This makes everything so simple! I feel this way would work too, I will work through the edge cases. There would be an extra pointer left that points to the array which contains elements greater than the largest element in the current node. This pointer can be saved separately in the node.

While discussing, I suddenly realised that I had read this format from the Database Internals book (page 63):

![](/blag/images/2021/right-most-pointer.png)

I decided to study the internals again, jot down the actual algorithm with the data structure I have in my mind and then start coding.

## Challenges with Disk Data structures

(I will update this section with more details soon)

These are challenges one would face when writing a disk based data structure compared to memory:

1. Cache locality
2. Physical movements within HDD, which adds yuge latency
3. Byte vs block (or page) address-ability
4. Pointers
5. Garbage collection and fragmentation
6. Encoding/decoding or serialisation/deserialisation

## Hammock Driven Development

Elvis introduced me to this [cool talk](https://www.youtube.com/watch?v=f84n5oFoZBc) by Rich Hickey (the creator of Clojure) called Hammock Driven Development.

It starts with a question: How long have you spent thinking hard about a problem, a day? a week? a month? a year? When was the last time you felt so confident trying something you had never before and what would it take to become confident?

It helps at getting better and confident at problem solving. Here's how:

1. State the problem. Talk it out loud, explain to a co-worker, find a stranger and tell them what you are trying to solve
2. Understand the problem. What do you know and what do you don't know? Write everything down
3. Think trade offs, other solutions. Most likely someone must have solved the same thing

Now that you have the problem, have understood it properly... go on a hammock and sleep! yes, seriously.

Our brain works when asleep, finding hidden relations between memories and solving problems which we were working on when awake. We have two minds, a waking mind and a background mind. The waking mind is good at analysis and tactics. Background mind is good at synthesis and strategy. Background mind will help us solve difficult problems. But we need to feed the input, activate it and charge it to its full potential.

How? Focus, be away from distractions, think hard about the problem. Think as much as possible.

Think hard.

That's it! As he says, "the cake is in the oven now". Wait overnight, maybe a few days or even months. Switch around when you are stuck.

You shall have the cake at the end 🍰