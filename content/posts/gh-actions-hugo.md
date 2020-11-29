---
title: "Setting up Github Actions for Hugo"
date: "2020-11-29T14:15:53+05:30"
categories: ["hugo"]
tags: ["hugo", "notes"]
slug: "gh-actions-hugo"
summary: "Github Actions for Hugo but with particular requirements"
---

I setup [Github Actions workflow](https://github.com/avinassh/blag/blob/9883271408233130eb4e7b8ba6aab25d954ab55a/.github/workflows/production.yml) for this blog to automate the publishing. Actions were new to me, this was a fun learning activity.

I had to write a new one because I could not find an existing action which filled my needs. Here is how it is setup:

1. My content, hugo config stays in the root of `master` branch and published site is at root of `gh-pages`.

2. Every commit on `master` should trigger a publish and non `master` commits should be ignored. For them, I use netfliy deploy previews.

3. Commits on `gh-pages` should preserve history. Some actions delete the existing history.

4. Since every commit on `gh-pages` reflects a commit from `master`, I wanted each of these commits to have the same commit message which triggered the build.

I have made this Github Action available here - [hugo-publish](https://github.com/avinassh/hugo-publish)