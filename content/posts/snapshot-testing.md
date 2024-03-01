---
title: "Snapshot Testing"
date: "2024-03-01T18:52:48+05:30"
categories: ["testing", ""]
tags: ["insta", "rust", "snapshot"]
slug: "snapshot-testing"
summary: "A smoll intro to snapshot testing"
---

Snapshot testing makes it easy to compare large outputs from a function. Instead of asserting against the raw output directly:

```rust
assert_eq!(my_really_large_6mb_string, my_func());
```

you save the expected output in a file and compare against that. But manually saving, loading, and comparing snapshot files is a lot of work! Snapshot testing frameworks make this process easy. In Rust, I have used [insta](https://crates.io/crates/insta):

```rust
assert_debug_snapshot!(my_func());
```

I don't need to explicitly save or load snapshot files. The framework handles it automatically!

The workflow is:

1. Write a test and include the assert macro.
2. Since this is the first run, there is no snapshot file yet. The framework generates one.
3. [Optional] Modify the snapshot file as needed.
4. Run the tests again - now the framework will compare against the saved snapshot and the test will pass.
5. If there is a regression or intentional change to the output, running the tests will generate a new snapshot file. The old one is preserved so you can review the change.

You may check my [pull request](https://github.com/tursodatabase/libsql/pull/1117) on libsql-server which adds a bunch of snapshot tests. 

Jane Street has a nice blog post on the same - [What if writing tests was a joyful experience?](https://blog.janestreet.com/the-joy-of-expect-tests/).