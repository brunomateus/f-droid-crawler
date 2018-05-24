import json
from pprint import pprint
import sys
from datetime import datetime
from github import Github
from github.GithubException import RateLimitExceededException
from github.GithubException import UnknownObjectException

def get_language(repo_url):
    repo_url = repo_url.strip()
    prefix="https://github.com/"
    if repo_url.startswith(prefix):
        g = Github()
        #g = Github("username", "password_text")
        repo_name = repo_url[len(prefix):]
        try:
            repo = g.get_repo(repo_name)
            languages= repo.get_languages()
            total_of_bytes = sum(languages.values())
            for l in languages:
                languages[l] = (languages[l]/total_of_bytes)*100
            return {"name": repo.name, "languages": languages}
            raise rate_e
        except UnknownObjectException as e:
            print("Impossible to recover language stats from: %s -  %s - Not found 404" % (repo_name, repo_url), file=sys.stderr)
        except Exception as e:
            raise e
    else:
        print("Impossible to recover language stats from %s" % repo_url, file=sys.stderr)


def parse_json(input_file, field_to_extract):
    result = []
    json_content = json.load(open(input_file))
    for app in json_content:
        repo_url = app.get(field_to_extract, "")
        app = get_language(repo_url)
        if app:
            result.append(app)
    return result

def parse_simple_txt(txt):
    result = []
    with open(txt, "rt") as f:
        for repo_url in f.readlines():
            app = get_language(repo_url)
            if app:
                result.append(app)
    return result

input_file = sys.argv[1]

if len(input_file) == 0:
   exit(0) 

result = dict()

if input_file.endswith(".json"):
    if len(sys.argv) < 3:
        raise Exception("You need to inform the json field that contais the url repo")
    result["apps"] = parse_json(input_file, sys.argv[2])
else:
    result["apps"] = parse_simple_txt(input_file)

print(json.dumps(result, indent=4, sort_keys=False))
