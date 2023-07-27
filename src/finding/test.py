import requests
from bs4 import BeautifulSoup

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

url = "https://logeion.uchicago.edu/%E1%BC%80%CF%81%CE%B8%CE%AD%CE%BD%CF%84%CA%BC"

res = requests.get(url, headers=headers, timeout=10)

print(res.status_code, res.reason)

with open("", 'w', encoding="utf-8") as f:
    f.write(res.text)
