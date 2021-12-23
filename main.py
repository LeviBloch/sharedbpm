import subprocess
import pytube
import shutil
import json
import requests
import ffmpeg

import spotipy_test
import imvdb_test
import youtube_test


# returns True if successful, False if there was an error
def downloadVideo(id):
    try:
        # todo: can probably use just the id
        yt = pytube.YouTube('https://www.youtube.com/watch?v=' + str(id))
    except:
        print("Connection Error")
        return False

    # could potentially cause problems if no audio-only streams exist
    try:
        stream = yt.streams.filter(only_video=True).first()
        stream.download(output_path="./raw", filename="video.mp4")
    except:
        print('Error, probably video unavailable')
        return False

    return True

def downloadAudio(id):
    try:
        # todo: can probably use just the id
        yt = pytube.YouTube('https://www.youtube.com/watch?v=' + str(id))
    except:
        print("Connection Error")
        return False

    # could potentially cause problems if no audio-only streams exist
    try:
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path="./raw", filename="audio.mp4")
    except Exception as e:
        print('Error, probably video unavailable')
        print(e)
        return False

    return True

def mergeVideoAndAudio():
    cmd = "ffmpeg -i ./raw/video.mp4 -i ./raw/audio.mp4 -map 0:v -map 1:a -c copy ./output.mp4"
    subprocess.call(cmd, shell=True)


def test():
    # # delete old audio/video files
    # should use an if to check
    try:
        shutil.rmtree("./raw")
        shutil.rmtree("./output")
    except:
        pass

    # get user input for first song
    inputQuery = input("Enter a song: ")

    # search for query
    tracks = spotipy_test.getTracks(inputQuery, 5)

    # print results
    # todo: show multiple artists
    for i in range(0, len(tracks)):
        print(str(i+1) + ') ' + tracks[i]['name'] + ' by ' + tracks[i]['artists'][0]['name'])

    # get track from tracks
    trackNum = int(input("Which number? ")) - 1
    track = tracks[trackNum]

    # get youtube vid of track
    audioYTId = youtube_test.getYoutubeId(track['name'], track['artists'][0]['name'])


    # print(json.dumps(track, indent=2))

    bpm = spotipy_test.getBPM(track['id'])

    resultTracks = spotipy_test.getTracksAtBPM(bpm)

    # for i in range(0, len(resultTracks)):
    #     print(str(i+1) + ') ' + resultTracks[i]['name'] + ' by ' + resultTracks[i]['artists'][0]['name'])

    # # get track from tracks
    # resultTrackNum = int(input("Which number? ")) - 1
    # resultTrack = tracks[resultTrackNum]
    # print(resultTrack)

    # find a track that has a music video
    for track in resultTracks:
        mv = imvdb_test.getMusicVideo(track['name'], track['artists'][0]['name'])
        if len(mv) > 0:
            print('music video found: ' + track['name'] + ' by ' + track['artists'][0]['name'])


            # todo: check if youtube video is unavailable, and if so, try again

            choice = 0
            choice = input('1) Your input is the audio\n2) Your input is the video\nChoice: ')
            if choice == '1':
                downloadAudio(audioYTId)
                downloadVideo(mv)
            elif choice == '2':
                downloadAudio(mv)
                downloadVideo(audioYTId)
            mergeVideoAndAudio()

            return

def main():
    test()

if __name__ == '__main__':
    main()
