---
title: "Adding An Unique Index On A Large Collection in Mongo DB"
date: "2021-03-31T14:53:12+05:30"
categories: ["", ""]
tags: ["mongodb", "replication", "index"]
slug: "adding-unique-index-large-collection"
summary: ""
draft: true
---



This is a story of time, replication, and large amount of data.

Mongo nice to knows:

1. Max memory it uses is 500mb for indexing, this value can be changed. For WireTiger cache it is %50 of RAM. But memory didn't get free when the indexing was done. 
2. Mongo indexing is single threaded. Adding more CPU doesn't help
3. BG indexing can become FG if it crashes. There is a setting which lets you avoid this
4. When indexing crashes, it doesn't say for which record it crashed.
5. Mongo aggregation group stage, cannot use index
6. pipeline stages have limited memory, 100mb. use allowdiskusage

{
        "ok" : 0,
        "errmsg" : "E11000 duplicate key error collection: default_dobby.messages index: client_id_1_message_id_1 dup key: { : \"abhibus\", : \"014fa1f1-2a84-4858-ba66-ba5fa7f8a327\" }",
        "code" : 11000,
        "codeName" : "DuplicateKey"
}


 command default_database.$cmd appName: "MongoDB Shell" command: createIndexes { createIndexes: "messages", indexes: [ { key: { client_id: 1.0, message_id: 1.0 }, name: "client_id_1_message_id_1", unique: true } ], lsid: { id: UUID("e4ad1619-e297-4d47-9197-18730a585a3d") }, $db: "default_dobby" } numYields:0 ok:0 errMsg:"E11000 duplicate key error collection: default_dobby.messages index: client_id_1_message_id_1 dup key: { : \"amazon\", : \"014fa1f1-2a84-4858-ba66-ba5fa7f8a327\" }" errName:DuplicateKey errCode:11000 reslen:248 locks:{ Global: { acquireCount: { r: 2, w: 2 } }, Database: { acquireCount: { w: 2, W: 1 } }, Collection: { acquireCount: { w: 2 } } } storage:{ data: { bytesRead: 261599377193, timeReadingMicros: 2344482330 } } protocol:op_msg 4441860ms
 

create an subset and index:

a small sample:

db.messages.find({"message_updated_at": {"$gte": ISODate("2021-03-20T12:35:33.062Z")}}).count()

5843213

create it to another subset:

db.messages.aggregate([ { $match: {"message_updated_at": {"$gte": ISODate("2021-03-20T12:35:33.062Z")}} }, { $out: "subset" } ], {allowDiskUse: true, explain: true});

copy the indexes:

var indexes = db.messages.getIndexes();

indexes.forEach(function(index){
    if(index.name =='_id_'){
     print("we are skip the _id_ index")
    }
      else{
        delete index.v;
        delete index.ns;
        var key = index.key;
        delete index.key
        var options = {};
        for (var option in index) {
            options[option] = index[option]
        }
        options['background'] = true;
        printjson(key);
        printjson(options);
        db.msgs.createIndex(key, options);
    }
});


final aggr query:

db.messages.aggregate([
  { $group: {
    _id: { "message_id": "$message_id", "client_id": "$client_id" },
    "primary_keys": { "$push": "$_id" },
    count: { $sum: 1 },
  } },
  { $match: { 
    count: { $gte: 2 } 
  } },
  {$out: "dupes"}
], {
  allowDiskUse: true, explain: true
});

---

for profile data
use default_profile

db.user_data.aggregate([
  { "$match": {
      "user_confirmed.Phone": { "$exists": true, "$ne": null }
    } },
  { $group: {
    _id: { "phone": "$user_confirmed.Phone", "client_id": "$client_id" },
    "primary_keys": { "$push": "$_id" },
    count: { $sum: 1 },
  } },
  { $match: { 
    count: { $gte: 2 } 
  } },
  {$out: "dupes"}
], {
  allowDiskUse: true, explain: true
});

