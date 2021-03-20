import requests
import json
import sys

params = {"state": "open"}
headers = {
  'Authorization': f'token 0ce2e851e3dc8b5371fbc5e10342450c49e31527',
  'accept' : 'application/vnd.github.v3+json',
  'Content-Type' : 'application/json'
}
heads = ["LEETCODE", "GENERATOR", "ITERATOR","HEXNUMBER", "TRIANGLE", "REQUESTS", "CLA"]
groups = ["1021", "1022"]
actions = ["Added", "Refactored", "Deleted", "Moved", "Fixed"]
data = {
  'body': f'Your title is incorrect',
  'path': '',
  'position': 1,
  'commit_id': ''
}


def get_pulls(name):
    link = "https://api.github.com/repos/{}/python_au/pulls".format(name)
    pulls_req=requests.get(link, headers=headers, params=params)
    return pulls_req.json()


def check_names(names):
    iscorrect = True
    for name in names:
        parts = name.split()
        parts[0] = parts[0].split("-")
        if len(parts) != 3 or len(parts[0]) != 2:
          iscorrect = False
          break
        if parts[0][0] not in heads:
          iscorrect = False
        if parts[0][1] not in groups:
          iscorrect = False
    return iscorrect


def isReviewed(pull):
    comments = requests.get(pull['review_comments_url'], headers=headers,params=params).json()
    for comm in comments:
        if comm['body'] == f'Your title is incorrect':
            print('exist')
            return True
    return False


def review(pull):
  if not isReviewed(pull):
    commit = requests.get(pull['url']+'/files',headers=headers,params=params).json()[0]
    data['path'] = commit['filename']
    data['commit_id'] = pull['head']['sha']
    requests.post(pull['url']+'/comments', data=json.dumps(data).encode('utf8'),headers=headers).json()
  pass


def get_all_commits(pull):
    commits = requests.get(pull['commits_url'], headers=headers, params=params)
    return commits.json()


def verify(pull):
    names = [pull['title']]
    for commit in get_all_commits(pull):
        names.append(commit['commit']['message'])
    if check_names(names) is False:
        review(pull)


def main():
    username = input()
    for pull in get_pulls(username):
        verify(pull)


if __name__ == '__main__':
    main()




