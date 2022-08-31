---
title: "Go Pipe Reduce Mem"
date: "2022-08-31T15:46:41+05:30"
categories: ["", ""]
tags: ["", ""]
slug: "go-pipe-reduce-mem"
summary: ""
---

using Go Pipe to reduce memory usage

https://old.reddit.com/r/golang/comments/x1pl2u/optimizing_your_go_programs_with_continuous/

https://www.polarsignals.com/blog/posts/2022/08/30/optimizing-with-continuous-profiling/

https://github.com/polarsignals/frostdb/pull/161

old code:

```go
data, err := t.Serialize()
if err != nil {
	return err
}
return Upload(ctx, fileName, bytes.NewReader(data))
```

new code:

```go
r, w := io.Pipe()
var err error
go func() {
	defer w.Close()
	err = t.Serialize(w)
}()
defer r.Close()

return Upload(ctx, fileName, r)
```

here the serialiser method would write to `w` instead of returning the whole array. And upload would just write to the filename