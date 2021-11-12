---
title: "Recurse Center Day 4: B Tree fill factor"
date: "2021-11-05T16:59:22+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-4"
summary: "Q: How do I have a same B Tree fill factor across all nodes?"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

I spent the half day today, because of [Deepavali](https://en.wikipedia.org/wiki/Deepawali) and also my sleep issues.

## Advice and Introductions

We had a new activity today, where RC facilitators, alumni and people who are currently RC* joined the call and gave us advice.

All of us in the current batch introduced ourselves, our backgrounds and all things we want to do at RC. It was exciting to meet my batch, hear their diverse backgrounds and all the interesting things they want to do at RC.

Each alumnus introduced themselves, told us what they are doing at RC, shared their experiences. Here is some advice 

1. Have a few fallback projects along with the main ones, for rainy days so that you can bounce back
1. Learn to balance time. Try to do both, socialise, learn from others but also work on your projects
1. While RC is for three months, the time is quite limited. It finishes very quickly, be prepared!
1. Reflect and keep reevaluating what works for you and what doesn't
1. There are so many exciting things going on here, try all of them!
1. Go where your heart takes, do things that interest you most <3

\*RC batches overlap. For e.g. my batch started on Nov 1 and will go on till Feb. A new batch starts on Jan 1 and my batch would overlap. I think this is nice because you get to know and work with lots of people, during a batch at RC.

## B Tree

Not much progress today. There is one question that keeps bugging me: how do I maintain the same fill factor across all nodes if the keys are of variable length?

B Tree nodes contain keys and the nodes have a property called Fill Factor. If the fill factor is 63% and if nodes can hold 100 keys, then we will put only 63 keys. However, the keys are variable in length, so not every node can hold 100 keys. So, I am wondering how do we achieve the same fill factor with all nodes.

## People

I paired with Oliver today who is contributing to PyTorch. We discussed how to add tests to the PR. There were two ways to write the tests, I felt there no was right or wrong with either approach. Ultimately we decided that it is best we open the PR and ask the maintainer themselves.

I think this is one of the advantages contributing to the open source. If one is not sure how to do X, we could ask the maintainers and get some guidance. I think contributing to open source has surely improved my coding, especially low level design skills.

edit: [The PR](https://github.com/pytorch/pytorch/pull/67756) is now accepted. Hurray! 

## Deepavali

A [rangoli](https://en.wikipedia.org/wiki/Rangoli) by my artful wife:

![](/blag/images/2021/deepavali.jpg)

Happy Deepavali :)
