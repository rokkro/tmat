# For reference: # https://dev.twitter.com/basics/user-profile-images-and-banners

try:
    import config, requests, base64, os
    from json import JSONDecodeError
except ImportError as e:
    print("Import Error in image.py:", e)

auth_headers = { # authentication keys for the Kairos API, stored in config.py.
    'app_id': config.appid,
    'app_key': config.appkey
}
image_file = "ta-image.jpg"

def remove_image():
    # Deletes downloaded profile pic, if it exists.
    if os.path.exists(image_file):
        os.remove(image_file)


def save_image(response):
    # Download the response as an image file.
    with open(image_file, 'wb') as f:  # convert response into saved image
        f.write(response.content)


def image_base64(file):
    # makes image usable for detect_api()
    with open(file, 'rb') as img:
        return base64.b64encode(img.read()).decode('ascii')


def emotion_api(img):
    # Opens saved image, does a POST request to Kairos Emotion API, returns response.
    url = 'https://api.kairos.com/v2/media'
    with open(img, 'rb') as img:
        response = requests.post(url, files={'source': img}, data={'timeout': 60}, headers=auth_headers)
    return response.json()


def detect_api(img):
    # Kairos 'detection' API, POST request with base64'd image.
    url = 'https://api.kairos.com/detect'
    response = requests.post(url, json={'image': image_base64(img)}, headers=auth_headers)
    return response.json()

def analyze(coll, limit):
    success = 0
    count = 1
    print("Running Image analysis...")
    cursor = coll.find({}, no_cursor_timeout=True)  # find all docs, prevent crashes with no timeout.
    for index, item in enumerate(cursor):  # loop through those
        try:
            if index == limit:  # Stop if limit is hit
                break
            print("\rTweet #" + str(count), "Successful: " + str(success), end=" ", flush=True)  # counter
            count += 1  # current

            profile_pic = item['user']['profile_image_url_https'].replace("_normal", "")  # get image URL

            response = requests.get(profile_pic)
            if response.status_code == 404 or response.status_code == 403:  # dead links to images
                continue

            if item['user']['default_profile_image'] or 'default_profile' in profile_pic:  # filter both default pics
                continue

            save_image(response)
            det = detect_api(image_file)

            if 'Errors' in det:
                error_code = det['Errors'][0]['ErrCode']
                if error_code != 5002:
                    print("Error:", error_code, "-", det['Errors'][0]['Message'] + ". Moving onto the next...")
                continue

            emo = emotion_api(image_file)

            if config.verbose: # Verbose mode output
                print("Document _id:", item.get('_id'))
                print(profile_pic + " " + item['user']['screen_name'])
                print(det)
                print(emo)

            coll.update_one({'_id': item.get('_id')}, {'$set': { # DB insertion
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

    print("\nFinished: " + str(success) + " of " + (str(count - 1) if limit is not None
        else str(cursor.count())) + " successfully processed and inserted!")
    cursor.close()
    remove_image()
