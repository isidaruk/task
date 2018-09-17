"""
Extractor

Script is used for read locally stored HTML file and analyze open jobs on the page, save the extracted job info into a CSV
file, formatted as follows:

jobs.csv format:
---
Job Title, Category, Status, Location
Accounts Payable Specialist, Finance Accounting, Regular, Los Angeles
Senior Accountant, Finance Accounting, Regular, London
...
...
----

Input
$ python extractor.py snap.html snap.csv

Output
snap.csv
"""