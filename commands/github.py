import requests
import config
params = {"state": "open"}
headers = {
  'Authorization': f'token ghp_C8SVmi2FjAmxHdu4uwCx6kdInwjZbH2nESs',
  'accept' : 'application/vnd.github.v3+json',
  'Content-Type' : 'application/json'
}

def get_pulls(name):
    link = "https://api.github.com/repos/{}/python_au/pulls".format(name)
    pulls_req=requests.get(link, headers=headers, params=params)
    return pulls_req.json()


