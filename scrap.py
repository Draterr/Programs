import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json


url = "https://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration.html"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html5lib')
tr = soup.table('tr')[0]
print(tr)