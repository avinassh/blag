---
title: "It is faster to compute 64 bit hash and truncate it to 32 bit than computing 32 bit hash in twox hash"
date: "2025-09-20T10:13:10+05:30"
categories: ["", ""]
tags: ["", ""]
slug: "64-bit-hash"
summary: ""
---

My good fren [Alex Miller] mentioned to me once that it is faster to compute a 64 bit hash, truncate it to 32 bits than computing the 32 bit hash in twox hash algorithm. I finally got around to benchmark it and here are some numbers:

```
================================================================================
XXHash Benchmark Results
================================================================================

Size           XXHash32       XXHash64    Speedup   Faster
------------------------------------------------------------
16B              1.5 ns         1.4 ns      1.05x    XXH64
64B              4.0 ns         4.3 ns      0.93x    XXH32
256B              16 ns          11 ns      1.40x    XXH64
512B              35 ns          21 ns      1.63x    XXH64
1KB               74 ns          39 ns      1.91x    XXH64
4KB              319 ns         159 ns      2.00x    XXH64
64KB            5.19 μs        2.57 μs      2.02x    XXH64
16KB            1.28 μs         641 ns      2.00x    XXH64
256KB           21.0 μs        10.3 μs      2.03x    XXH64
1MB             83.5 μs        41.4 μs      2.02x    XXH64
4MB              334 μs         166 μs      2.01x    XXH64
64MB            5.42 ms        2.69 ms      2.02x    XXH64
16MB            1.34 ms         671 μs      2.00x    XXH64
256MB           21.6 ms        10.8 ms      2.00x    XXH64
```

```
Latency by data size:
----------------------------------------
   16B:     1.5 ns →     1.4 ns  (1.05x faster)
   64B:     4.0 ns →     4.3 ns  (0.93x faster)
  256B:      16 ns →      11 ns  (1.40x faster)
   1KB:      74 ns →      39 ns  (1.91x faster)
  16KB:    1.28 μs →     641 ns  (2.00x faster)
  64KB:    5.19 μs →    2.57 μs  (2.02x faster)
 256KB:    21.0 μs →    10.3 μs  (2.03x faster)
   1MB:    83.5 μs →    41.4 μs  (2.02x faster)
  16MB:    1.34 ms →     671 μs  (2.00x faster)
  64MB:    5.42 ms →    2.69 ms  (2.02x faster)
 256MB:    21.6 ms →    10.8 ms  (2.00x faster)
```

```
Throughput (1MB data):
----------------------------------------
XXHash32:              11980 MB/s
XXHash64 truncated:    24183 MB/s
Improvement:           101.9%
```

It's literally 2x fast! But wait, we can do better. Twox hash also has a xx3 variant, that's 4x fast lol11!

```
====================================================================================================
XXHash Benchmark Results
====================================================================================================

Size             XXH64→32      XXH3-64→32       XXH3-128→32
-----------------------------------------------------------------------------------
16B              1.4 ns         1.0 ns         1.6 ns
64B              4.4 ns         2.7 ns         3.5 ns
256B              12 ns         6.1 ns         8.1 ns
512B              21 ns          11 ns          12 ns
1KB               39 ns          21 ns          23 ns
64KB            2.58 μs        1.37 μs        1.36 μs
4KB              161 ns          85 ns          85 ns
16KB            653 ns         342 ns         341 ns
256KB           10.4 μs        5.48 μs        5.44 μs
1MB             41.8 μs        21.8 μs        21.7 μs
64MB            2.69 ms        1.40 ms        1.40 ms
4MB              166 μs        86.9 μs        87.3 μs
16MB            674 μs         349 μs         350 μs
256MB           10.7 ms        5.60 ms        5.58 ms
```

```
====================================================================================================
Performance Summary (1MB data)
====================================================================================================

Latency and Throughput:
--------------------------------------------------
XXH3-128          21.7 μs      45982 MB/s
XXH3-64           21.8 μs      45950 MB/s
XXH64             41.5 μs      24113 MB/s
XXH32             83.6 μs      11955 MB/s

Relative Performance:
--------------------------------------------------
XXH3-128       3.85x faster than XXH32
XXH3-64        3.84x faster than XXH32
XXH64          2.02x faster than XXH32
XXH32          baseline
```

## Why

- 64 bit hardware
- m

## Lessons

1. Listen to your frens
1. Always measure and use what's suitable for your needs
