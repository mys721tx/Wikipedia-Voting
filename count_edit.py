"""count_edit.py
"""

from io import StringIO

import requests

import pandas as pd

URL = "https://xtools.wmflabs.org/ec-yearcounts/zh.wikipedia.org/{}?format=csv"

users = pd.read_csv(
    "data/wmc_memberships.csv",
    header=0,
    index_col=0,
    dtype={
        "Membership": bool
    }
)

frames = []

for username in users.index:
    print(username)
    response = requests.get(URL.format(username))
    try:
        count = pd.read_csv(
            StringIO(response.text),
            header=0,
            index_col=0
        )
        frames.append(count)

    except pd.errors.ParserError:
        print("unable to find {}".format(username))

counts = pd.concat(frames, keys=users.index, sort=True)

counts = counts.reindex(sorted(counts.columns), axis=1)

counts = counts.loc[:, ~counts.columns.str.contains('^Unnamed')]

counts.to_csv("data/edit_counts.csv", line_terminator="\r\n")
