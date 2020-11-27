---
title: "Scraping Javascript page using Python"
date: "2014-10-18T14:03:00+05:30"
categories: ["code"]
tags: ["python", "scraping"]
slug: "scraping-javascript-website-python"
description: "Simple code example to illustrate scraping a javascript driven website, using Python and Dryscape."
---

Python library [dryscape][1] can be used to scrape javascript driven websites. 

# Code

To give an example, I created a sample page with following HTML code. ([link][2]):

    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Javascript scraping test</title>
    </head>
    <body>
      <p id='intro-text'>No javascript support</p>
      <script>
         document.getElementById('intro-text').innerHTML = 'Yay! Supports javascript';
      </script> 
    </body>
    </html>

without javascript it says: `No javascript support` and with javascript: `Yay! Supports javascript`

## Scraping without JS support:

    >>> import requests
    >>> from bs4 import BeautifulSoup
    >>> response = requests.get(my_url)
    >>> soup = BeautifulSoup(response.text)
    >>> soup.find(id="intro-text")
    <p id="intro-text">No javascript support</p>

## Scraping with JS support:

    >>> import dryscrape
    >>> from bs4 import BeautifulSoup
    >>> session = dryscrape.Session()
    >>> session.visit(my_url)
    >>> response = session.body()
    >>> soup = BeautifulSoup(response)
    >>> soup.find(id="intro-text")
    <p id="intro-text">Yay! Supports javascript</p>


  [1]: https://github.com/niklasb/dryscrape
  [2]: http://avi.im/stuff/js-or-no-js.html
