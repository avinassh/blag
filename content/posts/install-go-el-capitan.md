---
title: "Install Go / Golang on OS X El Capitan (10.11.x) using Homebrew"
date: "2016-05-12T19:20:00+05:30"
lastmod: "2016-12-04T19:08:00+05:30"
categories: ["code"]
tags: ["golang"]
slug: "install-go-el-capitan"
summary: "Install Go v1.6.2. on OS X 10.11.x with Homebrew."
draft: true
---

Do the following:

    $ brew update
    $ brew install go --with-cc-all

    ==> Downloading https://homebrew.bintray.com/bottles/go-1.6.2.el_capitan.bottle.tar.gz
    Already downloaded: /Users/avi/Library/Caches/Homebrew/go-1.6.2.el_capitan.bottle.tar.gz
    ==> Pouring go-1.6.2.el_capitan.bottle.tar.gz
    ==> Caveats
    As of go 1.2, a valid GOPATH is required to use the `go get` command:
      https://golang.org/doc/code.html#GOPATH

    You may wish to add the GOROOT-based install location to your PATH:
      export PATH=$PATH:/usr/local/opt/go/libexec/bin
    ==> Summary
    🍺  /usr/local/Cellar/go/1.6.2: 5,778 files, 325.3M

As it says we need to set `GOPATH` and also `GOROOT`:

    $ mkdir $HOME/.go

If then add this to your profile, `.bash_profile` or `.zshrc`:

    # go things
    export GOPATH=$HOME/.go
    export GOROOT=/usr/local/opt/go/libexec
    export PATH=$PATH:$GOROOT/bin:$GOPATH/bin

### Updating to/Installation of Go 1.7.x

If you followed above methods and now want to update to 1.7.x, then do following:

    $ brew update
    $ brew upgrade go

If you are doing a fresh install, then do:

    $ brew update
    $ brew install go

And set `GOPATH` and `GOROOT` like earlier.


### Resources

1. [Brew recipe](https://github.com/Homebrew/homebrew-core/blob/9c867d598eee0f77350155c11f3ece6717c9026c/Formula/go.rb)
2. [This SO answer](http://stackoverflow.com/a/28423229/1382297)
