from bs4 import BeautifulSoup
import json
from datetime import date

"""
Where to find certifications: https://www.qlik.com/us/services/training/certifications-and-qualifications
"""

COMPANY = "qlik"

with open(f"{COMPANY}_certifications.html", "r") as rf, open(f"{date.today().year}_{COMPANY}Certifications.json", "w") as wf:
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
