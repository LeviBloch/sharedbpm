import requests
import json

IMVDB_API_KEY = 'YelFow220HzyToY4yhLxNwRWYTJF33XJIOper6qi'

# todo: loop through results to find one that has matching title and artist
# returns yt video id, or an empty string if none exists
def getMusicVideo(title, artist):
    response = requests.get('https://imvdb.com/api/v1/search/videos',
                            params={'q': title + ' ' + artist},
                            headers={'IMVDB-APP-KEY': IMVDB_API_KEY})

    if response.json() == None or 'results' not in response.json() or len(response.json()['results']) == 0:
        print('no results found in initial search')
        return ''

    id = response.json()['results'][0]['id']

    response = requests.get('https://imvdb.com/api/v1/video/' + str(id), params={'include': 'sources'})

    # print(json.dumps(response.json(), indent=2))

    if 'sources' in response.json():
        for source in response.json()['sources']:
            if source['source'] == 'youtube':
                return source['source_data']
    else:
        print('no video sources in response')
        return ''

    # no source is a yt video
    print('no source from youtube')
    return ''





# print(getMusicVideo("never gonna give you up", "rick astley"))