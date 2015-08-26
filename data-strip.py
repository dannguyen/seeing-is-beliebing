# convenience script to obfuscate, but not completely redact, *some*
# identifier information from a list of Instagram images, such as
# all likes and commenters. Image unique ID is left in so original data
# can be recovered
import json
from random import choice
from string import ascii_letters, digits

FNAME = './examples/images.json'
jdata = json.load(open(FNAME))
# the example file can be expected to contain standard Instagram response with 'data' attribute
# or just the list extracted from the original response's 'data' attribute
images = jdata if isinstance(jdata, list) else jdata['data']
print("Number of images: %s" % len(images))
for img in images:
    # remove comments and likes
    img['likes']['data'] = []
    img['likes']['count'] = 0
    img['comments']['data'] = []
    img['comments']['count'] = 0
    # remove user info, nominally
    tk_username = "".join(choice(ascii_letters) for i in range(10))
    tk_user_id = "".join(choice(digits) for i in range(12))
    tk_user_fullname = "Doe " + "".join(choice(ascii_letters) for i in range(5))
    img['user']['username'] = tk_username
    img['user']['full_name'] = tk_user_fullname
    img['user']['id'] = tk_user_id
    # edit caption info
    if img.get('caption'):
        img['caption']['from']['username'] = tk_username
        img['caption']['from']['full_name'] = tk_user_fullname
        img['caption']['from']['id'] = tk_user_id


print(json.dumps(images, indent = 2))
