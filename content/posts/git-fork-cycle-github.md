---
title: "Git/Github fork-pull request-update cycle "
date: "2016-02-19T23:03:00+05:30"
categories: ["code"]
tags: ["git", "github", "open-source"]
slug: "git-fork-cycle-github"
description: "When contributing to Open Source Projects, new contributors often run into problems of having multiple merge commits and issues with keeping the forked repo in sync. This post addresses solutions for some of the problems."
---

Lets say there is a project called `python` and you want to contribute. So you should fork `python` project and ALWAYS create a separate branch for the patch/feature you are working on and NEVER commit on the master branch of forked repo.

Lets call your forked repo as `python-forked`.

Once you fork a project, add a git remote called `upstream` (or whatever name you feel like using), which points to original repo. This remote will help you keep your project updated and in sync with original repo (from where you forked).

```
$ cd python-forked
$ git remote add upstream https://github.com/guido/python.git 
```

Consider 3 scenarios.

### The simple, fork and send PR

Create a new branch, name it on the patch/feature you are working on:

```
$ cd python-forked
$ git checkout -b bugfix-unicode-strings
```

Work on `bugfix-unicode-strings` and make all the changes you want. And then do a push to your github account, which is usually `origin` remote:

```
$ git push origin bugfix-unicode-strings
```

And then send PR, to `master` branch of `guido/python`, with your branch `bugfix-unicode-strings`.

Now, tomorrow, guido may add new features and you might want to update your forked repo. It's simple, just pull from the `upstream` to `master` branch of `python-forked`

```
$ cd python-forked
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
```

### Update and PR

You have forked the project and maintainer has later moved on and added new features which you need in the current patch you are working on

You need to fetch the new changes from `upstream` and put those in your `patch` branch. While doing this, usually I update my master branch also:

```
$ cd python-forked
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git checkout existing-patch-I-am-working-on
$ git rebase master
```

You could also do `$ git rebase upstream/master` in last step to update the current patch branch. 

### Update, resolve conflicts and PR

You have forked the project and maintainer has made some changes to the file you are also working on

Fetch the changes and merge it with current patch branch you are working:

```
$ cd python-forked
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git checkout existing-patch-I-am-working-on-which-has-a-file-edited-by-guido
$ git rebase master
```

above rebase will fail(?) (or interrupted) and terminal will ask you to resolve the conflicts and then merge.

usually:

```
# solve the conflicts
$ git rebase --continue
```

### References

- Syncing a Fork - [link](https://help.github.com/articles/syncing-a-fork/)
- Merging an upstream repository into your fork - [link](https://help.github.com/articles/merging-an-upstream-repository-into-your-fork/)
- How to update a GitHub forked repository? - [link](http://stackoverflow.com/questions/7244321/how-to-update-a-github-forked-repository)
