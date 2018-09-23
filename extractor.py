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
from bs4 import BeautifulSoup

import re

import sys

import csv

try:
	from_html_filename = sys.argv[1] # snap.html
	to_filename_csv = sys.argv[2]    # snap.csv
except:
	print('Wrong input format, follow such pattern: extractor.py example.html example.csv')
	exit()

from_html_filename = 'snap.html'
file = open(from_html_filename, 'r')

soup = BeautifulSoup(file, 'html.parser')

# soup.find_all('tr')

tabular_data = []

for tr in  soup.find_all('tr'):
	# print(tr)

	# print(tr.get_text())
	# print(tr.contents[:])
	
	job_content = []

	for content in tr.contents[ : ]:
		# print(content.get_text(), end=',')
		job_content.append(content.get_text())

	#print()
	tabular_data.append(job_content)
	
# print(tabular_data)

f_tabular_data = []

for data in tabular_data:
	# print(data)
	splitted = re.findall('[A-Z][^A-Z]*\S[^A-Z]*', data[3]) # find all bad-formatted data

	f_tabular_data.append(splitted)

# print(f_tabular_data)

for i in range(len(f_tabular_data)):
	len_sublist = len(f_tabular_data[i])
	if len_sublist > 1:
		for str_idx in range(len_sublist):
			if str_idx == 0: # first string 
				tabular_data[i][3] = f_tabular_data[i][str_idx] + '; ' # semicolon delimiter instead of whitespace ' '
			elif str_idx < len_sublist - 1: # prelast string
				tabular_data[i][3] += f_tabular_data[i][str_idx] + '; ' # semicolon delimiter instead of whitespace ' '
			# elif str_idx == len_sublist - 1:
			#	tabular_data[i][3] += f_tabular_data[i][str_idx]
			else:
				tabular_data[i][3] += f_tabular_data[i][str_idx]

# print(tabular_data)

##filename = 'tabular_data.txt'
##file = open(filename, 'w+', encoding='utf8') # plus sign means it will create a file if it does not exist
##file.write(str(tabular_data))
##file.close()


with open(to_filename_csv, 'w+', newline='', encoding='utf-8') as file_csv: # don't need to explicitly close the file now

	csv_writer = csv.writer(file_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) # , dialect='excel')
	# csv_writer = csv.writer(file_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, dialect='excel')

	csv_writer.writerow(['Job Title', 'Category', 'Status', 'Location']) # header row in csv: Job Title, Category, Status, Location

	for data in tabular_data:
		csv_writer.writerow(data)

