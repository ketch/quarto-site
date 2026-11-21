---
title: Managing publication lists in HTML
date: '2011-10-28'
categories:
- academia
- bibliographic-reference-management
- CSS
- HTML
- mendeley
- publications
- scientific-publishing
---
As an academic, it\'s a good idea to maintain a [professional website](http://web.kaust.edu.sa/faculty/davidketcheson/) with a [list of your publications](http://web.kaust.edu.sa/faculty/davidketcheson/publications.html).  Ideally, this list should include links to where visitors can download the papers (PDFs) [and any related code](http://sciencecodemanifesto.org).  In my case, I also maintain a [website for my research group](http://numerics.kaust.edu.sa) that has another [publication list.](http://numerics.kaust.edu.sa/publications.html) Of course, you need to maintain local reference files with the citation info for your publications (for inclusion in later publications), as well as your CV.

Maintaining all these separate lists can become very tedious, which is probably why most academics\' sites are usually out-of-date.  Here\'s how I automate much of it:

- **I use [Bibtex](http://www.bibtex.org/).** This allows automatic generation of bibliographies for papers and for my CV.  And it\'s the basis for generating HTML bibliographies, as outlined below.
- **I use [Mendeley](http://www.mendeley.com).** Mendeley allows me to create separate bibliographic lists (e.g., for my own publications and for those of my research group) and [export them as bibtex files](http://www.mendeley.com/blog/tipstricks/howto-use-mendeley-to-create-citations-using-latex-and-bibtex/), using the desktop app.  It\'s also possible to [get a bibtex file of your Mendeley publications directly on-line](http://bibbase.org/cgi-bin/mendeley/Mendeley-oapi/requestToken.py) through [BibBase](http://www.bibbase.org).  You can even [display a list of your publications on-line automatically using Mendeley,](http://www.mendeley.com/blog/academic-features/if-you-publish-a-paper-but-nobody-reads-it-does-it-make-a-difference/#more-26402) but it\'s not very customizable; for instance, they appear in alphabetical, rather than chronological order.
- **I would use [BibBase](http://www.bibbase.org/)** to [automatically display an updated bibliography](http://www.bibbase.org/help/) if my institutional server ran PHP or CGI scripts, but no luck there.
- My less-automatic solution is **[simple Python scripts](https://github.com/ketch/tex2_rst_html)** that generate CSS-friendly HTML.  The scripts use the Python module bibliograph to parse bibtex entries.  I could instead use [bibtex2html](https://encrypted.google.com/url?sa=t&rct=j&q=bibtex2html&source=web&cd=1&sqi=2&ved=0CBgQFjAA&url=http%3A%2F%2Fwww.lri.fr%2F~filliatr%2Fbibtex2html%2F&ei=EqqqTubIK4zC8QPF7sySCw&usg=AFQjCNFE8lFV7TxfgvapcrTjFvSDcEqyng).  I like my solution better because the customization is all done using CSS rather than Python, so I can change the look without re-generating the HTML.  Of course, bibtex2html is a more polished and flexible tool than my 30-line script.
- Here\'s a CSS snippet that\'s used for [this publication list](http://numerics.kaust.edu.sa/publications.html):

``` brush:css;
#pub {padding: 5px; border-width: 2px; border-style: none; background-color: #eee4b5; font-size: 1.2em; margin-top: 20px; margin-bottom: 20px;}
#pub a{font-weight: bold; color: #09434e;}
#pub name{font-weight: bold; color: #09434e;}
#pub journal{font-style: italic;}
```

 

The workflow for adding a new paper to an html bibliography is:

1.  Add the paper in Mendeley.
2.  Export bibtex from Mendeley.
3.  Run Python scripts.
4.  Paste resulting HTML into the appropriate file.

Again, it would be simpler if I could use Bibbase (cutting out steps 2-4).  It\'s still fairly painless, and it\'s easy to generate new bibilographic lists or customize the look of existing ones.
