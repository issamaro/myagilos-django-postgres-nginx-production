from bs4 import BeautifulSoup
from datetime import date
import json
from os import path
"""
Where to find certifications: https://aws.amazon.com/certification/?nc1=h_ls
"""

COMPANY = "aws"
COMPANY_PATH = "https://aws.amazon.com"

HTML_PATH = path.join(path.dirname(__file__), "html/")
JSON_PATH = path.join(path.dirname(__file__), "../static/certifications")
HTML_FILE = f"{HTML_PATH}/{COMPANY}_certifications.html"
JSON_FILE = f"{JSON_PATH}/{date.today().year}_{COMPANY}Certifications.json"

with open(HTML_FILE, "r") as rf, open(JSON_FILE, "w") as wf:
    html = rf.read()
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find("ul", class_="lb-dropdown-list")
    data = {
        "company": COMPANY.upper(),
        "certifications": [
            {
                "name": (
                    " ".join(li.find("span").text.split())
                ).replace("\u2013", "-"),
                "link": f"{COMPANY_PATH}{li.get('data-value')}",
                "code": (
                    "".join([f"{word[0]}{word[1]}" if len(word) > 1 else f"{word[0]}"
                            for word in li.find("span").text.strip().split()])
                ).replace("\u2013", "-")
            }
            for li in ul.find_all("li")
        ]
    }
    json.dump(data, wf, indent=2)