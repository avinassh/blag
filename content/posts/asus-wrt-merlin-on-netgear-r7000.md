---
title: "Flashing Asus-WRT Merlin by XVortex on NetGear NightHawk R7000"
date: "2015-05-10T22:20:00+05:30"
categories: ["tutorial"]
tags: ["r7000", "asus-wrt"]
slug: "asus-wrt-merlin-on-netgear-r7000"
description: "This tutorial will explain you how to flash Asus-WRT Merlin by XVortex on NetGear NightHawk R7000."
---

### Note:
There are many ways to achieve this and in this tutorial I follow two flash method. 

### Preparation:

- This guide assumes you are on stock firmware.
- If you are already on DD WRT or Tomato, ignore step 2 of procedure.
- Doesn't matter whether you are on Windows, Linux or Mac. Everything happens in browser
- Make sure you are connected to the router over one of WAN ports
- It doesn't matter which firmware version you are currently on. My router came with `V1.0.3.XX`, which I later upgraded to `V1.0.4.28_1.1.64`.
- Download these two files:
    1. Tomato Initial CHK file (`.chk`), which upgrades your NetGear firmware to Tomato - [link](http://tomato.groov.pl/download/K26ARM/Netgear%20R-series%20initial%20files/tomato-R7000-initial.chk).
    2. XWRT TRX file (`.trx`), which upgrades Tomato to XVortex's AsusWRT-Merlin (the thing you finally want). Current latest version is `v378.53_0`. The zip file contains `.chk` and `.trx` files, you can ignore the `.chk` for this guide - [link](http://mega.co.nz/#!lllgHBpT!oFGLRxwtkXgeijqgvDYRwbKh48gG9yGJLhsQefvJEGI).

### Procedure:

1. Login to your router. Reset it to factory settings (`Advanced` > `Administration` > `Backup Settings` > `Revert to factory default settings`).
2. Flash the `.chk` file, after this procedure firmware will be upgraded to Tomato. (`Advanced` > `Administration` > `Router Update` > `Browse` > `Apply`)
3. Now flash the `.trx` file which upgrades to XVortex's Firmware. You will see 'successful' message at end.
4. Now if your router is not being detected, do manual reboot of the router.
5. Connect to the router, if there are any IP conflicts it will be displayed. It should now show you the Installation Wizard. Either follow it or skip it. But it will require you to set the WPA creds.
6. Do another reset (`Administration` > `Restore/Save/Upload Setting` > `Factory default` OR `http://<router_ip_address>/Advanced_SettingBackup_Content.asp`).
7. Repeat step 4 if necessary.
8. Follow the installation wizard at your wish, same as in step 5.

That's all!! :D

### Post installation:

To set TX power to 30%-50%, for both bands:

1. Go to `Wireless` > `Professional` > `Tx power adjustment` (or `http://<router_ip_address>/Advanced_WAdvanced_Content.asp`).
2. Set `Tx power adjustment` to 30% - 50%.
3. Change `Band` to 5Ghz and do step 2 again.

Hope this helps.

### Credits:

Check [this thread](http://www.linksysinfo.org/index.php?threads/asuswrt-merlin-on-netgear-r7000.71108/page-5#post-261251) where I originally wrote this tutorial. Thanks to @XVortex for this fine firmware. Thanks to @slidermike who actually introduced me to this, or else I was going to try Tomato. Thanks to @ManiDhillon, @freibooter and @mito for answering my noobie questions and giving me instructions.