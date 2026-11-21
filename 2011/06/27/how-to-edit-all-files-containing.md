---
title: How to edit all files containing a particular string
date: '2011-06-27'
categories:
- linux
- programming
---
It\'s often useful to be able to automatically open all files with a particular string (say, to rename a variable throughout your code). To do this with ack, and open all files containing my_string in vim, just type:\
\
vim \$(ack -l my_string)\
\
It can be accomplished in a similar way with grep instead of ack.\
\
\
**Edit:** If you just want to search and replace a particular string in all files under some directory recursively, use\
\
grep -rl matchstring somedir/ \| xargs sed -i \"\" \'s/search string1/search string2/\'\
\
It took me a while to find that the double quotes after -i are necessary on Mac OS X. And be aware that the single quotes above usually get mangled to be backticks when copying and pasting.\
\
**Edit 2:** Don\'t do this in the root directory of a git repository! It will corrupt the repository.
