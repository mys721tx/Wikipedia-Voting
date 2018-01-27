"""
foo
"""

import csv

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import mpld3
from mpld3 import plugins

from sklearn.decomposition import PCA


mapping_vote = {"aye": 1, "nye": -1}

votes = {}
labels = {}

def rand_jitter(arr):
    stdev = .01*(max(arr)-min(arr))
    return arr + np.random.randn(len(arr)) * stdev

def jitter(x, y, s=20, c='b', marker='o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, hold=None, **kwargs):
    return plt.scatter(rand_jitter(x), rand_jitter(y), s=s, c=c, marker=marker, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax, alpha=alpha, linewidths=linewidths, verts=verts, hold=hold, **kwargs)

with open("votes-2017.csv", "r", encoding="utf-8") as data:
    reader = csv.reader(data)
    for row in reader:
        event, username, vote, label_raw = row
        if username in votes:
            votes[username][event] = mapping_vote[vote]
        else:
            votes[username] = {event: mapping_vote[vote]}

        if label_raw == "True":
            label = True
        else:
            label = False

        if username in labels:
            if label != labels[username]:
                raise ValueError
        else:
            labels[username] = label

dataframe = pd.DataFrame.from_dict(votes)

dataframe = dataframe.fillna(0)

pca = PCA(n_components=2)

pca.fit(dataframe.T)

reduced = pca.transform(dataframe.T)

wmc = dataframe.columns.map(lambda x: labels[x]).values.astype(bool)

rest = np.invert(wmc)

def label_point(x, y, val, ax):
    a = pd.DataFrame({'x': x, 'y': y, 'val': val})
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

plt.figure(figsize=(9, 6))

plot_rest = jitter(
    reduced[rest][:, 0],
    reduced[rest][:, 1],
    c="b",
    alpha=0.4,
    label="Non-WMC"
)

plot_wmc = jitter(
    reduced[wmc][:, 0],
    reduced[wmc][:, 1],
    c="g",
    alpha=0.4,
    label="WMC"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

#plt.legend(
#    handles=[plot_rest, plot_wmc]
#)

#label_point(reduced[:, 0],reduced[:, 1], dataframe.columns.tolist(), plt.gca())

tooltip_rest = plugins.PointHTMLTooltip(plot_rest, dataframe.columns[rest].tolist())
tooltip_wmc = plugins.PointHTMLTooltip(plot_wmc, dataframe.columns[wmc].tolist())

zoom = plugins.Zoom(button=False, enabled=True)
box_zoom = plugins.BoxZoom(button=False, enabled=True)


plugins.connect(plt.gcf(), tooltip_rest)
plugins.connect(plt.gcf(), tooltip_wmc)

mpld3.save_html(plt.gcf(), "pca-2017.html")

#plt.savefig("pca-2017.png", dpi=300, transparent=True)

#dataframe.to_csv("test.csv")
