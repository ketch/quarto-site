---
title: '7 Habits of the Open Scientist: #2 -- Reproducible Research'
date: '2012-08-03'
categories:
- open-science
- reproducible-research
- research
- science
- scientific-computing
- software-distribution
---
Note: this post is part of [a series on habits of the open scientist](http://scienceinthesands.blogspot.co.uk/2012/07/7-habits-of-open-scientist.html).  Here I discuss the second habit, **reproducible research**.  The previous post was on [**open scientific publishing**](http://scienceinthesands.blogspot.co.uk/2012/08/7-habits-of-open-scientist-1-open.html).

**Reproducible research**

Reproducibility is part of the definition of science: if the results of your experiment cannot be replicated by different people in a different location, then you\'re not doing science.  Far from being a mere philosophic concern, reproducible research has been a key issue in prominent controversies like [climategate](http://en.wikipedia.org/wiki/Climatic_Research_Unit_email_controversy) and [cancer research clinical trials](http://magazine.amstat.org/blog/2011/01/01/scipolicyjan11/).

Especially disconcerting is the typical irreproducibility of scientific work involving computer code:

> "Computational science is facing a credibility crisis: it's impossible to verify most of the computational results presented at conferences and in papers today." (LeVeque, Mitchell, Stodden, *CiSE* 2012)

Frankly, I used to find that I was often unable to reproduce *my own* computational results after a few months, because I had not maintained sufficiently detailed notes about my code and my computing environment.

**The open scientist ensures that the entire *research compendium* \-- including not only the paper but the data, source code, parameters, post-processing, and computing environment \-- is made freely available, preferably in a way that facilitates its reuse by others.**

I won\'t spend more time motivating reproducible research, since [others have done that](http://www.bloomberg.com/news/2012-01-10/scientists-share-secrets-or-lose-funding-stodden-and-arbesman.html) [much better than I could](http://biostatistics.oxfordjournals.org/content/11/3/385.full).  Instead, let me focus on the relatively easy first steps you can take to make your research more reproducible.

**The bare minimum: publish your code and data**

If you wish to set an example of good reproducible computational research practices, I have good news for you: the bar is very low at the moment.  The reason why \"it\'s impossible to verify most of the computational results\" is that *most researchers don\'t release their code and data.*  The first step toward working reproducibly is simply to put the code and data that is used in your published research out in the open.

If you don\'t want to release your code to the public, please read about [why you should](http://jarrodmillman.com/talks/siam2011/ms148/leveque.pdf) and [why you can](http://www.nature.com/news/2010/101013/full/467753a.html).  Once you\'re convinced, go endorse the [Science Code Manifesto](http://sciencecodemanifesto.org/).

Releasing your code and data can be as simple as posting a tarball on your website with a reference to the paper it pertains to.  Or you may wish to start putting all your code out in the open on [Bitbucket](http://bitbucket.org) or [Github](http://github.com), [like I do](http://github.com/ketch/).  I don\'t claim that these are the *best* solutions possible, but they are a big step forward from keeping everything on your own hard drive.

When you release your code and data, it is important to use an appropriate license.  [Victoria Stodden](http://stodden.net), a leader in the reproducible research movement, recommends the use of a permissive license like [modified BSD](http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22_or_.22Modified_BSD_License.22.29) for code and [Science Commons Database Protocol](http://sciencecommons.org/resources/faq/database-protocol/) for data.  Together with the [Creative Commons BY](http://creativecommons.org/licenses/by/2.0/) license for media (that I mentioned in [my last post](http://scienceinthesands.blogspot.co.uk/2012/08/7-habits-of-open-scientist-1-open.html)), these comprise the [*Reproducible Research Standard*](http://www.ijclp.net/files/ijclp_web-doc_1-13-2009.pdf), a convenient amalgamation of licenses for open science.

Be sure to include a mention of reproducibility in your paper, along with links to the code and data.  If you release your work under the RRS, I suggest using [this citation](http://dx.doi.org/10.1109/MCSE.2009.19).

**Real benefits**

The open scientist may adopt reproducible research practices for philosophical reasons, but he soon finds that they bring more direct benefits.  Because he writes code and prepares data with the expectation that it will be seen by others, the open scientist finds it much easier for himself, students, and colleagues to build on past work.  New collaborations are formed when others discover his work through openly released code and data.  And (as in the case of [this paper](http://numerics.kaust.edu.sa/papers/pyclaw-sisc/pyclaw-sisc.html), for example) the code itself may be the main subject of publications in [journals that have come to recognize the importance](http://scicomp.stackexchange.com/questions/660/venues-for-publishing-papers-that-emphasize-software) of scientific software.

**Taking it further**

Like free and open scientific publishing, reproducible research has become a very large movement, and only a book could hope to cover it all.  Here I\'ve merely distilled some basic practical suggestions.

Openly releasing code and data is only the first step.  Open scientists may wish to adopt tools that track code provenance and ensure a fully reproducible workflow, such as

- [Madagascar](http://www.reproducibility.org/wiki/Main_Page)
- [VisTrails](http://www.vistrails.org)
- [knitr](http://yihui.name/knitr/)
- [Sumatra](http://neuralensemble.org/trac/sumatra)
- [VCR](http://vcr.stanford.edu/)

Next up: Habit #3 \-- [**Pre-publication dissemination of research**](http://scienceinthesands.blogspot.co.uk/2012/08/7-habits-of-open-scientist-3-pre.html).
