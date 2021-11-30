---
title: "Recurse Center Day 16: Open Source"
date: "2021-11-23T16:13:29+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-16"
summary: "merged few open pull requests on my projects"
---

## Open Source

One of the good things about participating at RC is that you can work on anything you want. Yesterday I spent some time on the open PRs I had gotten on my side projects.

- [A PR](https://github.com/avinassh/fast-sqlite3-inserts/pull/19) on my [fast sqlite inserts]({{<ref "posts/fast-sqlite-inserts">}}) project improved the performance by ~22%, bringing down the insertion time to 23s!
- [A PR](https://github.com/avinassh/grpc-errors/pull/23) on grpc-errors repo fixed the Go examples to make it work with newer versions of golang, go mod, and gRPC

### Upgrading Django version (v1 to v4)

I have an [open source project](https://github.com/avinassh/della) that uses an outdated version of Django. I looked into updating to the latest version. I believe this task would be pretty easy as I don't need to support backward compatibility.

(I will add more notes here on the process)
