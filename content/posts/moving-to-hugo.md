---
title: "Moving to Hugo"
date: "2020-11-29T10:58:48+05:30"
categories: ["", ""]
tags: ["pelican", "hugo", "notes"]
slug: "moving-to-hugo"
summary: "some personal notes to remember the migration effort from Pelican to Hugo"
---

I decided to migrate to Hugo from Pelican and here are some of the changes I made for the [migration](https://github.com/avinassh/avinassh.github.io/pull/2):

1. Wrote a [script](https://github.com/avinassh/pelican-to-hugo) which converted the post's metadata from Pelican to Hugo. Run the script by providing an arg with the contents directory:

		
		$ python3 script.py content
		

	this script runs over all the files ending with `.md` and converts it accordingly.

2. Next task was moving static assets like images, gifs which I had used. Since they were very few, I just moved them manually and updated my markdown.

I setup [Github Actions](https://github.com/avinassh/blag/blob/9883271408233130eb4e7b8ba6aab25d954ab55a/.github/workflows/development.yml) to automate the publishing process.