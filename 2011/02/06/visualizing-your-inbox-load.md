---
title: Visualizing my inbox load
date: '2011-02-06'
categories:
- e-mail
- KAUST
- python
---
The other day I happened to notice that I had received well over 100 e-mails in one day.  While that may or may not seem high to you, in my case this meant that I spent most of the day handling e-mails, since the majority of these actually required a response or some other action on my part (I\'m organizing two workshops right now, which accounts for much of the traffic).\
\
I thought back to grad school days when I might or might not receive any e-mail on a given day.  When did it all get so crazy?  I decided it would be fun to find out.  A bit of searching turned up the Python package imaplib, which allowed me to download headers for all messages (ever!) from my Gmail account.  Then it was just a matter of extracting and reformatting the dates and plotting up a histogram with matplotlib.  Here\'s the result:\

<a href="http://1.bp.blogspot.com/_BY1MXXROj8g/TU75BC5FS6I/AAAAAAAAAmM/VO4o7wQM648/s1600/David_email_hist2.png" data-imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img src="http://1.bp.blogspot.com/_BY1MXXROj8g/TU75BC5FS6I/AAAAAAAAAmM/VO4o7wQM648/s400/David_email_hist2.png" data-border="0" width="400" height="216" /></a>

\
\
Can you tell when I graduated and started working for KAUST?  In the last few months prior to starting at KAUST, I got an average of about 250 messages a month.  Within 2 months of starting at KAUST, that average was well over 1000, with some months substantially higher.  Ah, the joys of being a professor\...
