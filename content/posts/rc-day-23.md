---
title: "Recurse Center Day 23: Reflections"
date: "2021-12-07T16:38:00+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin", ""]
slug: "rc-day-23"
summary: ""
draft: true
---

Week 6 is started yesterday and that's half time of RC is done. Stopped working on the database project entirely. Once I understood the internals, the B Tree algorithms and file formats, I lost the motivation to code. I think my driving factor was the unknowns of the building blocks. I will continue to watch lectures and continue learning more.

## Reflections

- Pairing
- What makes RC pru people and how RC helps
- Have many project ideas

I [added](https://github.com/avinassh/go/commit/9d5bef4251) a new token in `syntax/tokens.go`. Next step was to generate tokens by using `go generate` in `syntax` directory but I got an error:

```sh
GOROOT=/Users/avi/code/go-fork go generate tokens.go
tokens.go:9: running "stringer": exec: "stringer": executable file not found in $PATH
```

This can be fixed easily by installing `stringer`:

```sh
go get golang.org/x/tools/cmd/stringer
```

(Above might modify `go.mod` and `go.sum`, so do a git clean)

Above command [modified](https://github.com/avinassh/go/commit/c0f2bb8fce) `token_string.go` file. But I failed to compile the compiler. Turns out go source code had many uses of `loop` keyword as a label. So I [renamed](https://github.com/avinassh/go/commit/6a18f76431) my `loop` to `fuh`.

The next step was to figure out how `for` statements are parsed and make it parse `fuh` statements as well.
