---
title: "Want a Fast 32-bit Hash? Compute 64 bits"
date: "2025-09-20T10:13:10+05:30"
categories: ["", ""]
tags: ["", ""]
slug: "64-bit-hash"
summary: ""
---

My good fren [Alex Miller] mentioned to me once that it's faster to compute a 64-bit hash and truncate it to 32 bits than to compute the 32-bit hash directly (in the xxHash algorithm). I finally got around to benchmarking it, and here's what I found.

## Numbers

Here's throughput on 1MB of data. `XXH64 → 32` means `XXH64` used to generate 64 bit and then truncated to 32 bits, and so on:

| Algorithm | Throughput | vs XXH32 |
|-----------|-----------|----------|
| XXH32 | 11,955 MB/s | baseline |
| XXH64 → 32 | 24,113 MB/s | 2.0x |
| XXH3-64 → 32 | 45,950 MB/s | 3.8x |
| XXH3-128 → 32 | 45,982 MB/s | 3.9x |

XXH64 is twice as fast as XXH32. And the XXH3 variant is nearly 4x faster.

Here are some latency numbers with different datasizes:

| Size | XXH32 | XXH64 | XXH3-64 |
|------|-------|-------|---------|
| 16B | 1.5 ns | 1.4 ns | 1.0 ns |
| 1KB | 74 ns | 39 ns | 21 ns |
| 64KB | 5.19 μs | 2.57 μs | 1.37 μs |
| 1MB | 83.5 μs | 41.4 μs | 21.8 μs |
| 256MB | 21.6 ms | 10.8 ms | 5.60 ms |

## Why

After talking with some experts, here is what I learned: These algorithms are optimised for modern 64-bit hardware. XXH64 processes 32 bytes per loop iteration using 64-bit arithmetic, while XXH32 processes 16 bytes with 32-bit ops. XXH3, the fastest of them, goes further with SIMD instructions (AVX2/NEON), processing even larger chunks in parallel. The algorithm is doing more work per cycle, so you get more throughput—even if you throw away half the bits at the end.

## Quality (and safety)

xxHash is a non-cryptographic hash, so truncation is safe. But I wanted to check how truncation affects the hash quality. A good hash should have strong avalanche behavior: flipping any single input bit should flip each output bit with 50% probability. Avalanche bias measures deviation from this ideal; lower is better.

I ran [HashEvals](https://github.com/ashvardanian/HashEvals) to check:

| Hash | Avg Bias | Worst Bias |
|------|----------|------------|
| XXH3-64 → upper 32 | 0.14% | 3.3% |
| FoldHash | 0.20% | 4.9% |
| XXH3-64 → lower 32 | 0.20% | 5.1% |
| XXH3 (full 64-bit) | 0.20% | 5.1% |
| StringZilla | 0.22% | 5.5% |
| aHash | 0.26% | 6.6% |
| CRC32 (for reference) | 15.9% | 37.5% |

The truncated variants perform as well as (or slightly better than) the full 64-bit hash and other popular alternatives. CRC32 is included to show what poor avalanche looks like (it's designed for error detection, not general hashing).

## Lessons

1. Use XXH3 and truncate, it is fine most of the time™️
1. Listen to your frens
1. Always measure and use what's suitable for your needs

---

<small>1. All the measurements done on my M4 Macbook Pro, they took awful lot of time for quality test</small>
