---
title: "Staying Ahead of Amazon, in Amazon Treasure Hunt Contest"
date: "2015-10-31T22:20:00+05:30"
categories: ["code"]
tags: ["hacking"]
slug: "amazon-treasure-hunt"
description: "With a simple Man In The Middle (MITM) attack, I tried to cheat(?) one of Amazon India's contest."
---

Last week Amazon India had a Treasure Hunt contest which ran for a whole week. The contest was simple, from 10am to 6pm, every hour Amazon would display a clue (image) and you had to guess the product. That particular product would be on sale for ₹1, which also included shipping cost anywhere in India. The contest was app only i.e. image also would be displayed in the app and you had to buy using the app.

<img src="{filename}/images/2015/amazon-treasure/makeymakey1.jpg" alt="makey makey offer page" style="width: 50%;"/><img src="{filename}/images/2015/amazon-treasure/makeymakey2.jpg" alt="makey makey cart" style="width: 50%;"/>

Above images show [Makey Makey](http://www.amazon.in/dp/B008SFLEPE/) on promo.

Problem was, too many people were participating in the contest and by the time you could guess the product, search it in the app and add to your cart, it would be out of stock. Because quantity of the product on sale was only one. So you had to be very very quick.

Using [MITM](https://mitmproxy.org/), I started monitoring the API calls. In one of the calls, I found out the request which was asking for the contest image:

    https://images-eu.ssl-images-amazon.com/images/G/31/img13/mshop/treasure/clues-20/Clue5._UX828_SX828_V290896415_.png

At the time of this writing, above link is still active. In case Amazon removes it, you can check the [archived link](https://archive.is/tpoLd). This clue leads to [Canon Powershot SX400](http://www.amazon.in/dp/B00NPSTO42/) and it was actually sold for ₹1.

I changed string `Clue5` to `Clue6` (after other trial and errors) and I had access to the next clue, even before the contest was live:

    https://images-eu.ssl-images-amazon.com/images/G/31/img13/mshop/treasure/clues-20/Clue6._UX828_SX828_V290896415_.png

Here's the [archived link](https://archive.is/3tlhv). Now all I had do was increase the value and get all images. 

The clues did not require any authentication or special headers (and that's how [archive.is](https://archive.is) is able to GET and archive it).
