---
title: "Time in Programming"
date: "2022-03-28T20:09:31+05:30"
categories: ["programming", ""]
tags: ["", ""]
slug: "timezones"
summary: "my experience of using time in programming"
---

- Usage of time for created_at, updated_at
- Use UTC for past events
- ISO format does not capture location / timezone detail, only offset
- However, a multiple timezones can have same offset, so it would be difficult to capture timezone info from the ISO format
- The offsets can change for a timezone
- Timezone can change for a location too
- For recurring events, never save the data in UTC!
- Usage: Recurring Outreach/Campaign -- saved in UTC
- Business Hours: Saved with Timezone info, but not location

CppCon 2015: Greg Miller “Time Programming Fundamentals"
: https://www.youtube.com/watch?v=2rnIHsqABfM

https://docs.google.com/presentation/d/1H1tkvg_vm39jXPZbOvQLoWb32POSpTYiZx8qMtBvdSQ/pub?slide=id.gdf572321f_0_0

https://old.reddit.com/r/programming/comments/toui47/saving_time_in_utc_doesnt_work_and_offsets_arent/

https://swizec.com/blog/saving-time-in-utc-doesnt-work-and-offsets-arent-enough/


---

the oldest time/date supported by Databases? 

for e.g. using Django, datetime older than 1800 breaks