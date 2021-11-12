---
title: "Recurse Center Day 7: Basics of ncurses"
date: "2021-11-10T16:08:08+05:30"
categories: ["recurse-center", ""]
tags: ["recurse-center", "rc", "checkin"]
slug: "rc-day-7"
summary: "I learnt some basics of ncurses"
---

<div style="font-size: 0.7rem; margin: 1.2rem; padding: 0.5rem; background: #f7c9d0;"><p>This is a draft post that I have prematurely published. Currently, I am attending RC and I want to write as much as possible, log my daily learnings and activities. But, I also don't want to spend time on grammar and prose, so I am publishing all the posts which usually I'd have kept in my draft folder.</p></div>

## Ask stupid questions!

I read this lovely [article](https://www.nikitakazakov.com/ask-stupid-questions-as-software-developer) on asking stupid questions by Nikita Kazakov. A TLDR would be:

![](/blag/images/2021/ask-stupid-questions.png)


## B Tree

I started hand drawing the B Tree algorithm (I will add the pictures shortly), it immensely helped to understand the basics. Right now, I updated my code to do inserts in root and handle root splits.

## B Tree Invariants

I started making a small comic/drawing explaining the properties of B Tree. I will update it here.

## ncurses

I paired with Sarah today to work on her 2D 'Snake' game which is being written in C. We worked on a bug where it was not detecting the arrow keys properly. While doing that, I learned a couple of new things about ncurses and the terminal:

1. When arrows keys are pressed, they are displayed as `\033[A` (up), `\033[B` (down) etc. They are not multiple characters and the keyboard sends a single integer value representing them e.g. 259 (up), 258 (down) etc. These values could be OS specific, so better use the values from ncurses to match. Here is a sample program:

		#include <curses.h>
		int main() {
		  initscr();
		  keypad(stdscr, TRUE);
		  int c = getch();
		  if (c == KEY_UP) { // notice this KEY_UP? this comes from ncurses
		    printf("you pressed UP! (%d)\n", c);
		  }
		}

1. No need to load the key presses into char or any other data structure. Loading it into `int` is enough, it can capture the arrow keys
1. If you are on macOS, you need to call the `keypad` method, like shown in the snippet earlier. I found this info in [this Stackoverflow post](https://stackoverflow.com/questions/1182665/how-do-i-detect-arrow-keys-pressed-using-curses-in-c)
1. I found this nice article called [Interfacing with the key board](https://tldp.org/HOWTO/NCURSES-Programming-HOWTO/keys.html) which was very helpful. It comes with a sample program, that was enough to write my own
