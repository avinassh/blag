---
title: "Marshaling Struct with Special Fields to JSON in Golang"
date: "2021-05-01T14:35:53+05:30"
categories: ["golang", "json", "serialisation"]
tags: ["json", "serialisation", "marshal"]
slug: "golang-marshaling-special-fields"
summary: "This is a short post explaining how I marshaled http.Request into json"
---

I needed to marshal `http.Request` to json, but this struct contains few fields which are not serialise-able. Here is [some sample code](https://play.golang.org/p/CTIQXEUnxfn):

```go 
// imports and error handling is omitted for brevity
func main() {
    req, _ := http.NewRequest("GET", "http://example.com", nil)
    _, err := json.Marshal(req)
    fmt.Println(err)
}
```

When you run the above code, we get an error:

```go
json: unsupported type: func() (io.ReadCloser, error)
```

So I inspected [the struct](https://golang.org/pkg/net/http/#Request), found out that it has two fields which json doesn't know how to serialize:

```go
// in net/http
type Request struct {
    // snipped
    GetBody func() (io.ReadCloser, error)
    Cancel <-chan struct{}
}
```

I [wrote a wrapper struct](https://play.golang.org/p/84b1fFkUzLM) in which I embedded the `http.Request` object, redefined these fields. Do note that the json struct tags need to match with the corresponding fields from `http.Request`:

```go
type RequestWrapper struct {
    GetBody string `json:"GetBody,omitempty"` // the type doesn't really matter, since I
    Cancel  string `json:"Cancel,omitempty"` // don't want them in my final json output
    *http.Request
}

func main() {
    req, _ := http.NewRequest("GET", "http://example.com", nil)
    reqWrapper := &RequestWrapper{req}
    out, _ := json.Marshal(reqWrapper)
    fmt.Println(string(out))
}
```

This works nicely! But lets test the same with an HTTP request containing body:

```go
func main() {
    req, _ := http.NewRequest("POST", "http://example.com", strings.NewReader("Hello, World!"))
    reqWrapper := &RequestWrapper{Request: req}
    out, _ := json.Marshal(reqWrapper)
    fmt.Println(string(out))
}
```

Uh oh! we see that request body isn't marshaled correctly:

```python
{
    "Body": {"Reader": {}},
    // snipped
}
```

`Body` field is of type `io.ReadCloser`. While serialising JSON doesn't throw any error, but it doesn't know how to serialise it either. So, we will slightly modify our struct:


```go
type RequestWrapper struct {
    Body    string `json:"Body,omitempty"`   // this assumes body is always string
    GetBody string `json:"GetBody,omitempty"` // the type doesn't really matter, since I
    Cancel  string `json:"Cancel,omitempty"` // don't want them in my final json output
    *http.Request
}
```

Then we read the body, assign it to this newly added field:

```go
func main() {
    req, _ := http.NewRequest("POST", "http://example.com", strings.NewReader("Hello, World!"))
    body, _ := ioutil.ReadAll(req.Body)
    reqWrapper := &RequestWrapper{Request: req, Body: string(body)}
    out, _ := json.Marshal(reqWrapper)
    fmt.Println(string(out))
}
```

[This](https://play.golang.org/p/lq9touQZq_F) works perfectly!

## Bonus

The same can be achieved by implementing `MarshalJSON()` on the `RequestWrapper`, which I find it to be cleaner:

```go
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "strings"
)

type RequestWrapper struct {
    *http.Request
}

func (r *RequestWrapper) MarshalJSON() ([]byte, error) {
    body, _ := ioutil.ReadAll(r.Request.Body)
    return json.Marshal(&struct {
        Body    string `json:"Body,omitempty"`
        GetBody string `json:"GetBody,omitempty"`
        Cancel  string `json:"Cancel,omitempty"`
        *http.Request
    }{
        Body:  string(body),
        Request: r.Request,
    })
}

func main() {
    req, _ := http.NewRequest("POST", "http://example.com", strings.NewReader("Hello, World!"))
    reqWrapper := &RequestWrapper{Request: req}
    out, _ := json.Marshal(reqWrapper)
    fmt.Println(string(out))
}
```

### Note

If you are passing around this request object, then the next method won't be able to read the body. In that case, buffer needs to be refilled:

```go
body, _ := ioutil.ReadAll(req.Body)
// then assign an `io.ReadCloser` back to it
req.Body = ioutil.NopCloser(bytes.NewBuffer(body))
```
