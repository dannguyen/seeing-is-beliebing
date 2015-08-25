# seeing-is-beliebing
Instagram util for finding photos taken shorty before and after near where another photo was taken


Usage:

Assuming that your [Instagram access token](http://www.compciv.org/recipes/data/api-exploration-with-gmaps-instagram/) is in an environmental variable named `$INSTAGRAM_TOKEN`:


~~~sh
    $ python3 beliebe.py "https://instagram.com/p/6xXvJqwi-k"
~~~

Returns a list of photos within TK_DEFAULT feet and TK_BEFORE minutes and TK_AFTER minutes within the supplied Instagram image URL or ID.


(Note: currently only returns data from the given photo)
