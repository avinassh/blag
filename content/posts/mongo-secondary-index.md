---
title: "MongoDB secondary only index"
date: "2022-05-22T18:35:44+05:30"
categories: ["database"]
tags: ["database", "index", "mongodb"]
slug: "mongo-secondary-index"
summary: "This short post will show how to add a secondary only index in a MongoDB replica set"
---

MongoDB officially does not allow adding secondary only indexes in a replica set. However, there is one hacky way to achieve the same.

## Why

Sometimes you might have requirements which may not be needed for the main application. An actual use case is when you want to run analytics (or use things like [Metabase](https://www.metabase.com/)) but don't want to change the primary schema.

## How

Earlier, [I discovered an odd behaviour with MongoDB](https://avi.im/blag/2021/mongo-dupes-in-unique-index/) replica set and indexes. I thought one could use a similar approach to add secondary only indexes, which is what people have been doing.

The procedure is almost similar to how MongoDB adds [rolling indexes to replicas](https://www.mongodb.com/docs/manual/tutorial/build-indexes-on-replica-sets/#procedure) but slightly different.


1. Add a new member to the replica set (or pick an existing one)
1. Make this member a [non-voting member](https://www.mongodb.com/docs/manual/tutorial/configure-a-non-voting-replica-set-member/). This step is essential because we never want this member to become a primary, ever.
1. Remove the member from the replica set - [instructions](https://www.mongodb.com/docs/manual/tutorial/remove-replica-set-member/)
1. Add the indexes you need
1. Add the member back to the replica set
1. Now connect to only this instance for analytics or other purposes

You might need to repeat steps 3-5 if you want to add new indexes.

## References

1. Bunch of Jira tickets - [1](https://jira.mongodb.org/browse/SERVER-3664), [2](https://jira.mongodb.org/browse/SERVER-6587)
1. Stackoverflow - [1](https://stackoverflow.com/questions/22061008/in-mongodb-how-can-i-index-on-fields-in-collections-in-secondary-noderepli), [2](https://stackoverflow.com/questions/16472392/different-indexes-on-different-replica-set-members)
1. My [previous blog post](http://localhost:1313/blag/2021/adding-unique-index-large-collection/) where I discovered that you can add duplicate records on an unique index
