"""
plot_pca.py
"""

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import mpld3
from mpld3 import plugins

def rand_jitter(arr):
    stdev = .01*(max(arr)-min(arr))
    return arr + np.random.randn(len(arr)) * stdev

def jitter(x, y, s=20, c='b', marker='o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, hold=None, **kwargs):
    return plt.scatter(rand_jitter(x), rand_jitter(y), s=s, c=c, marker=marker, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax, alpha=alpha, linewidths=linewidths, verts=verts, hold=hold, **kwargs)

reduced = pd.read_csv(
    "data/pca_result.csv",
    header=0,
    index_col=0,
    dtype={
        "PC1": np.float64,
        "PC2": np.float64
    }
)

wmc = pd.read_csv(
    "data/wmc_memberships.csv",
    header=0,
    index_col=0,
    dtype={
        "Membership": bool
    }
)

rest = np.invert(wmc)

def label_point(x, y, val, ax):
    a = pd.DataFrame({'x': x, 'y': y, 'val': val})
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

plt.figure(figsize=(9, 6))

#print(reduced[rest])

plot_rest = plt.scatter(
    reduced[rest["Membership"]]["PC1"],
    reduced[rest["Membership"]]["PC2"],
    c="b",
    alpha=0.4,
    label="Non-WMC"
)

plot_wmc = plt.scatter(
    reduced[wmc["Membership"]]["PC1"],
    reduced[wmc["Membership"]]["PC2"],
    c="g",
    alpha=0.4,
    label="WMC"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.legend(
    handles=[plot_rest, plot_wmc]
)

plt.savefig("plots/pca-2017.png", dpi=300, transparent=True)

#label_point(reduced[:, 0],reduced[:, 1], reduced.columns.tolist(), plt.gca())

plt.figure()

plot_rest = jitter(
    reduced[rest["Membership"]]["PC1"],
    reduced[rest["Membership"]]["PC2"],
    c="b",
    alpha=0.4,
    label="Non-WMC"
)

plot_wmc = jitter(
    reduced[wmc["Membership"]]["PC1"],
    reduced[wmc["Membership"]]["PC2"],
    c="g",
    alpha=0.4,
    label="WMC"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

tooltip_rest = plugins.PointHTMLTooltip(plot_rest, reduced[rest["Membership"]].index.tolist())
tooltip_wmc = plugins.PointHTMLTooltip(plot_wmc, reduced[wmc["Membership"]].index.tolist())

zoom = plugins.Zoom(button=False, enabled=True)
box_zoom = plugins.BoxZoom(button=False, enabled=True)


plugins.connect(plt.gcf(), tooltip_rest)
plugins.connect(plt.gcf(), tooltip_wmc)

mpld3.save_html(plt.gcf(), "docs/pca-2017.html")
