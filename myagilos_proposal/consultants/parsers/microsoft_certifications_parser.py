from bs4 import BeautifulSoup
from datetime import date
import json
import os

COMPANY_PATH = "https://learn.microsoft.com"

COMPANY = "microsoft"
HTML_PATH = os.path.join(os.path.dirname(__file__), "html/")
JSON_PATH = os.path.join(os.path.dirname(__file__), "../static/certifications")
HTML_FILE = f"{HTML_PATH}/{COMPANY}_certifications.html"
JSON_FILE = f"{JSON_PATH}/{date.today().year}_{COMPANY}Certifications.json"

with open(HTML_FILE, "r") as rf, open(JSON_FILE, "w") as wf:
    html = rf.read()
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div", class_="card-template")
    data = {
        "company": COMPANY.upper(),
        "certifications": [
            {
                "name": " ".join(div.find("a", class_="card-title").text.split()),
                "link": f"{COMPANY_PATH}{div.find('a', class_='card-title').get('href')}",
                "code": div.find("span", class_="is-comma-delimited").text.strip()
            }
            for div in divs
        ]
    }
    json.dump(data, wf, indent=2)
