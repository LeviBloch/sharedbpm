import requests
import json

YOUTUBE_API_KEY = "AIzaSyCwZ8HeUWrAxKMK6Z9R3sQ1GScSM91pGG8"

# todo: check song and artist in a more intelligent way
def getYoutubeId(song, artist):
    response = requests.get("https://www.googleapis.com/youtube/v3/search",
                            params={'part': 'snippet', 'maxResults': '5', 'type': 'video', 'q': song + ' ' + artist, 'key': YOUTUBE_API_KEY})

    return response.json()['items'][0]['id']['videoId']