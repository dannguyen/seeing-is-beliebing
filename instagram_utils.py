import requests
import json
from datetime import datetime
INSTAGRAM_DOMAIN = 'https://api.instagram.com'
MEDIA_PATH = '/v1/media/shortcode/%s'
MEDIA_SEARCH_PATH = '/v1/media/search'

def extract_shortcode(weburl):
    """
    weburl (String):
        Can be either:
        - "https://instagram.com/p/6xXvJqwi-k/?taken-by=danwinny"
        - "6xXvJqwi-k"
    returns (String):
        "6xXvJqwi-k"
    """
    u = weburl.split('instagram.com/p/')
    if len(u) > 1:
        x = u[1]
        return x.split('/')[0]
    else: # just return whatever you got
        return weburl

def get_image_from_shortcode(shortcode, access_token):
    """
    shortcode (str):
        A web shortcode for an instagram image, e.g.
        '6xXvJqwi-k' from "https://instagram.com/p/6xXvJqwi-k"
    returns (dict):
        An object representing an Instagram image
    """
    path = MEDIA_PATH % shortcode
    url = INSTAGRAM_DOMAIN + path
    atts = {"access_token": access_token}
    resp = requests.get(url, params = atts).json()
    return resp['data']



def get_images_near_coordinates(lat, lng, distance_in_meters,
            min_timestamp, max_timestamp, access_token):
    """

    returns (list)"
        A list of all images found in the search

    more info:
    https://instagram.com/developer/endpoints/media/#get_media_search
    """
    images_dict = {}
    ix = 0
    atts = {
        'access_token': access_token,
        'distance': distance_in_meters,
        'lat': lat,
        'lng': lng,
        'min_timestamp': min_timestamp,
        'max_timestamp': max_timestamp
    }
    base_url = INSTAGRAM_DOMAIN + MEDIA_SEARCH_PATH
    # Now continually fetch from Instasgram until no more results are found
    while True:
        print("%s loop; from %s to %s:\t%s images total" % (ix,
                datetime.fromtimestamp(atts['min_timestamp']),
                datetime.fromtimestamp(atts['max_timestamp']),
                len(images_dict)))
        try:
            ix += 1
            resp = requests.get(base_url, params = atts).json()
            new_images = resp['data']
        except Exception as e:
            print("There was an error while retrieving images on %s loop" % ix)
            print(e)
            break
        except KeyboardInterrupt:
            break
        else:
            if new_images:
                # i'm sure there's a better way to prevent dupes...
                for img in new_images:
                    images_dict[img['id']] = img
                # get new max timestamp from oldest image in the latest batch
                #  and subtract one second
                oldest_ts = int(new_images[-1]['created_time']) - 1
                # Instagram's search filter is lax so sometimes photos
                #  that are newer than max_timestamp are let in...we need to do
                #  our own check
                if oldest_ts >= atts['max_timestamp'] or atts['min_timestamp'] >= atts['max_timestamp']:
                    break
                else:
                    atts['max_timestamp'] = oldest_ts

            else:
                print("get out")
                break # out of while loop
        # end try/else
    # end while
    return list(images_dict.values())


def get_images_near_some_other_image_via_shortcode(shortcode, access_token,
    seconds_before, seconds_after, dist_m):
    """
    An omni-wrapper method

    shortcode (str):
        A web shortcode for an instagram image, e.g.
        '6xXvJqwi-k' from "https://instagram.com/p/6xXvJqwi-k"
    returns (list):
        A list of images near `image` as extracted from Instagram media search
    """

    origin_image = get_image_from_shortcode(shortcode, access_token)
    # attempt to extract location
    try:
        lat = origin_image['location']['latitude']
        lng = origin_image['location']['longitude']
    except (KeyError, TypeError) as e:
        print("Target image lacks location information")
        print(json.dumps(origin_image, indent = 2))
        raise e
    # extract time as UTC seconds
    dts = int(origin_image['created_time'])

    nearby_images = get_images_near_coordinates(lat = lat, lng = lng,
        distance_in_meters = dist_m,
        min_timestamp = dts - seconds_before,
        max_timestamp = dts + seconds_after,
        access_token = access_token
    )

    # ad-hoc, add a label to the origin_image as found by the shortcode
    for img in nearby_images:
        if img['id'] == origin_image['id']:
            img['is_origin'] = True
            break

    return nearby_images
