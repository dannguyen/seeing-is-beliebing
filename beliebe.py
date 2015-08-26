from datetime import datetime
from instagram_utils import extract_shortcode, get_images_near_some_other_image_via_shortcode
from os import environ, makedirs
from os.path import join
from shutil import copytree
import argparse
import json

DEFAULT_TOKEN = environ['INSTAGRAM_TOKEN']
TOKENHELPMSG = "Default is %s" % DEFAULT_TOKEN if DEFAULT_TOKEN else "(no default set)"
DEFAULT_BEFORE_MIN = 30
DEFAULT_AFTER_MIN = 240
DEFAULT_DISTANCE_M = 500


def beliebe(shortcode, args):
    """
    TODO: make args better
    returns:
      a lot of stuff
    """

    access_token = args.token
    bargs = {}
    bargs['access_token'] = access_token
    bargs['seconds_before'] = args.minutes_before * 60
    bargs['seconds_after'] = args.minutes_after * 60
    bargs['dist_m'] = args.distance_in_meters

    nearby_images = get_images_near_some_other_image_via_shortcode(shortcode, **bargs)
    return nearby_images


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("shortcode", nargs = 1,
        help = "Instagram web URL/shortcode")
    parser.add_argument("--token", '-t', default = DEFAULT_TOKEN,
        help = "Instagram access token %s" % TOKENHELPMSG)
    parser.add_argument("--minutes-before", '-b', default = DEFAULT_BEFORE_MIN,
        type = int,
        help = "Limit search to photos X minutes-or-less before target photo's timestamp. Default is %s" % DEFAULT_BEFORE_MIN)
    parser.add_argument("--minutes-after", '-a', default = DEFAULT_AFTER_MIN,
        type = int,
        help = "Limit search to photos X minutes-or-less after target photo's timestamp. Default is %s" % DEFAULT_AFTER_MIN)
    parser.add_argument("--distance-in-meters", '-d', default = DEFAULT_DISTANCE_M,
        type = int,
        help = "Limit search to photos . Default is within X number of meters from target photo location. Default is %s" % DEFAULT_DISTANCE_M)

    args = parser.parse_args()
    shortcode = extract_shortcode(args.shortcode[0])
    print("Fetching images near %s" % shortcode)
    nearby_images = beliebe(shortcode, args)
    pdir = "./pages/" + shortcode + '--' + datetime.now().strftime("%Y-%m-%d_%H%M%S")
    # save into directory
    copytree('./template', pdir)
    datadir = join(pdir, 'data')
    makedirs(datadir)
    with open(join(datadir, 'images.json'), 'w') as fd:
        json.dump(nearby_images, fd, indent = 2)

    print("""
    Run:
         python3 -m http.server

    In your browser, visit:
         http://localhost:8000/{page_path}
""".format(page_path = pdir[2:]))
