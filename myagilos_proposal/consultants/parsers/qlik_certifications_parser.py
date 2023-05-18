from bs4 import BeautifulSoup
from datetime import date
import json
from os import path

"""
Where to find certifications: https://www.qlik.com/us/services/training/certifications-and-qualifications
"""

COMPANY = "qlik"

HTML_PATH = path.join(path.dirname(__file__), "html/")
JSON_PATH = path.join(path.dirname(__file__), "../static/certifications")
HTML_FILE = f"{HTML_PATH}/{COMPANY}_certifications.html"
JSON_FILE = f"{JSON_PATH}/{date.today().year}_{COMPANY}Certifications.json"

with open(HTML_FILE, "r") as rf, open(JSON_FILE, "w") as wf:
    html = rf.read()
    soup = BeautifulSoup(html, "html.parser")
    data = {
        "company": COMPANY.upper(),
        "certifications": [
            {
                "name": div.find("h2").text.strip(),
                "link": div.find("a", string="Register Now").get("href") if div.find("a", string="Register Now") else None,
                "code": "".join([word[0].upper() for word in div.find("h2").text.strip().split()])
            }
            for panel in soup.find_all("div", class_="tabs__panel")
            for div in panel.find_all("div", recursive=False)
        ]
    }
    json.dump(data, wf, indent=2)
