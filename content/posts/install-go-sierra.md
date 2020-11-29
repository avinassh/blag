---
title: "Install Go / Golang on macOS Sierra (10.12.x) using Homebrew"
date: "2016-12-06T19:03:00+05:30"
categories: ["code"]
tags: ["golang"]
slug: "install-go-sierra"
summary: "Install Go v1.7.x on OS X 10.12.x with Homebrew."
---

Do the following:

    $ brew update
    $ brew install go

    ...
    ==> Caveats
    As of go 1.2, a valid GOPATH is required to use the `go get` command:
      https://golang.org/doc/code.html#GOPATH

    You may wish to add the GOROOT-based install location to your PATH:
      export PATH=$PATH:/usr/local/opt/go/libexec/bin
    ==> Summary
    🍺  /usr/local/Cellar/go/1.7.4: 6,438 files, 250.7M

As it says we need to set `GOPATH` and also `GOROOT`:

    $ mkdir $HOME/.go

If then add this to your profile, `.bash_profile` or `.zshrc`:

    # go things
    export GOPATH=$HOME/.go
    export GOROOT=/usr/local/opt/go/libexec
    export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
