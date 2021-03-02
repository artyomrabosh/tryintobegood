import requests
import json

params = {"state": "open",}
headers = {
  'Authorization': f'token dea9e8c41e8c6032bdd92946f53f3667c4ef89b1',
  'accept' : 'application/vnd.github.v3+json',
  'Content-Type' : 'application/json'
}
heads = ["LEETCODE", "GENERATOR", "ITERATOR","HEXNUMBER", "TRIANGLE", "REQUESTS"]
groups = ["1021", "1022"]
actions = ["Added", "Refactored", "Deleted", "Moved", "Fixed", "ADDED"]
data = {
  'body' : f'Your title is incorrect',
  'path' : '',
  'position' : 1,
  'commit_id' : '6f3ccdb0f8941f66c37342d5ac34c3c1c8010d8b'
}

def get_pulls(name):
  link = "https://api.github.com/repos/{}/python_au/pulls".format(name)
  pulls_req=requests.get(link, headers=headers, params=params)
  return pulls_req.json()


def get_names(pull):
  names=[pull['title']]
  commits=requests.get(pull['commits_url'], headers=headers, params=params)
  for commit in commits.json():
    names.append(commit['commit']['message'])
  return check_names(names)


def check_names(names):
  isCorrect = True
  for name in names :
    parts=name.split()
    parts[0]=parts[0].split("-")
    if len(parts) != 3 or len(parts[0]) !=2:
      isCorrect = False
      break
    if parts[0][0] not in heads:
      isCorrect = False
    if parts[0][1] not in groups:
      isCorrect = False
  return isCorrect


def review(pull):
  commit = requests.get(pull['url']+'/files',headers=headers,params=params).json()[0]
  data['path'] = commit['filename']
  data['commit_id'] = pull['head']['sha']
  print(data)
  print(requests.post(pull['url']+'/comments', data=json.dumps(data).encode('utf8'),headers=headers).json())
  pass


def main():
  name = input()
  for pull in get_pulls(name):
    if(get_names(pull)):
      print("good")
    else:
      print("bad")
      review(pull)


main()
#print(requests.post('https://api.github.com/repos/artyomrabosh/python_au/pulls/23/comments', data = json.dumps(data).encode('utf8'), headers = headers).json())



