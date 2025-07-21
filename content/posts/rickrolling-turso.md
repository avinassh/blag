---
title: "Rickrolling Turso DB (SQLite rewrite in Rust)"
date: "2025-07-20T23:06:59+05:30"
categories: ["database", ""]
tags: ["database", "db", "rust", "SQLite", "Turso"]
slug: "rickrolling-turso"
summary: "This is a beginner's guide to hacking into Turso DB (formerly known as Limbo), the SQLite rewrite in Rust. I will explore how to get familiar with Turso's codebase, tooling and tests"
---

This is a beginner's guide to hacking into [Turso DB](https://github.com/tursodatabase/turso) (formerly known as Limbo), the SQLite rewrite in Rust. In this short post, I will explore how to get familiar with Turso's codebase, tooling, and tests (hereafter mentioned as just Turso).

<small>Disclosure: I work in the same organization where Turso is being developed. However, I am not a contributor (yet) and most of my work is on the <a href="https://turso.tech/blog/a-deep-look-into-our-new-massive-multitenant-architecture">Turso Server</a>.</small>

I don't contribute to the Turso Database, but I am somewhat familiar with SQLite. I wanted to take Turso for a spin and explore the codebase. I timeboxed my experiment for 6 hours, including writing this blog post. Do note that Turso is under heavy development, so much so that core developers spend more time resolving merge conflicts than writing code. So expect most of the content in this blog post to get obsoleted by next month.

## Getting and Compiling

Turso is written in Rust. So getting the code and running it was fairly simple:

```bash
git clone git@github.com:tursodatabase/turso.git
cd turso

cargo run
   Compiling turso_cli v0.1.3-pre.3 (/turso/cli)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.74s
     Running `target/debug/tursodb`

Turso v0.1.3-pre.3
Enter ".help" for usage hints.
This software is ALPHA, only use for development, testing, and experimentation.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database
turso>
```

Side note: compiling and running SQLite is also simple, btw.

The big hurdle I find with large codebases is that I have no idea how to compile and get them to run. My background is not in systems programming. I really like how modern languages make it easy to compile and run something. Last time I tried `make build` on a large C codebase, I invoked Cthulhu and got a bunch of unrelated errors, and I had no idea how to solve any of them.

```
turso> create table t(v);
turso> insert into t values("answer to everything");
turso> select * from t;
┌──────────────────────┐
│ v                    │
├──────────────────────┤
│ answer to everything │
└──────────────────────┘
turso>
```

My goal was to hack the column to provide some custom value instead of whatever is inserted. Perhaps, `42`, the answer to everything.

## Some internals - `op_column`

To make this work, we need to figure out how a query is run and executed. How the db parses the bytes it fetched from disk into something meaningful. It all starts with a db connection, so we must first understand the entry point and lifecycle of a connection. The repo has a mermaid [diagram here](https://github.com/tursodatabase/turso/blob/main/docs/manual.md#appendix-a-limbo-internals) which explains the sequence of a query.

Knowing SQLite internals helps here. In short, SQLite has a VM interpreter. Every query statement is turned into a bunch of opcodes, then executed on this VM, called [VDBE](https://www.sqlite.org/opcode.html).

SQLite also has a command equivalent to the `EXPLAIN` query we see in most databases. It gives a breakdown of a query plan and how it is run:

```
turso> explain select * from t;
addr  opcode             p1    p2    p3    p4             p5  comment
----  -----------------  ----  ----  ----  -------------  --  -------
0     Init               0     7     0                    0   Start at 7
1     OpenRead           0     2     0                    0   table=t, root=2
2     Rewind             0     6     0                    0   Rewind table t
3       Column           0     0     1                    0   r[1]=t.v
4       ResultRow        1     1     0                    0   output=r[1]
5     Next               0     3     0                    0
6     Halt               0     0     0                    0
7     Transaction        0     0     0                    0   write=false
8     Goto               0     1     0                    0

turso>
```

Read [this post by Ben Johnson](https://fly.io/blog/sqlite-virtual-machine) to understand more about VDBE. Turso CLI also has an option to inspect any opcode:

```
turso> .opcodes Column

Column
-------
Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
(See the MakeRecord opcode for additional information about the format of the data.) Extract the
P2-th column from this record. If there are less than (P2+1) values in the record, extract a NULL.
The value extracted is stored in register P3. If the record contains fewer than P2 fields, then
extract a NULL. Or, if the P4 argument is a P4_MEM use the value of the P4 argument as the result.
If the OPFLAG_LENGTHARG bit is set in P5 then the result is guaranteed to only be used by the
length() function or the equivalent. The content of large blobs is not loaded, thus saving CPU
cycles. If the OPFLAG_TYPEOFARG bit is set then the result will only be used by the typeof()
function or the IS NULL or IS NOT NULL operators or the equivalent. In this case, all content
loading can be omitted.
```

In short, the `Column` opcode is the one which is responsible for converting the values fetched from disk to an in-memory data structure. So if I wanted to hack it, this is where I need to modify. But how do I find how this opcode is implemented?

Since this is a Rust codebase, I set `RUST_LOG=trace` and did `cargo run`. This spit out a bunch of log lines, walking through the VM execution. `RUST_LOG` env works for most, if not all, Rust projects; it is quite universal.

With some more exploration of the codebase, I found out the following:

1. The [`Connection` struct](https://github.com/tursodatabase/turso/blob/55b5e45231da9b38b4b05abf1f45dae88a33dbf7/core/lib.rs#L552-L573)
2. Once a connection is created, the SQL statement is parsed and executed [here](https://github.com/tursodatabase/turso/blob/55b5e45231da9b38b4b05abf1f45dae88a33dbf7/core/lib.rs#L577) and [here](https://github.com/tursodatabase/turso/blob/55b5e45231da9b38b4b05abf1f45dae88a33dbf7/core/lib.rs#L637).
3. [`translate_select`](https://github.com/tursodatabase/turso/blob/be0a607ba8efeb041f2b28b82a32e5e74438c18f/core/translate/select.rs#L27-L26) generates the bytecode VM instructions
4. `op_column` is implemented [here](https://github.com/tursodatabase/turso/blob/6506b3147d7ccc328553ab96e37b5613888a2d07/core/vdbe/execute.rs#L1357-L1363)
5. The [Program builder](http://github.com/tursodatabase/turso/blob/bbd7f32d80aa0284bd703e3bc69984c3f427f0df/core/vdbe/mod.rs#L371) runs the VM

With all this info, I modified the `op_column` to do just this:

```rust
state.registers[*dest] = Register::Value(Value::Integer(42));
state.pc += 1;
return Ok(InsnFunctionStepResult::Step);
```

and it worked!

```
turso> insert into t values("answer to everything");
turso>
turso> select * from t;
┌────┐
│ v  │
├────┤
│ 42 │
└────┘
turso>
```

But there is one big issue: how do I retrieve my data when I want to?

## PRAGMA

SQLite lets you configure the database using [PRAGMA statements](https://www.sqlite.org/pragma.html). We are lucky today; Turso already supports them. Now I need to figure out how to hook up PRAGMA with the connection and use that when executing from the VM. This turned out to be easy too, as `Program` would have access to the `Connection`. So I added the flag in the `Connection` struct.

We want to add a new PRAGMA, something that is not supported by SQLite yet. So we need to first modify the parser to consider our pragma. Then we need to update this flag to enable/disable. But this turned out to be much simpler than I expected. I added the new PRAGMA [here](https://github.com/tursodatabase/turso/blob/6506b3147d7ccc328553ab96e37b5613888a2d07/vendored/sqlite3-parser/src/parser/ast/mod.rs#L1745), then fixed everywhere the Rust compiler complained.

## Tests

There are a bunch of bugs with this little hack. I also wanted to play with the DST (Deterministic Simulation Tests). To run the simulator, you can do:

```
cargo run -p limbo_sim
```

This runs the simulator till it finds a bug or till the end of time. But unfortunately, my time ran out, so I stopped my experiment. So next steps would be:

1. Fix the bugs and add tests in the simulator
2. Selectively enable this feature(?) for some specific columns
3. Add the same in SQLite. I notice a lot of method names in Turso to be similar to SQLite, so we could follow the same path
4. Explore adding the same in Postgres or MySQL (or try failing)

## Demo Time

Finally, here is the demo. You can share this special build with your frens and whatever song they insert, they will always get their favourite song back ;)

<img src="/blag/images/2025/sqlite-rick-roll.gif"/>

Here are [all my changes](https://github.com/avinassh/limbo/pull/1) to run and play this.

Though I am biased, I think Turso DB is a great project for someone new to jump into databases and start contributing. Rust makes it so accessible and easy to hack. If this post interested you, here are [some good first issues](https://github.com/tursodatabase/turso/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22).

---
<small>1. Trivia: Db's experimental experimental name was Ligma, written in Zig. Later it was rewritten to Rust and renamed to Limbo.</small><br>
<small>2. The blog posts and the linked papers have some more details on SQLite's internals: [How bloom filters made SQLite 10x faster
](https://avi.im/blag/2024/sqlite-past-present-future/) and [In search of a faster SQLite](https://avi.im/blag/2024/faster-sqlite/).</small><br>
