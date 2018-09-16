import json
import sys
import os.path
from datetime import datetime
def parse_json(input_file):
    result = []
    json_content = json.load(open(input_file))
    apps = json_content.get("apps", "")
    for app in apps:
        languages = app.get("languages", "")
        if languages.get("Kotlin", ""):
            result.append(app)
    return result

input_file = sys.argv[1]

if len(input_file) == 0:
   exit(0) 

result = dict()

if input_file.endswith(".json"):
    result["apps"] = parse_json(input_file)

print(json.dumps(result, indent=4, sort_keys=False))
