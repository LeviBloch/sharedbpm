import random
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
cid = '180a9d94d73f46babd449338483ea951'
secret = '5bb3524d61104251b88ee7619a7af05d'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)




# TODO: quick and dirty, could def be improved
def getRandomSearchQuery():
    commonChars = 'eariotns'
    randomChar = random.choice(commonChars)

    #add wildcard character (unclear if this is working)
    wildcard = '*'
    randomSearch = wildcard + randomChar + wildcard

    return randomSearch


def getRandomTracks(limit):
    results = sp.search(type='track', q=getRandomSearchQuery(), offset=random.randint(0, 999), limit=limit)
    tracks = results['tracks']
    items = tracks['items']
    return items

def getTracks(query, limit):
    # market must be included or else track_preview is sometimes null
    results = sp.search(type='track', q=query, limit=limit, market="US")
    return results['tracks']['items']

def getBPM(id):
    results = sp.audio_features(id)
    return(results[0]['tempo'])


def getTracksAtBPM(bpm):
    seedGenres = random.choices(sp.recommendation_genre_seeds()['genres'], k=5)
    # print(seedGenres)

    seedTracks = []
    seedArtists = []
    randomTracks = getRandomTracks(2)
    for song in randomTracks:
        seedTracks.append(song['id'])
        seedArtists.append(song['artists'][0]['id'])

    # results = sp.recommendations(seed_artists=seedArtists, seed_genres=seedGenres, seed_tracks=seedTracks, limit=10, min_tempo=bpm-1, max_tempo=bpm+1)
    results = sp.recommendations(seed_genres=seedGenres, limit=50, min_tempo=bpm-.5, max_tempo=bpm+.5, target_danceability=100)


    return(results['tracks'])

def orderTracksByBPMAccuracy(tracks):
    tempos = []
    for i in range(0, len(tracks)):
        tempos[i] = (getBPM(tracks[i]['id']))

    for i in range(0, len(tracks)):
        pass
# getSongsAtBPM(120)
