import json
import sys
import os.path
from datetime import datetime
from github import Github
from github.GithubException import RateLimitExceededException
from github.GithubException import UnknownObjectException
from urllib.parse import urlparse

def get_language(repo_url, g):
    repo_url = urlparse(repo_url.strip())
    if repo_url.netloc == "github.com":
        repo_name = repo_url.path[1:]
        try:
            repo = g.get_repo(repo_name)
            languages= repo.get_languages()
            total_of_bytes = sum(languages.values())
            for l in languages:
                languages[l] = (languages[l]/total_of_bytes)*100
            return {"name": repo.name, "repo": repo.html_url, "languages": languages}
        except UnknownObjectException as e:
            print("Impossible to recover language stats from: [%s](%s) - %s" % (repo_name, repo_url.geturl(), e), file=sys.stderr)
        except Exception as e:
            raise e
    else:
        print("Impossible to recover language stats from %s" % repo_url.geturl(), file=sys.stderr)


def parse_json(input_file, field_to_extract, g):
    result = []
    json_content = json.load(open(input_file))
    n_apps = 0
    n_errors = 0
    for app in json_content:
        n_apps += 1
        repo_url = app.get(field_to_extract, "")
        package =""
        if app.get("last_download_url", ""):
            package = app["last_download_url"].split('_')[0][len("https://f-droid.org/repo/"):]
        app = get_language(repo_url, g)
        if app:
            app["package"] = package
            result.append(app)
        else:
            n_errors +=1
    print("From %s apps, %s failed" % (n_apps, n_errors), file=sys.stderr)

    return result

def parse_simple_txt(txt, g):
    result = []
    n_apps = 0
    n_errors = 0
    with open(txt, "rt") as f:
        for repo_url in f.readlines():
            n_apps += 1
            app = get_language(repo_url, g)
            if app:
                result.append(app)
            else:
                n_errors +=1
    print("From %s apps, %s failed" % (n_apps, n_errors), file=sys.stderr)
    return result

input_file = sys.argv[1]

if len(input_file) == 0:
   exit(0) 

result = dict()

g = Github("user", "password")

if input_file.endswith(".json"):
    if len(sys.argv) < 3:
        raise Exception("You need to inform the json field that contais the url repo")
    result["apps"] = parse_json(input_file, sys.argv[2])
elif not os.path.isfile(input_file) and input_file.startswith("https://"):
    result = get_language(input_file, g)
else:
    result["apps"] = parse_simple_txt(input_file, g)

print(json.dumps(result, indent=4, sort_keys=False))
