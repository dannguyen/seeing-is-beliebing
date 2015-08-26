import requests
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

def get_shortlink_image(weburl, access_token):
    """
    weburl (String):
        Can be either:
        - "https://instagram.com/p/6xXvJqwi-k/?taken-by=danwinny"
        - "6xXvJqwi-k"
    returns (dict):
        An object representing an Instagram image
    """
    shortcode = extract_shortcode(weburl)
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
    images = []
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
                len(images)))
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
                images.extend(new_images)
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
    return images
