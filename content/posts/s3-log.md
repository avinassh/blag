---
title: "Building a distributed log using S3 (under 150 lines of Go)"
date: "2024-11-30T23:16:21+05:30"
categories: ["distributed systems"]
tags: ["database", "distributed systems", "infrastructure", "disaggregated storage", "zero disk", "diskless", "wal", "log"]
slug: "s3-log"
summary: ""
---

I will show how we can implement a durable, distributed, and highly available log using S3. This post is the third part in the series:

1. [Disaggregated Storage - a brief introduction](https://avi.im/blag/2024/disaggregated-storage/)
2. [Zero Disk Architecture](https://avi.im/blag/2024/zero-disk-architecture/)
3. Building a distributed log using S3

tl;dr The code is open source, comes with some tests and open issues to contribute: [s3-log](https://github.com/avinassh/s3-log)

## Log

I love logs. The log is the heart of data and event streaming systems. A database is a log. Kafka is a log. Simply put, it's an ordered collection of records. The log is append-only, and once records are written, they are immutable. Each inserted record gets a unique, sequentially increasing identifier.

Log is a powerful storage abstraction. Using a log, you can build a database, message queue, or an event streaming system. If you would like to learn more, read this excellent blog post by Jay Kreps, the creator of Kafka: [The Log: What every software engineer should know about real-time data's unifying abstraction](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying).

## Why S3?

In my previous post, I explained the benefits of [Zero Disk Architecture](https://avi.im/blag/2024/zero-disk-architecture/). A log on S3 is attractive for several reasons:

1. No disks, so it is elastic and scalable.
2. We don't have to roll our own distributed storage server. We get durability, availability, and replication for free just by using S3.
3. No operational overhead.
4. Cost. Systems like [WarpStream](https://www.warpstream.com/bring-your-own-cloud-kafka-data-streaming) and [BufStream](https://buf.build/blog/bufstream-kafka-lower-cost) claim to be 10x cheaper than Kafka.
5. Customers and enterprises love BYOC! You make $$$

## The Log Interface

```go
type Record struct {
	Offset uint64
	Data   []byte
}

type WAL interface {
	Append(ctx context.Context, data []byte) (uint64, error)
	Read(ctx context.Context, offset uint64) (Record, error)
}
```

We will write each payload as an object in S3 and make sure that it gets a unique offset in the log.

We need to make sure that record numbers are unique, and are sequentially increasing.

### Append

The only 'write' operation we can do on a log is `Append`. Append takes a bunch of bytes, writes that to end of the log. It returns the `offset` the position of this record on the log.

Let's define a struct which maintains a counter `length` and every time we insert, we will increment this counter by one.

```go
type S3WAL struct {
	client     *s3.Client
	bucketName string
	length     uint64
}
```

The very first record will have offset as `0000000001`, every new object we insert in the S3 bucket we will increment it by one. Once a record is inserted, we will return its offset to the caller. 

```go
func (w *S3WAL) Append(ctx context.Context, data []byte) (uint64, error) {
	nextOffset := w.length + 1

	input := &s3.PutObjectInput{
		Bucket:      aws.String(w.bucketName),
		Key:         aws.String(fmt.Sprintf("%020d", nextOffset)),
		Body:        bytes.NewReader(data),
		IfNoneMatch: aws.String("*"),
	}

	if _, err := w.client.PutObject(ctx, input); err != nil {
		return 0, fmt.Errorf("failed to put object to S3: %w", err)
	}
	w.length = nextOffset
	return nextOffset, nil
}
```

How do we prevent two writers appending records with same offset? This is one of the crucial property of a log. Using S3 Conditional Write it is very simple. That's why we have added `IfNoneMatch: aws.String("*")` in the request. If an object already exists with the same record offset, the request will be rejected. Let's write a basic test to confirm this:

```go
func TestSameOffset(t *testing.T) {
	wal, cleanup := getWAL(t)
	defer cleanup()
	ctx := context.Background()
	data := []byte("threads are evil")
	_, err := wal.Append(ctx, data)
	if err != nil {
		t.Fatalf("failed to append first record: %v", err)
	}

	// reset the WAL counter so that it uses the same offset
	wal.length = 0
	_, err = wal.Append(ctx, data)
	if err == nil {
		t.Error("expected error when appending at same offset, got nil")
	}
}
```

You might be thinking, why not use S3's latest feature appends and write to the same object? We can certainly do that, but it is tricky to get right since a zombie writer might come back and append to an old object while a new leader might be writing to a new file. Unlike typical Raft based storage systems, S3 does not have a concept of fencing tokens. I left this optimisation to tackle it later.

I have also kept the sequencing simpler and consider no gaps. If we allow gaps, it might be possible for a zombie writer to write to some old sequence number. There are ways to prevent this, but thats a problem for another day! (note to self: I should probably write another blog post with these problems)

### Checksums

S3 provides 99.99999999% durability. But like a sane man, I would never trust an external system for data integrity. [Most databases don't do checksums](https://avi.im/blag/2024/databases-checksum/), but we can do better. For now, let's use sha-256 for checksums (go std lib has it). So, let's store offset, the data and the checksum.

By storing offset we make the record self contained. For e.g. if we do compaction tomorrow and change file names, the record's offset remains same.

```go
func calculateChecksum(buf *bytes.Buffer) [32]byte {
	return sha256.Sum256(buf.Bytes())
}

func prepareBody(offset uint64, data []byte) ([]byte, error) {
	// 8 bytes for offset, len(data) bytes for data, 32 bytes for checksum
	bufferLen := 8 + len(data) + 32
	buf := bytes.NewBuffer(make([]byte, 0, bufferLen))
	binary.Write(buf, binary.BigEndian, offset)
	buf.Write(data)
	checksum := calculateChecksum(buf)
	_, err := buf.Write(checksum[:])
	return buf.Bytes(), err
}
```

### Read

Our log is coming along nicely! Let's implement the read. It's straightforward. Given an offset, we will construct the appropriate S3 object name and fetch it:

```go
func (w *S3WAL) Read(ctx context.Context, offset uint64) (Record, error) {
	key := w.getObjectKey(offset)
	input := &s3.GetObjectInput{
		Bucket: aws.String(w.bucketName),
		Key:    aws.String(key),
	}
	result, _ := w.client.GetObject(ctx, input)
	defer result.Body.Close()

	data, _ := io.ReadAll(result.Body)
	if len(data) < 40 {
		return Record{}, fmt.Errorf("invalid record: data too short")
	}
	if !validateOffset(data, offset) {
		return Record{}, fmt.Errorf("offset mismatch")
	}
	if !validateChecksum(data) {
		return Record{}, fmt.Errorf("checksum mismatch")
	}
	return Record{
		Offset: offset,
		Data:   data[8 : len(data)-32],
	}, nil
}
```

We will do a couple of validations:

1. The record has to be minimum 40 bytes
2. The offset in the request should match the one with request
3. The checksums should match

### Failover / Crash Recovery

Now that we have our basic operations working, let's handle failure scenarios. What if our node crashes? How do we recover it? We always initialize our WAL with length 0. Subsequently, new writes will try to write at `0000000001` offset. This is not a catastrophic bug! S3 conditional writes protect us and reject the writes. However, we will not be able to proceed with new writes. Let's fix this. Let's add a method which goes through the list of keys, finds the last inserted object. There are a couple of [ways to optimize this](https://github.com/avinassh/s3-log/issues/1), but let's iterate through all the keys:

```go
type WAL interface {
	LastRecord(ctx context.Context) (Record, error)
}

func (w *S3WAL) LastRecord(ctx context.Context) (Record, error) {
	input := &s3.ListObjectsV2Input{
		Bucket: aws.String(w.bucketName),
	}
	paginator := s3.NewListObjectsV2Paginator(w.client, input)

	var maxOffset uint64 = 0
	for paginator.HasMorePages() {
		output, _ := paginator.NextPage(ctx)
		for _, obj := range output.Contents {
			key := *obj.Key
			offset, _ := w.getOffsetFromKey(key)
			if offset > maxOffset {
				maxOffset = offset
			}
		}
	}
	if maxOffset == 0 {
		return Record{}, fmt.Errorf("WAL is empty")
	}
	w.length = maxOffset
	return w.Read(ctx, maxOffset)
}
```

That's it! The project is open source: [s3-log](https://github.com/avinassh/s3-log). You can check the code and some [tests here](https://github.com/avinassh/s3-log/blob/master/s3_wal_test.go). There are a couple of open issues if you'd like to contribute!

<small>open issues: [improving LastRecord](https://github.com/avinassh/s3-log/issues/1), [cache](https://github.com/avinassh/s3-log/issues/2), [batch write](https://github.com/avinassh/s3-log/issues/3), [buffered write](https://github.com/avinassh/s3-log/issues/4)</small>.

---

<small>1. Any object store would work. But I like S3.</small><br>
<small>2. Yes, a database is a log.</small><br>
<small>3. I'm not surprised that Jay Krepps ended up loving logs so much he wrote a book [I Heart Logs]().</small><br>
<small>4. [Threads are evil](https://x.com/iavins/status/1860299083056849098)</small><br>
<small>5. My fren read this post and asked me, instead of S3, can I use Kafka and store my records there? You definitely can. But running Kafka is not easy. Hosted Kafka is way more expensive than S3. Moreover, you build Kafka like systems using a log. Going other way around is recursive.</small><br>
