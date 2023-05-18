from datetime import date
import json
from os import path
"""
Where to find certifications: https://learn.snowflake.com/en/certifications/
"""
COMPANY = "timextender"
COMPANY_PATH = "https://www.timextender.com/certification/"

# HTML_PATH = path.join(path.dirname(__file__), "html/")
JSON_PATH = path.join(path.dirname(__file__), "../static/certifications")
# HTML_FILE = f"{HTML_PATH}/{COMPANY}_certifications.html"
JSON_FILE = f"{JSON_PATH}/{date.today().year}_{COMPANY}Certifications.json"

with open(JSON_FILE, "w") as wf:
    data = {
        "company": COMPANY.upper(),
        "certifications": [
            {
                "name": "Solutions Architect",
                "link": COMPANY_PATH,
                "code": "TSA"
            }
        ]
    }
    json.dump(data, wf, indent=2)
