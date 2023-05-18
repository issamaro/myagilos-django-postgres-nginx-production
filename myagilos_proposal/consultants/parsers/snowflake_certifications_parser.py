from bs4 import BeautifulSoup
from datetime import date
import json
from os import path

"""
Where to find certifications: https://learn.snowflake.com/en/certifications/
"""
COMPANY = "snowflake"
COMPANY_PATH = "https://learn.snowflake.com"

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
                "name": ' '.join(
                    (
                        ''.join(letter for letter in anchor.find("h4", class_="fVlLcO").text.strip()
                                if ord(letter) < 128)
                    ).strip().split()
                ),
                "link": f"{COMPANY_PATH}{anchor.get('href')}",
                "code": anchor.find("div", class_="blIVTa").text.strip()
            }
            for anchor in soup.find("div", class_="bKJiBp").find_all("a", recursive=False)
            if "jpn" not in anchor.get("href")
        ]
    }
    json.dump(data, wf, indent=2)
