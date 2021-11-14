---
title: "The brilliant simple ideas from Amazon's Dynamo paper"
date: "2021-11-14T00:20:51+05:30"
categories: ["database", ""]
tags: ["database", "dynamo", "dist-sys"]
slug: "amazon-dynamo-paper"
summary: "How amazon solved their problems related to availability and performance with few simple ideas"
---

I attended Papers We Love group at Recurse Center and spent some reading Amazon's Dynamo paper titled [Dynamo: Amazon’s Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf). The paper is easy to read, approachable, and has tons of implementation details. But, what I loved most was, how they brilliantly solved their problems with a bunch of really simple ideas. The paper does not 'invent' any new thing, rather they use the existing ideas.

NOTE: The paper came out in 2007. It has no relation with [Amazon DynamoDB](https://aws.amazon.com/dynamodb/). I don't think there are any public information about the Dynamo, other than this paper.

## The Larger Problem

Before we break into the smaller problems, let me first list down the larger problem the amazon wanted to solve:

- A system with low latency, 99.9th percentile of delay < 300 ms
- No matter what, it should always be available. Especially, writes should never fail
- From the paper: customers should be able to view and add items to their shopping cart even if disks are failing, network routes are flapping, or data centers are being destroyed by tornados.

