# For reference: # https://dev.twitter.com/basics/user-profile-images-and-banners

try:
    import time
    from config import conf
    import requests, base64, os
    from json import JSONDecodeError
except ImportError as e:
    print("Import Error in image.py:", e)



class Image():
    AUTH_HEADERS = {  # authentication keys for the Kairos API, stored in config.py.
        'app_id': conf['appid'],
        'app_key': conf['appkey']
    }
    IMAGE_FILE = "ta-image.jpg"
    RETRY_LIM = 5
    MAX_LIM = 1500
    STOP_TIMER = 86460

    def __init__(self):
        self.calls = 0


    def remove_image(self):
        # Deletes downloaded profile pic, if it exists.
        if os.path.exists(self.IMAGE_FILE):
            os.remove(self.IMAGE_FILE)


    def save_image(self,response):
        # Download the response as an image file.
        with open(self.IMAGE_FILE, 'wb') as f:  # convert response into saved image
            f.write(response.content)


    def image_base64(self,file):
        # makes image usable for detect_api()
        with open(file, 'rb') as img:
            return base64.b64encode(img.read()).decode('ascii')


    def emotion_api(self,img):
        # Opens saved image, does a POST request to Kairos Emotion API, returns response.
        url = 'https://api.kairos.com/v2/media'
        with open(img, 'rb') as img:
            response = requests.post(url, files={'source': img}, data={'timeout': 60}, headers=self.AUTH_HEADERS)
        self.calls+=1
        return response.json()


    def detect_api(self,img):
        # Kairos 'detection' API, POST request with base64'd image.
        url = 'https://api.kairos.com/detect'
        response = requests.post(url, json={'image': self.image_base64(img)}, headers=self.AUTH_HEADERS)
        self.calls+=1
        return response.json()

    def run(self,api_func):
        retry_count = 0
        sleep_time = 5
        while True:
            try:
                result = api_func(self.IMAGE_FILE)
                if 'Errors' in result:
                    error_code = result['Errors'][0]['ErrCode']
                    if error_code != 5002:
                        print("Error:", error_code, "-", result['Errors'][0]['Message'] + ". Moving onto the next...")
                    raise TypeError
                return result
            except JSONDecodeError as e:
                if retry_count > self.RETRY_LIM:
                    raise Exception("Possible Kairos Error, verify your keys are accurate:",e)
                time.sleep(sleep_time)
                sleep_time*=2
                retry_count +=1
                continue

    def analyze(self, coll, limit):
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

                if self.calls < self.MAX_LIM:
                    self.save_image(response)
                    det = self.run(self.detect_api)
                    emo = self.run(self.emotion_api)
                else:
                    print("Sleeping for 86460 seconds...")
                    time.sleep(self.STOP_TIMER)
                    self.calls = 0


                if conf['verbose']: # Verbose mode output
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
            except TypeError:
                self.remove_image()
                continue
            except KeyboardInterrupt:
                self.remove_image()
                print("\n")
                return
            except KeyError:
                continue
            except Exception as e:
                print("Error:", e)
                self.remove_image()
                continue

        print("\nFinished: " + str(success) + " of " + (str(count - 1) if limit is not None
            else str(cursor.count())) + " successfully processed and inserted!")
        cursor.close()
        self.remove_image()
