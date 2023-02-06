---
title: "It is becoming difficult for me to be productive in Python"
date: "2023-02-05T17:56:57+05:30"
categories: ["rant", ""]
tags: ["python", "go"]
slug: "refactoring-python"
summary: ""
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #d8d1d2;"><p>Note: Following blog post more or less applies to any dynamically typed programming language, e.g. Ruby. I am only sharing my experience and frustrations with Python, cos that's the language I use.</p></div>

I started learning to program with Python, which holds a special place in my heart. It's the language which taught me how to think about programming, modelling a problem to code and communicate with the machine. I was hired at my current job (or the previous one) because of Python. I was a fanboy and evangelist. I spent a lot of time in Python communities, learning and helping others. When I started mentoring beginners to code, Python was my choice of language.

I distinctly remember having the following conversation with a friend:

> Friend: C# makes life a lot easier with types
>
> Me: I haven't had the need. Are they needed?
>
> Friend: But how do you deal with functions that can take any type of argument?
> 
> Me: I have unit tests and high test coverage. A small change will catch any changes. Also, you add documentation on functions explaining what they do and the type of arguments they expect. Easy peasy.

Oh boy, how wrong I was. At that time, I had shipped code to production in Python, but there were few users. I did not have experience with other languages.

When I joined my current startup (a team of 3 developers), I started learning Go. I had the responsibility of building a few services. I picked Python for a few because I was most comfortable with it, and I could ship fast. Django was better suited for some of the problems. Indeed, I could ship fast and build some services that are still in use.

In a couple of months, I had stopped writing any new Python. Go was used for new services, and I started contributing them, including some that would be the core, crucial ones. This was many years back. I was still learning Python on the side, e.g. when async came; I upgraded one of [my side projects](https://github.com/avinassh/haxor) to use it.

We upgraded some internal APIs and libraries a few months ago, and a few Python services needed updates. I was eager to work with Python again, but my enthusiasm faded quickly.

## Guess Driven Development

The first issue I faced was understanding the code. It took a sweet amount of time to figure out the kind of objects, things certain functions were receiving and what they were doing with them. The code did have some unit tests, but the coverage was poor. So I had to guess, make changes and test the code at many places.

I could not get hints in my IDE for a few modules. It became a habit to keep the source file open in another tab and refer every time for any new code I was writing. Without type (or type hints), I had no idea how to use a function. A language with type makes a lot of difference when refactoring; one glance at the signature, and I know what to do.

After all the guessing game and refactoring, how do I ensure my changes work effectively? The only way to be sure is by running the code and verifying that every line is executed under all possible combinations. 

Years of coding in Go gave me this comfortable feeling: if it compiles, it works. (Rust takes it to the next level; if it compiles, you won't have memory issues or data races.) The compilation gives quick feedback, which makes it very easy to make changes.

## Unit tests and type hints

Type hints solve these issues to some extent, [but bugs](https://twitter.com/iavins/status/1524407933982765056) can still slip through. Unit testing is the way to go. However, this is not always possible, for instance, when enforcing rules within a team is difficult or when inheriting a legacy project. But does enforcing strict rules work in practice? You could set up CI/CD pipeline enforcing 100% code coverage, but that will affect team productivity and surely piss off people.

I want a system where the chances of making mistakes are minimal. I can achieve that with unit tests and CI/CD pipelines. But type safety provides me that by default.

What I have learnt is the real world is not perfect. Having codebases without comments, documentation, and unit tests is common. Some of these are inevitable when working in a team with large codebases. In such cases, working in Python becomes a huge pain.

## Is Python fast to ship? 

With typed languages, I used to think, ugh, I'd have to define types everywhere, make struct (or classes) in advance, and sometimes make wild guesses because those things were unknown or not finalised. All of these are valid complaints. If I am prototyping in Rust, I will take a lot of time. With Python, I can ship fast. But only once. 

Refactoring involves reading the existing code, understanding it and then making changes. Types are like free documentation. For me, it's hard to understand and reason about the code without them. Types give me the confidence to make minor changes quickly and ensure they work fine when the code compiles.

I am finding it painful to refactor in Python. I can't even complain that someone else wrote it. I only wrote that code years ago! I could mitigate these issues with type hints and unit tests. But is it fast to ship if I spend so much time doing all these?

Static languages have an initial one-time cost. I find it similar to TDD. But your future self will thank you. If I am touching a project after years, I'd rather wish it was in a typed language. I have written some interesting stuff in Python, [like one](https://github.com/avinassh/fast-sqlite3-inserts) or [this one](https://github.com/avinassh/py-caskdb). I will continue to learn and use it for my side projects. But I am going to dread working on a large Python codebase.

<small><i>Thanks to Hari, Nihar, and Sumesh for reading a draft of this.</i></small>

---

<small>1. I found [this post](https://davidlebech.com/thoughtflow/guess-driven-development/) coining Guess-driven development: *Bad programmers spend much of that 90% debugging code by randomly making changes and seeing if they work.*</small><br>
<small>2. Yes, I will not miss the meta-programming features, many of them felt like voodoo to me anyways, and I'd like to avoid voodoo in my codebase.</small>