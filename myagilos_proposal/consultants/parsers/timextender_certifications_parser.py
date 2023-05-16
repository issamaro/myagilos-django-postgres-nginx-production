import json
from datetime import date

"""
Where to find certifications: https://learn.snowflake.com/en/certifications/
"""
COMPANY = "timextender"
COMPANY_PATH = "https://www.timextender.com/certification/"

with open(f"{date.today().year}_{COMPANY}Certifications.json", "w") as wf:
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
