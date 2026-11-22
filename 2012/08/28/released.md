---
title: NodePy version 0.4 released
date: '2012-08-28'
categories:
- nodepy
- numerical-analysis
- python
- Runge-Kutta-methods
- software-distribution
---
NodePy is a Python package for analyzing numerical integrators for initial value ODEs.  It\'s essentially a collection of all the kinds of analysis I\'ve used in my time integrator research, collected in a single object-oriented package.  

If you have a new Runge-Kutta method and want to know all about it, NodePy can tell you most anything.  If you want to design new time integration methods, NodePy can help you.

Although I\'m rather proud of it, it fills a very small niche in the world and I\'m not aware of anyone using it outside of my group and close collaborators.  If you\'ve used it, please let me know in the comments.

One of the thorniest issues in NodePy previously was that floating-point representations of method coefficients were sometimes insufficient, especially when studying very high order methods.  I\'ve now updated NodePy to use Sympy Rationals (and radicals, etc.) wherever possible, allowing exact analysis of many properties.

That and [much more](https://numerics.kaust.edu.sa/nodepy/changes.html#changes) awaits in [NodePy version 0.4](https://numerics.kaust.edu.sa/nodepy/), now available via pip.
