import requests
INSTAGRAM_DOMAIN = 'https://api.instagram.com'
MEDIA_PATH = '/v1/media/shortcode/%s'

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



def get_images_near_coordinates(access_token, lat, lng, min_timestamp = '2000-01-01', max_timestamp = "TKTK"):
    """
    https://instagram.com/developer/endpoints/media/#get_media_search
    """
