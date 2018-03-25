"""count_edit.py
"""

import time
from io import StringIO

import requests

import pandas as pd

URL = "https://xtools.wmflabs.org/ec-yearcounts/zh.wikipedia.org/{}?format=csv"

users = pd.read_csv(
    "wmc_memberships.csv",
    header=0,
    index_col=0,
    dtype={
        "Membership": bool
    }
)

counts = pd.DataFrame()

for username in users.index:
    print(username)
    response = requests.get(URL.format(username))
    count = pd.read_csv(
        StringIO(response.text),
        header=0,
        index_col=0
    )
    year_total = count.sum(axis=0)
    year_total.name = username
    counts = counts.append(year_total)

counts = counts.reindex(sorted(counts.columns), axis=1)

counts.to_csv("edit_counts.csv", line_terminator="\r\n")