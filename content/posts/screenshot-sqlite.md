---
title: "Taking screenshot of a SQLite DB"
date: "2025-07-24T18:08:26+05:30"
categories: ["database", ""]
tags: ["SQLite", "db", "backup", "screenshot"]
slug: "screenshot-sqlite"
summary: "Here is how we can take a screenshot of the SQLite DB"
---

At the start of 2025, I [tweeted](https://x.com/iavins/status/1870133868826669175) the following meme:

<img src="/blag/images/2025/screenshot-meme.png" alt="screenshot meme" style="width: 80%;"/>

Then I realised, this joke is actually possible with SQLite. SQLite is too amazing, lol. So I will explain how we do that in the following post. We will literally store our DB data in a screenshot and hack into SQLite's VFS layer so that it can read and write from that screenshot. Here is the [code](https://github.com/avinassh/screenshot-db) if you are in a hurry, and scroll down for the quick demo.

## SQLite I/O and VFS

SQLite has a VFS (Virtual File System) layer which is an interface for OS operations. All the disk I/O is done via this layer. The query engine calls this layer for I/O, and this layer is responsible for reading from the disk and writing reliably to the disk.

You can register multiple VFSs and also provide your own custom VFSs. In fact, SQLite works this way internally too. For Unix and Windows, there are separate VFS libraries.

VFSs are stackable. That is, you can chain multiple VFS layers. For example, checksums and encryption are implemented via VFS. The layers above won't even know that the DB is encrypted.

SQLite's VFS documentation is excellent. Not only do they explain how to write one, but the source code also comes with a bunch of example VFS shims. For the purpose of this article, we are interested in the following [IO methods](https://www.sqlite.org/c3ref/io_methods.html) which we will implement:

```c
int (*xRead)(sqlite3_file*, void*, int iAmt, sqlite3_int64 iOfst);
int (*xWrite)(sqlite3_file*, const void*, int iAmt, sqlite3_int64 iOfst);
```

Our interface should have `xRead` and `xWrite` methods which take a pointer to the SQLite file, a buffer, and the offset. In `xRead`, we will fill the buffer at the specified offset. Similarly, in `xWrite` we will write the buffer contents at the offset.

So the key idea is that we will write our own VFS shim, which intercepts these read/write calls and performs them on the screenshot image. But then how do we store this data in an image?

## PNG File Format

<img src="/blag/images/2025/png-file-format.svg" alt="png file format" style="width: 70%;"/>

We will use a PNG file to store the DB pages. Internally, a PNG file is just a sequence of well defined chunks. Each chunk has: 4-byte length, 4-byte type, length bytes of payload, 4-byte CRC of the type + payload.

<img src="/blag/images/2025/png-chunk-structure.svg" alt="png chunk structure" style="width: 60%;"/>

The accepted types are `IHDR`, `PLTE`, `IDAT`, and `IEND`. The file must start with an 8-byte signature: `89 50 4E 47 0D 0A 1A 0A` immediately followed by an `IHDR` chunk. Then any number of `IDAT` chunks and must end with an `IEND` chunk. `PLTE` is an optional chunk; it must come before `IDAT` chunks. Typically, you have a single `IDAT` chunk instead of multiple ones. This consumes less storage space too.

The types I mentioned earlier are called critical chunks. PNG also has something called ancillary chunks which let us create custom chunks. There are some standard ancillary chunks like `tEXt`, `zTXt`, etc. Ancillary chunks can come before or after the `IDAT` chunks.

So our trick is we will create a chunk called `ruSt` to store SQLite's pages. The spongebob case here is deliberate due to naming rules. I had to debug to find that out.

## SQLite 🤝 PNG

<img src="/blag/images/2025/pngvfs.svg" alt="png as sqlite vfs" style="width: 90%;"/>

The SQLite VFS operates in offsets as you can see from the `xRead` / `xWrite` signature. All we need to do is calculate the page number from the offset requested, then search for that page in the PNG. Note that the PNG VFS layer assumes fixed 4096-byte sized pages:

```rust
let page_num = (offset / PAGE_SIZE as u64) as usize;
let offset_in_page = (offset % PAGE_SIZE as u64) as usize;
```

Note that we could save the entire SQLite file as a single chunk in the PNG. But this is highly inefficient, because a single write would result in writing the entire DB file to disk (i.e., yuge write amplification), and we would need to compute the checksum for the entire database every time.

SQLite doesn't do checksums by default. Since we keep checksums per chunk, this PNG file storing SQLite pages is more resilient in detecting corruption than SQLite itself.

## Bootstrapping and Usage

I built a handy CLI tool for quick bootstrapping. We are going to take an existing SQLite DB, create chunks from the pages, and then save them in a PNG file. We will store checksums to make sure that the data doesn't get corrupted.

```sh
cargo run --release -- bootstrap --image meme.png --db universe.db --out magic.png

✓ Successfully embedded 8192 bytes as 2 page(s) into magic.png
```

Then we can use our custom VFS to query and make inserts in this PNG file:

```sh
$ sqlite3

SQLite version 3.51.1
sqlite> .load ./target/release/libpngvfs
sqlite> .open file:magic.png?vfs=png
sqlite> SELECT * FROM oracle;
what is the answer to everything?|42
sqlite> insert into oracle values('it works?', 1);
```

## Demo

<img src="/blag/images/2025/screenshot-db-demo.gif" alt="screenshot db demo" style="width: 90%;"/>

## Code

The code is here: [screenshot-db](https://github.com/avinassh/screenshot-db)
