---
title: Getting things to install for the correct shell in Mac OS X
date: '2009-11-24'
categories:
- computing
- os-x
- python
---
In addition to blogging about KAUST here, I\'m also going to post little useful tidbits related to scientific computing in OS X. Today I was setting up my new Mac Pro. After installing the [Enthought Python Distribution](http://www.enthought.com), I found that ipython was not in my path (and the python in my path was not the enthought-installed version).\
\
The culprit was the following: I had changed shells in Terminal\'s preferences to tcsh, but somehow the EPD installer didn\'t detect this and thought I was still using bash. Thus the modifications to my path were placed in \~/.bash_profile rather than in \~/.cshrc. That was easy enough to fix, but to avoid similar problems in the future, I opened a Terminal and typed\
\
chsh -s /bin/tcsh\
\
so that next time the installer would know my default shell.
