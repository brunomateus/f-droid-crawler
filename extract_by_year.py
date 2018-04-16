import json
from pprint import pprint
import sys
from datetime import datetime
result = sys.argv[1]


jsonlen = len(result)

if jsonlen == 0:
   exit(0) 

data = json.load(open(result))

result = []
target = int(sys.argv[2])

for app in data:
    last_version_year = datetime.strptime(app['last_added_on'], "%Y-%m-%d").date().year
    if last_version_year == target:
        result.append(app)

print('[' + ',\n'.join(json.dumps(i, sort_keys=True) for i in result) + ']\n') 
