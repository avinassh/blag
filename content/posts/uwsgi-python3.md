---
title: "Using uWSGI with Python 3"
date: "2015-12-18T14:03:00+05:30"
categories: ["code"]
tags: ["python", "django", "web", "self-notes"]
slug: "uwsgi-python3"
description: "Simple steps to get uWSGI up and running in Python 3."
---

Gevent does not have Python 3 support yet, but its available as a release candidate. So this will lead to problems if you use the latest stable Gevent with Python 3. Follow these simple steps to install uSWGI and Gevent properly for Python 3. 

1. Uninstall existing uWSGI:

        pip uninstall uwsgi
        pip3 uninstall uwsgi

2. Install everything via `pip3` and use Gevent v1.1rc3:

        pip install gevent==1.1rc3
        pip install uwsgi

Note: Above instructions will be obsolete once Gevent stable has Python 3 support.

## Update 06/12/2016:

Gevent now supports Python 3, so just do:

    pip3 install gevent
    pip3 install uwsgi