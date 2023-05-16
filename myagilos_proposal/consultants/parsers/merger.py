import json
import os
from datetime import date

CURRENT_YEAR = date.today().year
JSON_PATH = "../static/certifications"
json_current_year_files = [json.load(open(file)) for file in os.listdir(f"{JSON_PATH}/")
                           if file.startswith(str(CURRENT_YEAR)) and file.endswith(".json")]

[open(file).close() for file in os.listdir(JSON_PATH)
 if file.startswith(str(CURRENT_YEAR)) and file.endswith(".json")]

merged_dict = [{
    "company": json_file["company"],
    "certifications": json_file["certifications"]
} for json_file in json_current_year_files]

with open(f"{JSON_PATH}/Certifications.json", "w") as wf:
    json.dump(merged_dict, wf, indent=2)