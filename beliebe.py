from instagram_utils import get_shortlink_image, get_images_near_coordinates
from os import environ
import argparse
import json

DEFAULT_TOKEN = environ['INSTAGRAM_TOKEN']
TOKENHELPMSG = "Default is %s" % DEFAULT_TOKEN if DEFAULT_TOKEN else "(no default set)"
DEFAULT_BEFORE_MIN = 20
DEFAULT_AFTER_MIN = 20
DEFAULT_DISTANCE_M = 500

parser = argparse.ArgumentParser()
parser.add_argument("shortcode", nargs = 1,
    help = "Instagram web URL/shortcode")
parser.add_argument("--token", '-t', default = DEFAULT_TOKEN,
    help = "Instagram access token %s" % TOKENHELPMSG)
parser.add_argument("--minutes-before", '-b', default = DEFAULT_BEFORE_MIN,
    type = int,
    help = "Limit search to photos X minutes-or-less before target photo's timestamp. Default is %s" % DEFAULT_BEFORE_MIN)
parser.add_argument("--minutes-after", '-a', default = DEFAULT_BEFORE_MIN,
    type = int,
    help = "Limit search to photos X minutes-or-less after target photo's timestamp. Default is %s" % DEFAULT_AFTER_MIN)
parser.add_argument("--distance-in-meters", '-d', default = DEFAULT_DISTANCE_M,
    type = int,
    help = "Limit search to photos . Default is within X number of meeters from target photo location. Default is %s" % DEFAULT_DISTANCE_M)


args = parser.parse_args()
shortcode = args.shortcode[0]
access_token = args.token
seconds_before = args.minutes_before * 60
seconds_after = args.minutes_after * 60
dist_m = args.distance_in_meters

# get the photo data from the URL/shortcode
image = get_shortlink_image(shortcode, access_token = access_token)
image_dmp = json.dumps(image, indent = 2)

# attempt to extract location
try:
    lat = image['location']['latitude']
    lng = image['location']['longitude']
except KeyError as e:
    print("Target image lacks location information")
    print(image_dmp)
    raise e
# extract time as UTC seconds
dts = int(image['created_time'])

near_images = get_images_near_coordinates(lat = lat, lng = lng,
    distance_in_meters = dist_m,
    min_timestamp = dts - seconds_before,
    max_timestamp = dts + seconds_after,
    access_token = access_token
)
near_images_dmp = json.dumps(near_images, indent = 2)
print(near_images_dmp)
