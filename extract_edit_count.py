"""extract_edit_count.py
"""

import pandas as pd

table = pd.read_csv(
    "data/edit_counts.csv",
    header=0,
    index_col=[0, 1],
)

table.sum(level=0, axis=0).to_csv("data/edit_counts_total.csv", line_terminator="\r\n")
table.xs("Main", level=1).to_csv("data/edit_counts_main.csv", line_terminator="\r\n")
table.xs("Wikipedia", level=1).to_csv("data/edit_counts_wikipedia.csv", line_terminator="\r\n")
