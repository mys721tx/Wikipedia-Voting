"""
pca.py

Principle component analysis
"""

import csv

import numpy as np

import pandas as pd

from sklearn.decomposition import PCA


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

pca = PCA(n_components=2)

pca.fit(dataframe)

reduced = pd.DataFrame(
    pca.transform(dataframe),
    index=dataframe.index,
    columns=("PC1", "PC2")
)

reduced.to_csv("data/pca_result.csv", line_terminator="\r\n")

wmc.to_csv("data/wmc_memberships.csv", line_terminator="\r\n")
