"""extract_data.py

Extract data from xlsx sheet
"""

from csv import writer

from openpyxl import load_workbook

import pandas as pd

workbook = load_workbook("data/WMCVotes.xlsx")

votes = []

wmc_memberships = pd.read_csv(
    "data/wmc_list.csv",
    header=0,
    index_col=0,
    dtype={
        "Membership": bool
    }
)

members_wmc = set(wmc_memberships.index)

for worksheet in workbook.worksheets:
    if worksheet.title != "Members":
        for cell in worksheet["A"]:
            if cell.value and cell.value != "Supporters":
                votes.append((worksheet.title, cell.value, "aye", ))
        for cell in worksheet["D"]:
            if cell.value and cell.value != "Opposers":
                votes.append((worksheet.title, cell.value, "nye", ))

with open("data/votes.csv", "w", encoding="utf-8") as data:
    csvwriter = writer(data)

    for vote in votes:
        csvwriter.writerow([*vote, vote[1] in members_wmc])
