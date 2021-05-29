import requests
import config
params = {"state": "open"}
headers = {
  'Authorization': f'token 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',
  'accept' : 'application/vnd.github.v3+json',
  'Content-Type' : 'application/json'
}

def get_pulls(name):
    link = "https://api.github.com/repos/{}/python_au/pulls".format(name)
    pulls_req=requests.get(link, headers=headers, params=params)
    return pulls_req.json()


