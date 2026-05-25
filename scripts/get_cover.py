import urllib.parse, urllib.request, json, os, sys
keywords = os.environ.get('VIDEO_KEYWORDS') or os.environ.get('SONG_TITLE', 'music')
key = os.environ.get('PIXABAY_KEY', '')
q = urllib.parse.quote(keywords)
url = "https://pixabay.com/api/?key=" + key + "&q=" + q + "&image_type=photo&per_page=3&min_width=500&min_height=500"
try:
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    hits = data.get('hits', [])
    cover = hits[0]['largeImageURL'] if hits else ''
except Exception:
    cover = ''
print(cover)
