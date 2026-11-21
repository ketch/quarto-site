---
title: The positivity pipe dream fulfilled?
date: '2011-05-31'
categories:
- numerical-analysis
- positivity
- SSP
- hyperbolic-PDEs
- mathematical-exposition
---
This post is about my [recently accepted SINUM paper](http://arxiv.org/abs/1105.5798). This is an attempt to provide a broad context for the paper and related work in a less formal way, which couldn\'t be included in a journal publication.\
\
In 1979, Bolley and Crouzeix published a fairly astonishing result ([in French here](http://archive.numdam.org/article/M2AN_1978__12_3_237_0.pdf)). Namely, they showed that, for linear differential equations whose solution is always positive, it is **impossible** to design numerical methods that always yield a **positive** solution under **arbitrarily large** step sizes, even if one considers the very broad class of ODE solvers known as general linear methods. The **only** exception to this statement is the backward Euler method, which has many nice properties but is, unfortunately, too inaccurate for most applications.\
\
This result stands in stark contrast to corresponding results on, say, stability in inner-product norms, where use of implicit methods can get you **unconditional** stability even for nonlinear problems.\
\
I\'m speaking roughly here, and won\'t attempt to be more precise (go read the paper if you want details). But the motivation cited by Bolley and Crouzeix for looking at this question was the idea that one might be able **to take large time steps and maintain positivity in the solution of hyperbolic problems**. Unfortunately, their result showed that this was not possible unless one was willing to settle for first-order accuracy.\
\
What this result didn\'t indicate is **how large** the positivity-preserving step size could be for an implicit method. This question was partially answered within a decade, by [Lenferink](http://www.jstor.org/pss/2008536) and by [van de Griend & Kraaijevanger](http://www.springerlink.com/content/t3x7154136486u46/), for linear multistep methods and for Runge-Kutta methods, respectively. In both cases they found that the largest positivity-preserving step size was **no more than two times** the step size allowed by using the forward Euler method.\
\
Of course, an implicit solve costs significantly more than an explicit solve, so gaining only a factor of two in the step size just isn\'t worth it. I don\'t know of any more work that was done on this problem after 1991 until fairly recently, in two of [my own](http://www.amath.washington.edu/~ketch/David_Ketcheson/ketcheson2008c.html) [papers](http://linkinghub.elsevier.com/retrieve/pii/S0168927408000688). The results there are consistent with the apparent barrier of a 2X step size, although see my short note at the end.\
\
In one attempt to circumvent this bound, [Gottlieb, Macdonald & Ruuth](http://people.maths.ox.ac.uk/~macdonald/dsrk.pdf) investigated the class of diagonally split Runge-Kutta methods (which aren\'t general linear methods, so escape the implications of Bolley & Crouzeix). They did find higher order methods with unconditional strong stability properties, but the accuracy of these methods invariably reduced to **first order** when used with large timesteps! It seemed that any effort to find unconditionally positive methods would be thwarted one way or another.\
\
This sets the stage for my recently accepted SINUM paper. In this paper I found that by using both upwind-biased and downwind-biased discretizations (an idea that goes all the way back to [Shu\'s original paper on \"TVD time discretizations\"](http://link.aip.org/link/?SJOCE3/9/1073/1)) in implicit Runge-Kutta methods, one can obtain second-order accurate methods that preserve positivity under arbitrarily large step sizes \-- and they have this property even when applied to nonlinear problems. Remarkably, the methods appear to give quite accurate results when applied to problems with shocks.\
\
It seems that we have gotten around the 2X barrier at last! But important issues remain, most notably the efficient implementation of these \"implicit downwind Runge-Kutta schemes\" in combination with high order hyperbolic PDE discretizations (like WENO).\
\
I must reiterate that I\'ve glossed over several important technical points here. For more details, go read the paper.\
\
Note 1: In my Ph.D. thesis, I did find a method that breaks the 2X barrier, but only just barely and only for linear problems.\
\
Note 2: I\'ve referred rather carelessly in this post to literature on positivity preservation, contractivity, and strong stability preservation (monotonicity) without distinguishing between the three, simply because the conditions on the method turn out to be the same. The articles mentioned generally focus on one property or the other, but the results almost always carry over to all three.
