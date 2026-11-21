---
title: Python code for making a histogram of your e-mail volume
date: '2011-02-07'
categories:
- e-mail
- python
---
Here is the source code for the example in my last post. I haven\'t had time to clean it up, and some parts are not very elegant. But if you want to try it out with your own inbox, all you need to do is change the e-mail address and run it.\
\
Three caveats:\
1. If you need to download a large number of e-mail headers, it will take some time (maybe several minutes).\
2. It sometimes gets the dates wrong. However, this seems to occur only in a statistically insignificant fraction of cases.\
3. Running this will mark all the messages it accesses as read. I\'m sure there\'s a way to avoid this, but haven\'t had time to track it down.\
\

```{=html}
<script src="https://gist.github.com/815049.js"></script>
```
