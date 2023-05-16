from bs4 import BeautifulSoup
import json
from datetime import date

"""
Where to find certifications: https://learn.snowflake.com/en/certifications/
"""
COMPANY = "snowflake"
COMPANY_PATH = "https://learn.snowflake.com"

with open(f"{COMPANY}_certifications.html", "r") as rf, open(f"{date.today().year}_{COMPANY}Certifications.json", "w") as wf:
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
