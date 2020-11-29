---
title: "Catching SIGTERM in Python"
date: "2016-02-20T17:03:00+05:30"
categories: ["code"]
tags: ["python", "process"]
slug: "sigterm-in-python"
summary: "Simple code example to show catching SIGTERM in a Python script."
---

I needed a very simple SIGTERM handler in a script I was working on. It is very simple to do so in Python, add a handler method and 'register' it. 

First define a handler method:

    def sigterm_handler(signal, frame):
        # this method defines the handler i.e. what to do
        # when you receive a SIGTERM
        pass

And register the handler:

    # Register the handler and let the process know that 
    # there is a handler for SIGTERM
    signal.signal(signal.SIGTERM, sigterm_handler) 

Here's a simple script, if it receives `kill` then it saves current state and exits gracefully. Here's a full working code:

    import signal
    import sys
    import time


    def sigterm_handler(signal, frame):
        # save the state here or do whatever you want
        print('booyah! bye bye')
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)


    def main():
        for i in range(100):
            print(i)
            time.sleep(i)


    if __name__ == '__main__':
        main()

Run the above script and send KILL, like

    $ kill <PID here>

it will print `'booyah! bye bye'` in terminal.

### References

Python 3 docs on `signal` - [link](https://docs.python.org/3.5/library/signal.html)