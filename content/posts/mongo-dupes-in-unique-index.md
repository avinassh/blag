---
title: "I ended up adding duplicate records on a unique index in MongoDB"
date: "2021-03-31T19:51:35+05:30"
categories: ["database", "mongodb", "replication"]
tags: ["database", "mongodb", "replication"]
slug: "mongo-dupes-in-unique-index"
summary: "how my curiosity lead me to discover a weird inconsistency with MongoDB where I was able to insert records that conflicted the index constraints"
thumbnail: "images/2021/mongo-unique-index-oops.png"
---

<small>Note: The intention of this post is not to shit on MongoDB. They specifically forbid the steps I am about to explain. This post is a chronicle of my curiosity, exploration, and fun learning experience. If you still find it interesting, then continue to read on (:</small>

In MongoDB (or generally in any database), the following rules apply when it comes to the unique indexes:

1. You cannot add duplicate records which violate the unique constraints
2. If there is a collection that has duplicate records, then you cannot add a unique index to the collection unless you delete those dupes first

Yet, I ended up breaking these set rules and bringing my MongoDB in a weird state in which: 

1. The secondary was replicating from the primary with data which conflicted the unique index constraints (breaking the rule 1)
2. I was able to have a unique index with data that conflicted the unique constraints (breaking the rule 2)

## The Problem

I have a three node cluster, with a primary and two secondaries. If you want to create an index on a large collection, MongoDB docs suggest you do something called [Rolling Index Builds](https://docs.mongodb.com/v4.0/tutorial/build-indexes-on-replica-sets/):

1. Remove a member from the replica set
2. Create the index
3. Add the follower back to the replica set
4. Repeat for all the followers
5. Make the primary to step down and let some other followers become the primary
6. Then create the index on the last remaining follower (the earlier primary)

However, these steps change when you want to create a unique index. The Mongo docs specifically highlight this:

> To create [unique indexes](https://docs.mongodb.com/v4.0/core/index-unique/#index-type-unique) using the following procedure, you must stop all writes to the collection during this procedure.
> 
> If you cannot stop all writes to the collection during this procedure, do not use the procedure on this page. Instead, build your unique index on the collection by issuing [db.collection.createIndex()](https://docs.mongodb.com/v4.0/reference/method/db.collection.createIndex/#db.collection.createIndex) on the primary for a replica set.

Mongo has two modes of creating indexes:

1. Foreground: This uses more efficient data structures, but this [blocks all read, write operations](https://docs.mongodb.com/v4.0/faq/indexes/#how-does-an-index-build-affect-database-performance) on the collection while the index is being built. This is not good if you don't want to have downtime. There are [ways to speed this process up](https://docs.mongodb.com/v4.0/reference/parameters/#param.maxIndexBuildMemoryUsageMegabytes), but Mongo index creation process is [single threaded](https://jira.mongodb.org/browse/SERVER-676). Ouch.
2. Background: This runs in the background, but uses an inefficient index data structure and also, this is very very slow. No way to speed this up.

I measured and both of them were terrible. Foreground mode took about 3 hours (with the maximum RAM I could add in Google Cloud). Background indexing took about 18 hours on a single replica. The constraints apply only when the index is fully built. During the index creation if dupes get inserted, then the whole [index process will be aborted](https://docs.mongodb.com/v4.0/core/index-creation/#interrupted-index-builds) and needs to be restarted again. (The older version of Mongo had a nice option of specifying dropping the dupes during index creation.)

I disliked both and I was tempted to try the Rolling Index builds for the unique indexes, the very thing which Mongo docs forbade. The docs said 'do not do this', but did not say what would happen if someone did it. Of course, I had to take one for the team and try it.

## The (Anti) Solution

I diligently followed the instructions given [here](https://docs.mongodb.com/v4.0/tutorial/build-indexes-on-replica-sets/#a-stop-one-secondary-and-restart-as-a-standalone) and took out one of the followers. This was simple, I had to change the mongod config (usually located at `/etc/mongod.conf`):

```yaml
net:
   bindIp: localhost
   port: 27217
#   port: 27017
#replication:
#   replSetName: myRepl
setParameter:
   disableLogicalSessionCacheRefresh: true
// snipped conf file
``` 

Then I built an unique index on a collection:

```javascript
> db.records.createIndex({user: 1}, {unique: true})
{
	"createdCollectionAutomatically" : false,
	"numIndexesBefore" : 1,
	"numIndexesAfter" : 2,
	"ok" : 1
}
```

While the index was being built, I inserted a duplicate document in the primary. Since primary did not have any indexes, it happily obliged to my commands:

```javascript
rs0:PRIMARY> db.records.insert({user: "avi"})
WriteResult({ "nInserted" : 1 })
```

I undid the conf file changes in the secondary and added it back to the replica set, crossed my fingers, and asked my friends to guess what would happen:

1. The new follower would be rejected because it has an index which primary isn't aware of
1. The unrecognised index would be dropped silently from the secondary
1. The replication will be failing in a loop whenever it encountered the duplicate record from the primary
2. The replication would complete successfully, dropping the duplicate records silently

<!-- so yeah, Mishraji and DC, you were both wrong. ha ha. -->

But, as you have guessed already, none of these things happened. The follower was welcomed into the replica set and replication completed successfully. I first checked the primary, if there were any new indexes. Rightly so, there were none. I checked the secondary if the unique index had gotten dropped. But nope. 

Then the following blew my mind:

```javascript
rs0:SECONDARY> db.records.getIndexes()
{ "v" : 2, "unique" : true, "key" : { "user" : 1 }, "name" : "user_1" }
// snipped output
rs0:SECONDARY> db.records.find()
{ "_id" : ObjectId("6066e0f278d5455b08f3920b"), "user" : "avi" }
{ "_id" : ObjectId("6066e80385a02d98945e380e"), "user" : "avi" }
```

Then I forced this particular secondary to become the primary. The index existed and it wasn't replicated to other nodes, as expected. When I tried to insert dupes, it failed:

```javascript
db.records.insert({user: "avi"})
WriteResult({
	"nInserted" : 0,
	"writeError" : {
		"code" : 11000,
		"errmsg" : "E11000 duplicate key error collection: users.records index: user_1 dup key: { : \"avi\" }"
	}
})
```

I made this new primary step down and I inserted dupes again from the primary. Checked them happily being replicated into the secondary:

```javascript
rs0:SECONDARY> db.records.find()
{ "_id" : ObjectId("6066e0f278d5455b08f3920b"), "user" : "avi" }
{ "_id" : ObjectId("6066e80385a02d98945e380e"), "user" : "avi" }
{ "_id" : ObjectId("6066ea3b85a02d98945e380f"), "user" : "avi" }
rs0:SECONDARY> db.records.getIndexes()
{ "v" : 2, "unique" : true, "key" : { "user" : 1 }, "name" : "user_1" }
// snipped output
```

### Bonus

<script id="asciicast-cHfzvlc3Rpkd6JqSJCLetgZTM" src="https://asciinema.org/a/cHfzvlc3Rpkd6JqSJCLetgZTM.js" async></script>

---

<small>1. This post references Mongo DB v4.0, the version I was using. However, this behaviour exists in the latest version of v4.4 as well.</small><br>
<small>2. The index creation mechanisms have greatly improved in the newer versions of [Mongo DB, starting with 4.2](https://docs.mongodb.com/v4.2/core/index-creation/).</small>