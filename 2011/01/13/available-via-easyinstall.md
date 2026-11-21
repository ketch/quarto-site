---
title: nodepy 0.3 available via easy_install
date: '2011-01-13'
categories:
- nodepy
- easy_install
- python
- software-distribution
---
To facilitate my research and perhaps help someone else out there, I develop a python package based around numerical ODE solvers (Runge-Kutta methods, multistep methods, etc.) as objects. The package is called [nodepy](http://web.kaust.edu.sa/faculty/davidketcheson/NodePy/), and has somewhat limited functionality. However, it contains a very nice implementation of rooted trees, including the ability to compute all the things necessary for deriving order conditions of general linear methods. It also has a lot of nice functionality for Runge-Kutta methods, including a lot of things related to low-storage methods and embedded methods.\
\
As of today, the package is finally [available on the PyPI server](http://pypi.python.org/pypi/nodepy/0.3), and therefore can be installed using\
\
`easy_install nodepy`\
\
Hopefully this will encourage interested parties to try it out (or better yet, to contribute!)
