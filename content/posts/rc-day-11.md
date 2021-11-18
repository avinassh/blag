---
title: "Recurse Center Day 11: B Tree Insertions"
date: "2021-11-16T16:07:59+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin", "btree"]
slug: "rc-day-11"
summary: "I started writing code for B Tree insertions"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## B Tree

I was having trouble with the B Tree insertion algorithm. Here is what I was trying to do:

1. The first phase was almost similar to search. Start with the root, find the appropriate key.
1. Traverse down to the internal nodes, down to the leaf node
1. Insert in the leaf node. If the node overflows, split the node
1. (this part I was still coding, having difficulty with) If there is a node split, propagate this information upwards
1. Recursively split if needed, all the way up to root

But the algorithm given in the CLRS is slightly different:

> As with a binary search tree, we can insert a key into a B-tree in a single pass down the tree from the root to a leaf. To do so, we do not wait to find out whether we will actually need to split a full node in order to do the insertion. Instead, as we travel down the tree searching for the position where the new key belongs, we split each full node we come to along the way (including the leaf itself). Thus whenever we want to split a full node `y`, we are assured that its parent is not full.

1. If the root is full, split it 
1. Find the internal node. If it is full, split it
1. Keep on splitting till you find the leaf node
1. Since you have been splitting along the way, no more splits can happen when you insert in the leaf

This is way easier!

1. What I was trying to do was, bottom up approach and this one seems like top down
1. I am not sure why, but I find this easier to code top down approach

While this is easier, this will split the root (or internal nodes) even though it is not needed. I was trying to optimise this, as to why split it unnecessarily.

I also consulted the assignments of few of the online courses:

1. CMU Databases 15445: 2020 version (other versions seem to be asking to implement a Hash Index) has an [assignment on B Trees](https://15445.courses.cs.cmu.edu/fall2020/project2/
), but it does not address this. I guess it's up to the person who is implementing. However, I haven't checked the assignment code yet. 
1. Berkeley CS186: [The assignment](https://cs186.gitbook.io/project/assignments/proj2/your-tasks) is to implement a B Tree, but does not include more details.
1. Utah CS6530: [This](https://www.cs.utah.edu/~lifeifei/cs6530/lab2.html) goes really well into the details. They refer to [Database Management Systems](http://pages.cs.wisc.edu/~dbbook/) which neatly explain how to propagate the details to the parent.

## Javascript Arrow Functions

I paired with Tal and Nicole to get some basic understanding of arrow functions. I don't know JS enough, but now I learned how to use arrow functions!

Here are the two resources which helped me understand them better: 

- [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions), make sure to check the limitations of arrow functions
- [ES6 In Depth: Arrow functions
](https://hacks.mozilla.org/2015/06/es6-in-depth-arrow-functions/)
