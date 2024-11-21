---
title: "Go Error Handling"
date: "2022-08-31T15:04:30+05:30"
categories: ["", ""]
tags: ["", ""]
slug: "go-error-handling"
summary: ""
---

```go
func get(key string)(*User, error){
	var item User
	err := cache.get(key, &item)
	return &item, err
}
```

this is wrong cos caller might check only the objects and not interested in the errors since its a caching call. Following is better:

```go
func get(key string)(*User, error){
	var item User
	err := cache.get(key, &item)
	if if err != nil {
		return nil, err
	}
	return &item, nil
}
```

the caller wasn't interested in the errors:

```go
user, _ := get(key)
if user != nil {
	return user, nil
}
```

ideally, it should have been:

```go
user, err := get(key)
if err != nil {
	return user, nil
}
```