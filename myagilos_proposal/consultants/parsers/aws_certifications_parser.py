from bs4 import BeautifulSoup
import json
from datetime import date
"""
Where to find certifications: https://aws.amazon.com/certification/?nc1=h_ls
"""
JSON_PATH = "../static/certifications"
COMPANY_PATH = "https://aws.amazon.com"
COMPANY = "aws"

with open(f"{COMPANY}_certifications.html", "r") as rf, open(f"{JSON_PATH}/{date.today().year}_{COMPANY}Certifications.json", "w") as wf:
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
