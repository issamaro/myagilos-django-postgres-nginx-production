from bs4 import BeautifulSoup
import json
from datetime import date

MICROSOFT_PATH = "https://learn.microsoft.com"
COMPANY = "microsoft"

with open(f"{COMPANY}_certifications.html", "r") as rf, open(f"{date.today().year}_{COMPANY}Certifications.json", "w") as wf:
    html = rf.read()
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div", class_="card-template")
    data = {
        "company": COMPANY.upper(),
        "certifications": [
            {
                "name": " ".join(div.find("a", class_="card-title").text.split()),
                "link": f"{MICROSOFT_PATH}{div.find('a', class_='card-title').get('href')}",
                "code": div.find("span", class_="is-comma-delimited").text.strip()
            }
            for div in divs
        ]
    }
    json.dump(data, wf, indent=2)
