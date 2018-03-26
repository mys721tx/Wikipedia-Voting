"""
simulate_votes.py

Principle component analysis
"""

import csv

import numpy as np
from numpy.random import randint

import pandas as pd

from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

mapping_vote = {"aye": 1, "nye": -1}

votes = {}
labels = {}

with open("data/votes-2017.csv", "r", encoding="utf-8") as data:
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

wmc = pd.DataFrame(
    dataframe.columns.map(lambda x: labels[x]).values.astype(bool),
    index=dataframe.columns,
    columns=("Membership",)
)

dataframe = dataframe.T

dataframe[wmc["Membership"]] = randint(-1, 2, dataframe[wmc["Membership"]].shape)

pca = PCA(n_components=2)

pca.fit(dataframe)

reduced = pd.DataFrame(
    pca.transform(dataframe),
    index=dataframe.index,
    columns=("PC1", "PC2")
)

rest = np.invert(wmc)

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
    label="Simulated"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.legend(
    handles=[plot_rest, plot_wmc]
)

plt.savefig("plots/pca-simulation.png", dpi=300, transparent=True)
