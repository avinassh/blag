---
title: "Recurse Center Day 24: Hacking Go compiler to add a new keyword"
date: "2021-12-08T13:03:55+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin", "go", "compiler"]
slug: "rc-day-24"
summary: "I forked and modified Go compiler to add a new keyword called `let`, as alias for `var`"
---

## Go Compiler

I want to poke around the Go compiler and understand some internals for my next RC project. I want to add a new feature that does something new to the compiler. I found this fantastic article [Go compiler internals: adding a new statement to Go](https://eli.thegreenplace.net/2019/go-compiler-internals-adding-a-new-statement-to-go-part-1/) by Eli Bendersky, precisely what I want!

Before doing anything significant, I wanted to make a tiny change to get familiar with the toolchain. First, I decided to add an alias `loop` for `for`. However, the compiler codebase already uses keyword loop as a label at many places, so I changed my alias. Also, instead of `for`, I decided to add an alias for `var`. The rest of this post summarises how I accomplished this and my learnings along the way.

I cloned the Go compiler (this is like \~500mb):

```
# Already forked on Github
# I have cloned in /Users/avi/code or ~/code
git clone git@github.com:avinassh/go.git go-fork 

# This is the latest release of this writing
git checkout tags/go1.17.4 -b var-vah
```

The next step was to make a minimal change, compile and make sure it worked. I decided I would rename `var` to `vah` so that I can compile the following:

```go
package main

import "fmt"

func main() {
	vah someVar = 42;
	fmt.Println(someVar)
}
```

If you compile the above, you will get the following error:

```shell
# command-line-arguments
./main.go:6:6: syntax error: unexpected someVar at end of statement
```

The go compiler code resides at `src/cmd/compile/internal`. To compile, run `src/make.bash`. Another alternative is to run `all.bash`, which runs all the tests but can be very slow for rapid development.

There are a couple of things I need to do:

1. Add a new token, `vah`, to tokenise my code correctly. That is, recognise a new word called `vah` in my source code.
2. Parse the code and generate an identical AST as `var`. Make it so that it thinks `vah` is the same as `var`.

### Adding a new token

Adding a new keyword in Go is...[interesting](https://github.com/avinassh/go/commit/07be904cff):

1. There is a file `tokens.go` which maintains an enum of all tokens
1. The keys point to the tokens
1. The comment next to them are the actual tokens you have in the source code

```go
// syntax/tokens.go
	_Struct      // struct
	_Switch      // switch
	_Type        // type
	_Var         // var
	_Vah 		 // vah
}
```

The next step is to generate tokens by using `go generate` in the `syntax` directory, but I got an error:

```sh
GOROOT=/Users/avi/code/go-fork go generate tokens.go
tokens.go:9: running "stringer": exec: "stringer": executable file not found in $PATH
```

This error can be fixed easily by installing `stringer`:

```sh
go get golang.org/x/tools/cmd/stringer
```

(Above might modify `go.mod` and `go.sum`, so do a git clean)

Above command [modified](https://github.com/avinassh/go/commit/4ba3f6e7d7) `token_string.go` file. I was able to compile the compiler too. But it did not work as expected; when I tried to compile my code, the error was the same as earlier. As if it did not consider any changes I made. I spent the next four hours figuring out and pulling my hair out.

### Keyword map generator

Following is the [keyword map generator code](https://github.com/avinassh/go/blob/go1.17.4/src/cmd/compile/internal/syntax/scanner.go#L426,#L435):

```go
func init() {
	// populate keywordMap
	for tok := _Break; tok <= _Var; tok++ {
		h := hash([]byte(tok.String()))
		if keywordMap[h] != 0 {
			panic("imperfect hash")
		}
		keywordMap[h] = tok
	}
}
```

Notice how the for loop is hardcoded till `_Var`, but not till the [last item `tokenCount`](https://github.com/avinassh/go/blob/go1.17.4/src/cmd/compile/internal/syntax/tokens.go#L70). So the keyword generator wasn't even considering my new token! 

### Keyword map size

I [moved](https://github.com/avinassh/go/commit/e07e586041) the `vah` to a line above. This time when I tried to bootstrap the compile, I got an error:

```shell
./make.bash

Building Go cmd/dist using /usr/local/Cellar/go/1.17.2/libexec. (go1.17.2 darwin/amd64)
Building Go toolchain1 using /usr/local/Cellar/go/1.17.2/libexec.
Building Go bootstrap cmd/go (go_bootstrap) using Go toolchain1.
panic: imperfect hash

goroutine 1 [running]:
bootstrap/cmd/compile/internal/syntax.init.0()
	/Users/avi/code/go-fork/src/cmd/compile/internal/syntax/scanner.go:431 +0xc5
```

This error was [originating](https://github.com/avinassh/go/blob/go1.17.4/src/cmd/compile/internal/syntax/scanner.go#L430,#L432) from keyword map generator. From Eli's blog:

> The compiler tries to build a "perfect" hash table to perform keyword string to token lookups. By "perfect" it means it wants no collisions, just a linear array where every keyword maps to a single index. The hash function is rather ad-hoc (it only looks at the contents of the first characters of the string token, for example) and it's not easy to debug why a new token creates collisions. To work around it, I increased the lookup table size by changing it to [1 << 7]token, thus changing the size of the lookup array from 64 to 128. This gives the hash function much more space to distribute its keys, and the collision went away.

So I [changed the size to 128](https://github.com/avinassh/go/commit/8009619e8e), but the error persisted.

### Token Hash

There is a [method](https://github.com/avinassh/go/blob/go1.17.4/src/cmd/compile/internal/syntax/scanner.go#L418,#L422) in `syntax/scanner.go` which says how the hash is calculated:

```go
// hash is a perfect hash function for keywords.
// It assumes that s has at least length 2.
func hash(s []byte) uint {
	return (uint(s[0])<<4 ^ uint(s[1]) + uint(len(s))) & uint(len(keywordMap)-1)
}
```

The `hash` method considers the token's first and second characters and the length. I was pairing with Miccah, and he pointed to this method; thanks to him, I figured out that `var` and `vah` had the same hash, and hence it was breaking!

I decided to [use](https://github.com/avinassh/go/commit/2886c0344c) `let` instead of `vah`. So my code would be:

```go
package main

import "fmt"

func main() {
	let someVar = 42;
	fmt.Println(someVar)
}
```

After all these changes, I was able to bootstrap the compiler.

### Updating the parser

Updating the parser was fairly simple. When encountering the `let` token in the parsing step, I wanted to behave as if it encountered `var`. So I made the [following change](https://github.com/avinassh/go/commit/50f8bd505c):

```go
// syntax/parser.go
switch p.tok {
	case _Var, _Let:
		return p.declStmt(p.varDecl)

	case _Const:
		return p.declStmt(p.constDecl)

	case _Type:
		return p.declStmt(p.typeDecl)
	}
```

The method `p.declStmt(p.varDecl)` parses the current statement as `var`.

This change alone was enough to compile my custom code, but it didn't work at first, and I spent more than two hours debugging why. I had set a `GOROOT` in my shell, which pointed to my system installation. I had to update this to point to the forked repo, and it worked!

```
$ GOROOT=/Users/avi/code/go-fork ./go run main.go
42
```

So far, my changes have been minimal. If a `for` loop had `var` declaration, it wouldn't throw a warning. If I had a global `let` declaration, it would fail: 

```go
package main

import "fmt"

let someVar int = 42

func main() {
	fmt.Println(someVar)
}
```

```shell
# command-line-arguments
./main.go:14:1: syntax error: non-declaration statement outside function body
```
I [updated](https://github.com/avinassh/go/commit/454505b7a9) my code to handle these cases for the sake of completion.

## Final words

1. Hacking on an unknown large codebase is scary at first, but it is satisfying
1. Due to hash calculations, you can't add single-character tokens, tokens that are of the same length but differ after 3rd characters onwards
1. Other than Eli's post, there are no documentation or articles on Go compiler internals. How does someone get started working on them? How do they navigate and find all these intricacies without spending hours? Maybe Google has some internal documentation on the Go compiler.

(update 9/Dec)**Note**: This post is getting a lot attention. Any chance you are a regular Go contributor? I would love to learn about the daily development cycle. How do you make changes, how do you do quick tests before running the whole test suite etc. Feel free to reach out to me [@iavins](https://twitter.com/iavins) or [email]({{< ref "about" >}}).
