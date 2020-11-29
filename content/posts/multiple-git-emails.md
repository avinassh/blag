---
title: "How I Am Maintaining Multiple Emails For Git On A Same Machine"
date: "2015-08-01T22:20:00+05:30"
categories: ["tutorial"]
tags: ["git"]
slug: "multiple-git-emails"
summary: "In this simple tutorial I will show how to maintain multiple git emails on a same machine. And how to configure git emails per directory or per project."
---

Every git commit is associated with two important data: your name and email. I don't want my personal email address associated with work related git commits and vice versa. First, to set the git email address system wide, you would run following:

    $git config --global user.email "your_global@email.com"
    $git config --global user.name "Your Name"


and every commits will have above info. To set the email address for individual repo, just drop the `global`. `cd` into your repository and run the following:

    $git config user.email "your_project@email.com"
    $git config user.name "Your Name"

Now every commit for *this* repository will have above email. There is another way, by modifying `.git/config` of your repository and including a `[user]` block, something like:

    [core]
        ...
    [remote "origin"]
        ...
    [branch "master"]
        ...
    [user]
        name = Your Name
        email = your_project@email.com

## Problems
Though above mentioned methods work, there are two major issues (at least for me):

1. You have to run the above command everytime you create a new repository.
2. You have to remember #1.

\#2 is actually difficult for me.

## Solution
Use [`direnv`](http://direnv.net/). `direnv` is one nifty tool which lets you have different environment variables based on directories/path. The best part is, as soon as you enter into a directory, `direnv` does it's magic, so you don't have to remember that you have to run `direnv`. For `direnv` to work, you have to create a file called `.envrc` where you can specify what all environment variables you want and place it the directory.

This is how I have organized my repositories:

    ~/
    |- work # all work related repos go here
        |-- .envrc
        |-- repo-1
        |-- ...
        |-- repo_X
    |- Documents/code # all my personal projects go here
        |-- .envrc
        |-- repo-1
        |-- ...
        |-- repo_X

So, my `~/work/.envrc` contains:

    export GIT_AUTHOR_EMAIL="avi@work.com"
    export GIT_COMMITTER_EMAIL="avi@work.com"

similarly, my `~/Documents/code/.envrc` contains:

    export GIT_AUTHOR_EMAIL="avi@personal.com"
    export GIT_COMMITTER_EMAIL="avi@personal.com"

Before each prompt `direnv` checks for `.envrc` in current directory and parent directories. And when the file is found, it applies those and those variables will be present in your shell. You can also add `GIT_AUTHOR_NAME` or `GIT_COMMITTER_NAME` if you want to use different names in git commits.

### References:

 - Pro Git book on [environment variables](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables).
 - [`direnv`](http://direnv.net)