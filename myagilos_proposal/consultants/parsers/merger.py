import json
import os
from datetime import date

CURRENT_YEAR = date.today().year

JSON_PATH = os.path.join(os.path.dirname(__file__), "../static/certifications")
JSON_FILE = f"{JSON_PATH}/{date.today().year}_allCertifications_.json"
# for x in os.listdir(JSON_PATH):
#     print(x)

json_current_year_files = [json.load(open(os.path.join(JSON_PATH, file))) for file in os.listdir(JSON_PATH)
                           if file.startswith(str(CURRENT_YEAR)) and file.endswith("Certifications.json")]

# print(json_current_year_files)

[open(os.path.join(JSON_PATH, file)).close() for file in os.listdir(JSON_PATH)
 if file.startswith(str(CURRENT_YEAR)) and file.endswith("Certifications.json")]

# for file in json_current_year_files:
#     for _ in range(5):
#         print()
#     print(file)

merged_dict = [{
    "company": json_file["company"],
    "certifications": json_file["certifications"]
} for json_file in json_current_year_files]

with open(JSON_FILE, "w") as wf:
    json.dump(merged_dict, wf, indent=2)