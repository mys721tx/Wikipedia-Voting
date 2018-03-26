"""count_edit.py
"""

import time
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

counts = pd.DataFrame()
counts_main = pd.DataFrame()

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
    edit_main = count.loc["Main"]
    edit_main.name = username
    counts_main = counts_main.append(edit_main)

counts = counts.reindex(sorted(counts.columns), axis=1)
counts_main = counts_main.reindex(sorted(counts_main.columns), axis=1)

counts.to_csv("data/edit_counts.csv", line_terminator="\r\n")
counts_main.to_csv("data/edit_counts_main.csv", line_terminator="\r\n")
