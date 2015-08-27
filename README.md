# seeing-is-beliebing
Instagram util for finding photos taken shorty before and after near where another photo was taken.


My phone footage of fans [waiting for Justin Bieber to leave WHTZ's building in Tribeca](https://www.youtube.com/watch?v=-lNVGbobZFA).


Given an Instagram image, this script uses Instagram's API to find all photos within 500 meters and uploaded within 30 minutes before and 240 minutes after of the supplied Instagram image. It then creates a filterable webpage of those images.



Usage:

Assuming that your [Instagram access token](http://www.compciv.org/recipes/data/api-exploration-with-gmaps-instagram/) is in an environmental variable named `$INSTAGRAM_TOKEN`:


~~~sh
    $ python3 beliebe.py "https://instagram.com/p/6xXvJqwi-k"
~~~



## TODO:

- Set origin image
- Add haversine
- Add data to each image
  - lat/lng
  - distance 
  - comments
  - text as a span
- Add sort buttons for:
  + Likes
  + Comments
  + Time 
  + Distance
- Add filter buttons for:
  + Before/after
- Add filter text
