---
title: 'My favorite new tool: ack'
date: '2011-05-24'
categories:
- tools
- UNIX
---
If you\'re like me, about once a week you type something like\
\
\>\> grep words\
\
and then wait a few seconds before remembering that you really meant\
\
\>\> grep words \*\
\
or perhaps\
\
\>\> grep -r words \*\
\
If so, do yourself a favor and install **[ack](https://betterthangrep.com/)** right now. You\'ll be glad you did.\
\
Note: ack tries to intelligently search only filetypes that it believes to be text. Unfortunately, its built-in list of extensions for such files is incomplete. For instance, it does not include .rst (ReStructured Text) files. To add more extensions, just create a file \".ackrc\" in your home directory and put the following line in it:\
\
\--type-add=TYPE=.ext\
\
Here TYPE is the name of the filetype (anything you want) and .ext is the extension of that filetype. For example:\
\
\--type-add=RST=.rst\
\
(in the line above, \"type\" is preceded by two minus characters. Unfortunately, they look strange in my blog\'s font).
