---
title: "Til Mongo Empty Subdoc"
date: "2022-08-31T15:01:24+05:30"
categories: ["", ""]
tags: ["", ""]
slug: "til-mongo-empty-subdoc"
summary: ""
---

if you want to find a document which does not have a empty sub field, use `$gt`

e.g. `{ 'score.user': { "$gt": {} } }`

then documents without the `user` field won't be matched

https://stackoverflow.com/questions/6607102/mongodb-match-non-empty-doc-in-array/6838057#6838057