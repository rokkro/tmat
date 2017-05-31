
#from textstat.textstat import textstat
import re

def strip_link(text):
    link = re.sub(r"http\S+", "", text).replace("#","").strip()
    #tag = re.sub(r"#(\w+)","",link)
    user = re.sub(r"@(\w+)","",link)
    if not user.endswith("."):
        user+="."
    return user

def analyze(coll):
    print("lol nice try duuuuuude. This doesnt do anything yet")
    '''
    try:
        cursor = coll.find({})
        for i in cursor:
            if "text" not in i:  # if the current doc doesnt have 'text' field, move on
                continue
            text = strip_link(i['text'])
            if not len(text):
                continue
            print(text,textstat.t(text))
    except Exception as e:
        print(e)
    '''
