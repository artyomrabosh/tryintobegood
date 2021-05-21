import requests
import urllib.request
import config as cfg
import oss2
import json
import base64
import urllib
import time


# тут всё делается через апи сайта light pdf и файлообменник alibaba

def auth_light():
    return requests.get('http://api.lightpdf.com/api/authentications', headers=cfg.auth_header_lightpdf)


def encode_callback(cb_dict):
    cb_str = json.dumps(cb_dict).strip()
    return oss2.compat.to_string(base64.b64encode(oss2.compat.to_bytes(cb_str)))


def upload_pdf(path, auth_res):
    print("uploading pdf to service")
    data = {
        "id": auth_res['data']['access_id'],
        'path': path,
        'resources': auth_res['data']['path']['resources'],
        'secret': auth_res['data']['access_secret'],
        'token': auth_res['data']['security_token'],
        'endpoint': "http://{}".format(auth_res['data']['endpoint'])
    }
    options = {
        'x-oss-callback': encode_callback(auth_res['data']['callback_url'])
    }
    auth = oss2.StsAuth(data['id'], data['secret'], data['token'])
    bucket = oss2.Bucket(auth, data['endpoint'], auth_res['data']['bucket'])
    oss_result = bucket.put_object_from_file(data['resources'], data['path'], options)
    result = oss_result.resp.read().decode('utf-8').replace("'", '"')
    data = json.loads(result)
    return data


def create_task(uploaded):
    print("converting pdf to xlsx")
    files = [{
        "file_id": uploaded['data']['resource']['resource_id'],
        "password": ""
    }]
    query_files = json.dumps(files)
    params = {
        'service_type': "pdf-to-excel",
        'files': query_files,
        'autostart': 1,
        'args': ''
    }
    link = "http://api.lightpdf.com/api/tasks"
    response = requests.post(link, headers=cfg.task_header_lightpdf, params=params)
    return response.json()


def download_excel(task_id):
    print("downloading xlsx")
    task_link = "http://api.lightpdf.com/api/tasks/{}".format(task_id)
    resp = requests.get(task_link, headers=cfg.auth_header_lightpdf).json()
    file_link = resp['data']['target_file']['url']
    f = open("commands/timetable.xlsx", 'wb')
    f.write(requests.get(file_link).content)
    f.close()
    print("good job!")



def update_timetable():
    for num in range(1, 10):
        print("downloading latest timetable")
        try:
            logo = urllib.request.urlopen(
                cfg.timetable_url.format(num)).read()
            f = open("../try.pdf", "wb")
            f.write(logo)
            f.close()
        except urllib.error.HTTPError:
            print('cant {}'.format(num))
    auth = auth_light()
    uploaded = upload_pdf('../try.pdf', auth.json())
    task = create_task(uploaded)
    time.sleep(7)
    download_excel(task['data']['task_id'])
