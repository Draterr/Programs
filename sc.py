import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import html2text

url = "https://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration.html"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html5lib')

rows = str(soup.findAll('tbody')[1])

anything = open("out.txt", "r")
anything.readline()
old_data = anything.readline()
anything.close()
ppp = old_data.split()[0]
writing_to_text = open("out.txt", "a")
to_txt = html2text.html2text(rows)
#writing_to_text.write(to_txt)

#new_data = to_txt.split("\n")[1].split()
#new_time = to_txt.split("\n")[1].split()[1]
new_date = to_txt.split("\n")[1].split()[0]
new_date_month = to_txt.split("\n")[1].split()[0].split("-")[1]
new_date_day = to_txt.split("\n")[1].split()[0].split("-")[2]

#print(old_data.split("-")[1])
def compare(a,b):
    if a.split("-")[1] <= b.split("-")[1]:
        pass
    else:
        if a.split("-")[2] > b.split("-")[2]:
            return True

for i in range(1,len(to_txt.split("\n"))-2):
    if compare(to_txt.split("\n")[i].split()[0], ppp):
        writing_to_text.write((to_txt.split("\n")[i].split()))

