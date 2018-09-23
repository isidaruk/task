"""
Crawler

Script is used for downloading job page from URL https://www.snap.com/en-US/jobs/ and save the
extracted page info into an HTML file on the disk:

Input
$ python crawler.py https://www.snap.com/en-US/jobs/ snap.html

Output
snap.html
"""
import sys

import requests

# import urllib.request, urllib.parse, urllib.error

from bs4 import BeautifulSoup

from selenium import webdriver

try:
	from_url = sys.argv[1]         # 'https://www.snap.com/en-US/jobs/'
	to_html_filename = sys.argv[2] # 'snap.html'
except:
	print('Wrong input format, follow such pattern: crawler.py "https://www.example.com/" example.html')
	exit()

driver = webdriver.Firefox('C:\\Users\\Dom\\task\\geckodriver-v0.22.0-win64\\')
# driver = webdriver.Chrome('C:\\Users\\Dom\\task\\chromedriver_win32\\chromedriver.exe') # uncomment this line if Firefox isn't installed

try:
	driver.get(from_url)

	req = requests.get(from_url)

	if req.status_code == 200: # 200 means a successful request
		# HTML from '<html>':
		contents_html = driver.execute_script('return document.documentElement.outerHTML')
		soup_contents_html = BeautifulSoup(contents_html, 'html.parser') # lxml parser didn't work properly
		# soup_contents_html = BeautifulSoup(contents_html, 'lxml') # need lxml to be installed
		# print(soup_contents_html.prettify())
		soup_contents_html_str = str(soup_contents_html)
		# soup_contents_html_str = str(soup_contents_html.prettify())
		
except:
	print('Error while talking to URL: ' + from_url)


# open the file we want to write to and write the contents: 
to_html_file = open(to_html_filename, 'w+', encoding='utf8') # plus sign means it will create a file if it does not exist
to_html_file.write('Copy from URL: ' + from_url + '\n') # add a copyright line
to_html_file.write(soup_contents_html_str)
to_html_file.close()

driver.close()
# driver.quit() # quit the browser

