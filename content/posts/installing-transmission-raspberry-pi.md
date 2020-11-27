---
title: "Installing Transmission (remote and CLI) client on Raspberry Pi "
date: "2013-12-05T10:20:00+05:30"
lastmod: "2014-09-02T19:30:00+05:30"
categories: ["tutorial"]
tags: ["raspberry-pi", "transmission"]
slug: "installing-transmission-raspberry-pi"
description: "This tutorial will explain you how to install Transmission client on Raspberry Pi running Raspbian."
---

I have found [Transmission](http://www.transmissionbt.com/) to be best client to run on Raspberry Pi. In this tutorial I will explain how to install Transmission and access it using it's web interface over browser. 

Though this tutorial is for Raspberry Pi, it should work for any computer running Debian flavour. 

First run these commands to update and upgrade the packages you have installed. 

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install transmission-daemon

Create a directory where you will be saving the downloads. I have always connected a HDD to Pi and that's where all my downloads go. Fix the path accordingly. 

    mkdir /media/my_passport/downloads

Run the following commands which grants access to the download directory and also adds current user to `transmission-daeomon` group:

    sudo chown debian-transmission:debian-transmission /media/my_passport/downloads
    sudo usermod -a -G debian-transmission <user>
    sudo chmod 770 /media/my_passport/downloads


Before making any changes, make sure you are stopping the Transmission client. The config file resides at `/etc/transmission-daemon/settings.json`. Make changes to it as per your requirements. To make some changes:

    sudo service transmission-daemon stop
    sudo nano /etc/transmission-daemon/settings.json

Above should show you Nano editor, where you can edit the config file. Once done, press `Ctrl + O` (Control plus Oh) to save and `Ctrl + X` to exit Nano editor. Some of the changes I make are:
    
    "download-dir": "/media/my_passport/downloads",
    ...
    ...
    "rpc-authentication-required": true,
    "rpc-bind-address": "0.0.0.0",
    "rpc-enabled": true,
    "rpc-password": "password",
    "rpc-port": 9091,
    "rpc-url": "/transmission/",
    "rpc-username": "avi",
    "rpc-whitelist": "127.0.0.1, 192.168.*.*",
    "rpc-whitelist-enabled": false,

Make sure you keep a strong password and the file is valid json. Or else Transmission client won't start. You can check the validity of json file on [JSON Lint](http://jsonlint.com/).

### How to start/stop/restart Transmission client:

- to start:
 
        sudo service transmission-daemon start

- to stop:

        sudo service transmission-daemon stop

- to restart:

        sudo service transmission-daemon restart


### How to access Transmission in Web Browser:

Transmission web client starts on port 9091 by default. Check:

    http://<raspberry_pi_ip_address>:9091