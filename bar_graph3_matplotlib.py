import numpy as np
from math import comb
import matplotlib.pyplot as plt

width = 1
x_scale = 2
n = 8

# grey background: all 2^n strings by total Hamming weight w = 0..n
w = np.arange(n + 1)
all_counts = np.array([comb(n, x) for x in w])            # C(8,w), sum = 256

# subset with Bob's index = 1: among strings of total weight w, the number
# with that fixed bit = 1 is C(n-1, w-1) (the other w-1 ones among 7 bits).
bob1_counts = np.array([comb(n - 1, x - 1) if 1 <= x <= n else 0 for x in w])

tie = n // 2   # = 4, Alice's tie -> randomize
BLUE = "#1f6fe0"; RED = "#e02020"; GREY = "#e0dfdf"

fig, ax = plt.subplots(figsize=(min(0.22*(n+1)+1, 13), 3.2))

# grey full histogram behind
for xi, c in zip(w, all_counts):
    ax.bar(xi*x_scale, c, width=width, color=GREY, edgecolor="none", zorder=1)

# overlay Bob=1 subset, coloured by whether Alice's action is correct
for xi, c in zip(w, bob1_counts):
    if c == 0:
        continue
    if xi > tie:          # majority 1s -> Alice sends 1 -> correct shoot (blue)
        ax.bar(xi*x_scale, c, width=width, color=BLUE, edgecolor="none", zorder=2)
    elif xi < tie:        # majority 0s -> Alice sends 0 -> missed shoot (red)
        ax.bar(xi*x_scale, c, width=width, color=RED, edgecolor="none", zorder=2)
    else:                 # tie -> half correct / half missed
        ax.bar(xi*x_scale, c/2,             width=width, color=RED,  edgecolor="none", zorder=2)
        ax.bar(xi*x_scale, c/2, bottom=c/2, width=width, color=BLUE, edgecolor="none", zorder=2)

ax.set_xlim(min(w)-width, max(w)*x_scale + width)
ax.set_ylim(0, all_counts.max()*1.02)
ax.axis("off")
fig.savefig("bars_n8_test3.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02, transparent=True)
plt.close(fig)