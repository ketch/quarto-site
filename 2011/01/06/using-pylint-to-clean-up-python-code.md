---
title: Using pylint to clean up Python code
date: '2011-01-06'
categories:
- programming
- pylint
- python
---
I just recently discovered a very useful package for anyone who writes python code: [pylint](https://pypi.python.org/pypi/pylint). It took a little tweaking to get it to do what I wanted. Besides looking for outright errors, it checks all the recommended Python coding style conventions. Since I don\'t abide by many of those, pylint gave my [nodepy](https://web.kaust.edu.sa/faculty/davidketcheson/NodePy/) code a rating of -4.5/10.0 (yes, that\'s a NEGATIVE rating) initially. More importantly, I couldn\'t find the real errors among the thousands of style complaints. To run pylint without checking all the style conventions, just type\
\
`pylint -d C xxxx`\
\
where \"xxxx\" is the name of a python package or module. It will still make a lot of subjective judgments about your code (like suggesting that no function should have more than 5 arguments), but to me it\'s a tolerable level (and sometimes the suggestions really are helpful). More information about pylint\'s output messages can be found here: [https://www.logilab.org/card/pylintfeatures.](https://www.logilab.org/card/pylintfeatures) I was able to uncover several previously unnoticed issues in my package in this way.
