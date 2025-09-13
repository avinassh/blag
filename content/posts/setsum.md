---
title: "Setsum - order agnostic, additive, subtractive checksum"
date: "2025-09-12T22:49:24+05:30"
categories: ["correctness"]
tags: ["databases", "correctness", "verification", "checksum", "replication"]
slug: "setsum"
summary: "A brief introduction to Setsum - order agnostic, additive, subtractive checksum"
---

Setsum is an order agnostic, commutative checksum. It was developed by [Robert Escriva](https://rescrv.net) at Dropbox's metadata team. In this short post, I'll explain why they're used and the math behind them. Jump to the end if you'd like to see the code.

## Introduction

Say you're building a database replication system. The primary sends logical operations to replicas, which apply them in order:

```json
{"op": "add", "id": "apple"}
{"op": "add", "id": "apple"}
{"op": "remove", "id": "orange"}
```

After the replica processes these changes (add two apples, remove an orange), how do you verify both nodes ended up in the same state?

One naive (rather horrible) approach is to dump both states and compare them directly. It's expensive, impractical, and doesn't scale. Instead, you can maintain checksums that update with each operation. When you're done, just compare the checksums; if they match, you're in sync. That's why distributed databases like Cassandra use Merkle trees for the same purpose.

Setsum is similar but has some nice properties that make it attractive over Merkle trees. They can be computed incrementally; the cost only depends on the change being applied, not the whole dataset. I also find them attractive because they let you remove items as well.

## Properties

Setsum has some interesting properties:

**1. Order doesn't matter.** Both of these yield the same result:
```rust
s1 = New()
s1.add("apple")
s1.add("banana")

s2 = New()
s2.add("banana")
s2.add("apple")

assert_eq(s1, s2)
```

**2. You can remove items.** These are equivalent:
```rust
s1.add("apple")
s1.add("banana")
s1.remove("apple")

s2.add("banana")
s2.add("banana")
s2.remove("banana")

assert_eq(s1, s2)
```

**3. You can combine setsums.** As you guessed already, these are equal:
```rust
s1.add("apple")
s1.add("banana")
s2.add("chikoo")

s3.add("banana")
s3.add("chikoo")
s3.add("apple")

assert_eq(s1+s2, s3)
```

The only state you need to maintain is 256 bits, and all operations are `O(len(msg))` instead of depending on your entire dataset.

## The internals

Each Setsum is an array of 8 unsigned 32-bit integers (u32), called "columns". Each column starts at 0 when you create a new Setsum. Each column has an associated large prime number (close to `u32::MAX`).

When you add an item:

* Compute the SHA3-256 hash of the item (produces 32 bytes)
* Split the hash into 8 chunks of 4 bytes each
* Interpret each chunk as a little-endian u32
* Add each number to its corresponding column
* If the sum exceeds the column's prime, store the remainder (mod prime)

You can also remove an item that was previously added. The magic is in computing the inverse: first, derive the inverse of the item's hashed value, then add that inverse to the setsum. This effectively cancels out the original, removing the item from the set!

To compute the inverse, we use modular arithmetic: it's simply the prime minus the value.

## The math behind setsum

Disclaimer: If we're friends, you already know I'm no math person. If not, hey there, new friend! You can probably skip this if you understand modulo arithmetic, the Chinese remainder theorem, and a bit of probability.

Let's simplify: instead of 8 columns, let's use just one. The prime number for this column is 29. Consider adding these items with their hash and inverse values:

| Item        | Hash | Inverse |
|-------------|------|---------|
| apple       | 15   | 14      |
| banana      | 23   | 6       |
| chikoo      | 7    | 22      |
| pomegranate | 18   | 11      |
| watermelon  | 26   | 3       |

<br>
Notice that all hash values stay below the prime. If a hash exceeds it, we take the remainder. For example, if `guava` hashes to 33, the final value would be 4 (33 mod 29). Also, hash + inverse always equals the prime.

Let's add some items:

```rust
s = 0
s = 15 (add apple - 15)
s = 9 (add banana - 23)
s = 16 (add chikoo - 7)
```

Let's try in some random order:

```rust
s = 0
s = 7 (add chikoo - 7)
s = 22 (add apple - 15)
s = 16 (add banana - 23) // see, this ends up same!
```

Let's try removal. Note that for removal we add the inverse values:

```rust
s = 0
s = 15 (add apple - 15)
s = 9 (add banana - 23)
s = 27 (add pomegranate - 18)
s = 12 (remove apple - 14)
s = 18 (remove banana - 6)
s = 25 (add chikoo - 7)
```

```rust
s = 0
s = 18 (add pomegranate)
s = 25 (add chikoo) // whoa 🤯
```

I cherry-picked these examples to demonstrate setsum, but there's a flaw in the above examples. Can you spot it?

Consider this collision:
```rust
s = 0
s = 15  (add apple - 15)
s = 22  (add chikoo - 7)
```
```rust
s = 0
s = 18  (add pomegranate - 18)
s = 22  (add guava - 4)
```

Both sets of completely different items sum to 22! This happens because we're only using one column and a very small prime number. But add another column and the collision probability drops dramatically. With 8 columns, the probability of collision drops to <sup>1</sup>/<sub>2<sup>256</sup></sub>.

Setsum also uses SHA3-256 as its hash function, though the hash algorithm is replaceable. SHA3-256 is fast, has fewer collisions, and produces well-distributed hashes, so we can avoid the collision problem I showed above.

## Observations

1. Setsum can tell you if states diverged, but not where. To narrow things down, you can split your data into smaller chunks and compare those. Build this into a hierarchical structure and you're basically back to something like a Merkle tree.

2. You can remove items that never existed. This might or might not be a problem depending on your use case. Given that you're only maintaining 256 bits of state, it's a reasonable tradeoff.

3. There's no history tracking. You can't tell when or how states diverged, just that they did.

## Code

The original Rust implementation is [here](https://github.com/rescrv/blue/tree/main/setsum). I ported it to Go, with all the same tests - [setsum](https://github.com/avinassh/setsum).

---

<small>1. I found out about setsum from Chroma's excellent post [wal3: A Write-Ahead Log for Chroma, Built on Object Storage](https://trychroma.com/engineering/wal3) and got nerd sniped into writing this blog post</small><br>
<small>2. This is a good post: [Using Merkle trees to detect inconsistencies in Cassandra](https://distributeddatastore.blogspot.com/2013/07/cassandra-using-merkle-trees-to-detect.html)

<small><i>Thanks to toc2, and General Bruh for reading an early draft of this post.</i></small>
