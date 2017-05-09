try:
    from display import Color
    import config, requests, base64, os
    from json import JSONDecodeError
except ImportError as e:
    print("Error", e)

auth_headers = {
    'app_id': config.appid,
    'app_key': config.appkey
}


def remove_image():
    if os.path.exists("ta-image.jpg"):
        os.remove("ta-image.jpg")


def save_image(response):
    with open('ta-image.jpg', 'wb') as f:  # convert response into saved image
        f.write(response.content)
    return "ta-image.jpg"


def image_base64(file):  # makes image usable for detect_api()
    with open(file, 'rb') as img:
        return base64.b64encode(img.read()).decode('ascii')


def emotion_api(img):
    url = 'https://api.kairos.com/v2/media'
    with open(img, 'rb') as img:
        response = requests.post(url, files={'source': img}, data={'timeout': 60}, headers=auth_headers)
    return response.json()


def detect_api(img):
    url = 'https://api.kairos.com/detect'
    response = requests.post(url, json={'image': image_base64(img)}, headers=auth_headers)
    return response.json()


# https://dev.twitter.com/basics/user-profile-images-and-banners
def insert_data(coll, limit):
    success = 0
    count = 1
    print(Color.YELLOW + "Running Image analysis..." + Color.END)
    cursor = coll.find({}, no_cursor_timeout=True)  # finds all documents in collection
    for index, item in enumerate(cursor):  # loop through those
        try:
            if index == limit:  # if hit the limit
                break
            print("\rTweet #" + str(count), "Successful: " + str(success), end=" ", flush=True)  # counter
            count += 1  # current

            profile_pic = item['user']['profile_image_url_https'].replace("_normal", "")  # get image URL

            response = requests.get(profile_pic)
            if response.status_code == 404 or response.status_code == 403:  # dead links to images
                continue

            if item['user']['default_profile_image'] or 'default_profile' in profile_pic:  # filter both default pics
                continue

            img = save_image(response)
            det = detect_api(img)

            if 'Errors' in det:
                error_code = det['Errors'][0]['ErrCode']
                if error_code != 5002:
                    print("Error:", error_code, "-", det['Errors'][0]['Message'] + ". Moving onto the next...")
                continue

            emo = emotion_api(img)

            if config.verbose:
                print("Document _id:", item.get('_id'))
                print(profile_pic + " " + item['user']['screen_name'])
                print(det)
                print(emo)

            coll.update_one({'_id': item.get('_id')}, {'$set': {
                "face": {
                    "emotion": emo,
                    "detection": det
                }}})
            success += 1  # successfully inserted
        except JSONDecodeError as e:
            print("Possible Kairos Error, verify your keys are accurate:", e)
            remove_image()
            return
        except KeyboardInterrupt:
            remove_image()
            print("\n")
            return
        except KeyError:
            continue
        except BaseException as e:
            print(type(e), "Error:", e)
            remove_image()
            continue

    print(Color.YELLOW + "\nFinished: " + str(success) + " of " + (str(count - 1) if limit is not None
        else str(cursor.count())) + " successfully processed and inserted!" + Color.END)
    cursor.close()
    remove_image()
