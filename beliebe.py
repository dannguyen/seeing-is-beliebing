from instagram_utils import get_shortlink_image
from os import environ
import argparse
import json

DEFAULT_TOKEN = environ['INSTAGRAM_TOKEN']
TOKENHELPMSG = "Default is %s" % DEFAULT_TOKEN if DEFAULT_TOKEN else "(no default set)"

parser = argparse.ArgumentParser()
parser.add_argument("shortcode", nargs = 1,
    help = "Instagram web URL/shortcode")
parser.add_argument("--token", '-t', default = DEFAULT_TOKEN,
    help = "Instagram access token %s" % TOKENHELPMSG)
args = parser.parse_args()
shortcode = args.shortcode[0]
access_token = args.token

# get the photo data from the URL/shortcode
image = get_shortlink_image(shortcode, access_token = access_token)
# todo: finish the rest of this
txt = json.dumps(image, indent = 2)
print(txt)
