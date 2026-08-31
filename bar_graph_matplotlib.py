import numpy as np
from scipy.special import comb
import matplotlib.pyplot as plt
width = 1
x_scale = 2
def draw(n, fname, bell=False):
    m = n - 1                       # other bits (Bob's bit fixed = 1)
    k = np.arange(m + 1)         # Hamming weight of the other m bits
    h = comb(m, k)                  # counts C(m,k), sum = 2**m
    tie = (m+1) // 2              # weight where adding Bob's 1 makes an exact tie

    BLUE = "#1f6fe0"
    GREY = "#b8b8b8"
    RED = "#e02020"

    fig, ax = plt.subplots(figsize=(min(0.22*(m+1)+1, 13), 3.2))
    for ki, hi in zip(k, h):
        if ki < tie:                # strict majority of 1s -> win  (blue)
            ax.bar(ki*x_scale, hi, width=width, color=BLUE, edgecolor="none")
        elif ki > tie:              # majority of 0s -> loss  (grey)
            ax.bar(ki*x_scale, hi, width=width, color=RED, edgecolor="none")
        else:                       # exact tie -> Alice random -> half win
            ax.bar(ki*x_scale, hi/2,               width=width, color=RED, edgecolor="none")
            ax.bar(ki*x_scale, hi/2, bottom=hi/2,  width=width, color=BLUE, edgecolor="none")

    if bell:                        # peak-matched Gaussian, dotted
        mu = m / 2.0
        sigma = np.sqrt(m) / 2.0
        xx = np.linspace(0, m, 400)
        yy = h.max() * np.exp(-(xx - mu)**2 / (2 * sigma**2))
        ax.plot(xx * x_scale, yy, linestyle=(0, (2, 2)), linewidth=2.2,
                color="#333333", zorder=5)

    ax.set_xlim(min(k)-width, max(k)*x_scale + width)
    ax.set_ylim(0, h.max()*1.02)
    ax.axis("off")
    fig.savefig(fname, dpi=200, bbox_inches="tight",
                pad_inches=0.02, transparent=True)
    plt.close(fig)

draw(8,  "bars_n8.png")
draw(64, "bars_n64.png", bell=True)