import requests, base64,config

auth_headers={
    'app_id': config.appid,
    'app_key': config.appkey
}

def image_base64(file):
    with open(file,'rb') as img:
        return base64.b64encode(img.read()).decode('ascii')

def emotion():
    url = 'https://api.kairos.com/v2/media'
    with open("test.jpg",'rb') as img:
        response = requests.post(url, files={'source': img}, data={'timeout':60}, headers=auth_headers)
    print(response.json())

def detect():
    url = 'https://api.kairos.com/detect'
    response = requests.post(url,json={'image':image_base64("test.jpg")},headers=auth_headers)
    print(response.json())
