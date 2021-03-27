import requests
import urllib.request
import config as cfg
import oss2
import random
import string
import json
import time


def auth_lightpdf():
    return requests.get('http://api.lightpdf.com/api/authentications', headers = cfg.auth_header_lightpdf)


def upload_pdf(path, auth_res):
    data = {
        "id" : auth_res['data']['access_id'],
        'path': 'try.pdf',
        'resourses': auth_res['data']['path']['resources'],
        'secret' : auth_res['data']['access_secret'],
        'token' : auth_res['data']['security_token'],
        'endpoint' : "http://{}".format(auth_res['data']['endpoint'])
    }
    options = {
        'x-oss-callback' : json.dumps(auth_res['data']['callback_url']).encode(('base64'))
    }
    auth = oss2.StsAuth(data['id'], data['secret'], data['token'])
    bucket = oss2.Bucket(auth, data['endpoint'], auth_res['data']['bucket'])
    result = bucket.put_object_from_file(data['resourses'], data['path'], options)
    print(result.resp.read())
    return result


def create_task(uploaded):
    files = [{
        "file_id" : uploaded.crc,
        "password" : ""
    }]
    params = {'headers':cfg.task_header_lightpdf}
    service_type = "pdf-to-excel"
    link = "http://api.lightpdf.com/api/tasks"
    data = json.dumps(files).encode('utf8')
    response = requests.post(link, headers=cfg.auth_header_lightpdf, data=data)
    return response.json()


def download_excel(task):
    task_link = task['task_url']
    result = requests.get(task_link,headers=cfg.auth_header_lightpdf)
    table = urllib.request.urlopen(result['target_file']['url'], ).read
    file = open('timetable.xlsx', 'wb')
    file.write(table)
    file.close()
    return file

def update_timetable():
    for num in range(1, 10):
        try:
            logo = urllib.request.urlopen(
                cfg.timetable_url.format(num)).read()
            f = open("try.pdf", "wb")
            f.write(logo)
            f.close()
        except urllib.error.HTTPError:
            print('cant {}'.format(num))
    auth = auth_lightpdf()

    print(auth.json())
    uploaded = upload_pdf('try.pdf', auth.json())
    task = create_task(uploaded)
    time.sleep(30)
    timetable = download_excel(task)
    return timetable

update_timetable()