---
title: "PSA: SQLite does not do checksums"
date: "2024-11-09T12:56:46+05:30"
categories: ["database", ""]
tags: ["sqlite", "checksum", "bit rot", "database", "corruption"]
slug: "sqlite-bit-flip"
summary: "SQLite does not do checksums by default. Disk corruptions go silently unnoticed."
---

SQLite does not do checksums by default. I learned this from [Alex Miller](https://fosstodon.org/@AlexMillerDB/109553692861357766). What does this mean? If there is disk corruption, the database or application won't be able to know that the database is 'corrupt'.

Even a single bit flip can cause havoc. This can happen due to a faulty disk, a bug in the disk driver, or when another application (malicious or otherwise) modifies the database files.

This is not a bug - it's properly documented:

> SQLite assumes that the detection and/or correction of bit errors caused by cosmic rays, thermal noise, quantum fluctuations, device driver bugs, or other mechanisms, is the responsibility of the underlying hardware and operating system. SQLite does not add any redundancy to the database file for the purpose of detecting corruption or I/O errors. SQLite assumes that the data it reads is exactly the same data that it previously wrote.

I created a [simple script](https://gist.github.com/avinassh/0e7e4b0578136a338f1b9a03fba36ead) to demonstrate this:

1. Create a sample database using [this script](https://gist.github.com/avinassh/0e7e4b0578136a338f1b9a03fba36ead). It creates a bank database and adds a row for Alice with $83K.

2. Flip a single bit:

		printf '\x00\x00\x00\x00\x00\x80' | dd of=bank.db bs=1 seek=$((0x1ffd)) count=1 conv=notrunc

3. Alice's balance is now zero. Sorry, Alice.

It passes `PRAGMA integrity_check` too. Here's an ASCII animation if you prefer that:

<script src="https://asciinema.org/a/688119.js" id="asciicast-688119" async="true"></script>

## WAL and Checksums

SQLite has checksums for WAL frames. However, when it detects a corrupt frame, it silently ignores the faulty frame and all subsequent frames. It doesn't even raise an error!

Ignoring frames might be acceptable, but not raising an error is where it gets me.

## Checksum VFS Shim

You can use the [Checksum VFS Shim](https://www.sqlite.org/cksumvfs.html), but there's one important caveat:

> Checksumming only works on databases that have a reserve bytes value of exactly 8

The [documentation of reserve bytes](https://www.sqlite.org/fileformat2.html#resbyte) explains:

> SQLite has the ability to set aside a small number of extra bytes at the end of every page for use by extensions. These extra bytes are used, for example, by the SQLite Encryption Extension to store a nonce and/or cryptographic checksum associated with each page. The "reserved space" size in the 1-byte integer at offset 20 is the number of bytes of space at the end of each page to reserve for extensions. This value is usually 0. The value can be odd.

This means if you're using any extension that uses reserve bytes, you can't use the Checksum shim.

Again, this is not a bug. [Most databases (except a few)](https://avi.im/blag/2024/databases-checksum) assume that the OS, filesystem, and disk are sound. Whether this matters depends on your application and the guarantees you need.

edit: I wrote a [follow up post](https://avi.im/blag/2024/databases-checksum).

---

This post has gone more viral than I anticipated! I don't have SoundCloud, but consider joining my [Telegram](https://t.me/databases_v) or [WhatsApp](https://www.whatsapp.com/channel/0029VaC5Qe72P59b63Qozt0c) where I post database internals content.