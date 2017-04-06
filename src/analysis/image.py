import requests, base64,config, os

auth_headers={
    'app_id': config.appid,
    'app_key': config.appkey
}
def get_image(response):
    with open('image.jpg','wb') as f: #convert response into saved image
        f.write(response.content)
    return "image.jpg"

def image_base64(file): #makes image usable for detect()
    with open(file,'rb') as img:
        return base64.b64encode(img.read()).decode('ascii')

def emotion(img):
    url = 'https://api.kairos.com/v2/media'
    with open(img,'rb') as img:
        response = requests.post(url, files={'source': img}, data={'timeout':60}, headers=auth_headers)
    print(response.json())
    return response.json()

def detect(img):
    url = 'https://api.kairos.com/detect'
    response = requests.post(url,json={'image':image_base64(img)},headers=auth_headers)
    print(response.json())
    return response.json()

#https://dev.twitter.com/basics/user-profile-images-and-banners
def insert_data(coll):
    cursor = coll.find({})  # finds all documents in collection
    for i in cursor:  # loop through those
        profile_pic =i['user']['profile_image_url_https'].replace("_normal","")
        response = requests.get(profile_pic)
        if response.status_code == 404 or response.status_code == 403: #dead links to images
            continue
        #print(response.headers)
        #print(response)
        if not i['user']['default_profile_image'] and 'default_profile' not in profile_pic: #filter both default pics
            print(profile_pic + " " + i['user']['screen_name'])
            img = get_image(response)
            det = detect(img)
            if 'Errors' in det:
                print("Error:", det['Errors'][0]['ErrCode'] , "-", det['Errors'][0]['Message'])
                continue
            emo =emotion(img)

            coll.update_one({'_id': i.get('_id')}, {'$set': {
                "face": {
                    "emotion":emo,
                    "detection": det
                }}})
        else:
            #print(profile_pic+ " DEFAULT!" + " " + i['user']['screen_name'])
            continue
    os.remove("image.jpg")
