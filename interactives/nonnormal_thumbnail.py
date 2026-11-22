# Regenerate with: python3 interactives/nonnormal_thumbnail.py interactives/nonnormal.png
# Thumbnail for the Interactives listing: the solution of u' = Au with nearly
# parallel eigenvectors (15 degrees apart) and eigenvalues -1, -10, as on the
# page, shortly after t = 0, with its two eigenvector components.
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

a = np.radians(15) / 2
r1 = np.array([np.cos(a), np.sin(a)])
r2 = np.array([np.cos(a), -np.sin(a)])
u0 = np.array([np.cos(np.radians(60)), np.sin(np.radians(60))])
z = np.linalg.solve(np.column_stack([r1, r2]), u0)
t = np.linspace(0, 3, 1501)
U = np.outer(z[0] * np.exp(-t), r1) + np.outer(z[1] * np.exp(-10 * t), r2)
k = np.searchsorted(t, 0.06)
p1 = z[0] * np.exp(-t[k]) * r1

fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
fig.patch.set_facecolor("white")
s = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(s), np.sin(s), color="0.6", lw=1)
for r, c in ((r1, "#1f77b4"), (r2, "#2ca02c")):
    ax.plot([-4 * r[0], 4 * r[0]], [-4 * r[1], 4 * r[1]], "--", color=c, alpha=0.5, lw=1)
ax.plot(U[:, 0], U[:, 1], color="0.3", lw=1.5)
ax.annotate("", xy=p1, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#1f77b4", lw=2.5))
ax.annotate("", xy=U[k], xytext=p1, arrowprops=dict(arrowstyle="-|>", color="#2ca02c", lw=2.5))
ax.plot(*u0, "o", mfc="white", mec="black")
ax.plot(*U[k], "ko")
ax.set_xlim(-1.4, 3.8); ax.set_ylim(-1.2, 1.4); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color("0.7")
fig.tight_layout()
fig.savefig(sys.argv[1])
