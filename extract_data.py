"""extract_data.py

Extract data from xlsx sheet
"""

from csv import writer

from openpyxl import load_workbook, Workbook

workbook = load_workbook("WMCVotes.xlsx")

votes = []

for worksheet in workbook.worksheets:
    if worksheet.title != "Members":
        for cell in worksheet["A"]:
            if cell.value and cell.value != "Supporters":
                votes.append((worksheet.title, cell.value, "aye", ))
        for cell in worksheet["D"]:
            if cell.value and cell.value != "Opposers":
                votes.append((worksheet.title, cell.value, "nye", ))
    else:
        members_wmc = set([cell.value for cell in worksheet["A"] if cell.value])

with open("votes.csv", "w", encoding="utf-8") as data:
    csvwriter = writer(data)

    for vote in votes:
        csvwriter.writerow([*vote, vote[1] in members_wmc])
