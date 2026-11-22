# Regenerate with: python3 interactives/limiters_thumbnail.py interactives/limiters.png
# Thumbnail for the Interactives listing: piecewise-linear interpolants of the
# discontinuous data from the limiters page, with centered-difference slopes
# (which overshoot) and minmod slopes (which do not).
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-4, 5).astype(float)
y = np.sin(x / 2.) + 1. + 2. * (x > 0)


def pieces(y, sigma):
    edges = np.concatenate(([x[0]], (x[1:] + x[:-1]) / 2., [x[-1]]))
    px, py = [], []
    for i in range(len(x)):
        for e in (edges[i], edges[i + 1]):
            px.append(e)
            py.append(y[i] + sigma[i] * (e - x[i]))
    return px, py


centered = np.zeros_like(y)
centered[1:-1] = (y[2:] - y[:-2]) / 2.
F = np.zeros_like(y); B = np.zeros_like(y)
F[:-1] = np.diff(y); B[1:] = np.diff(y)
minmod = np.where(F * B > 0, np.sign(F) * np.minimum(abs(F), abs(B)), 0.)
minmod[0] = minmod[-1] = 0.

fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
fig.patch.set_facecolor("white")
ax.plot(*pieces(y, centered), color="#d62728", lw=1.5, alpha=0.8)
ax.plot(*pieces(y, minmod), color="black", lw=2)
ax.plot(x, y, "o", color="red", ms=6, alpha=0.5)
ax.set_xlim(-4, 4); ax.set_ylim(-0.4, 4.6)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color("0.7")
fig.tight_layout()
fig.savefig(sys.argv[1])
