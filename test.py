# 1. Log into Youtube
# 2. Get the music Videos from the selected Playlists
# 3. Log into Spotify
# 4. Create a (new) Youtube playlist in Spotify
# 5. Search for the song in Spotify
# 6. Add the song to the playlist


import json
import requests
from youtube_client_secret import youtube_data_api_key, youtube_analytics_api_key

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import youtube_dl

# def get_youtube_client(self, youtube_credentials):
#     """ Log Into Youtube, Copied from Youtube Data API """
#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
#
#     api_service_name = "youtube"
#     api_version = "v3"
#
#     # Get credentials and create an API client
#     scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         youtube_credentials, scopes)
#     credentials = flow.run_console()
#
#     # from the Youtube DATA API
#     youtube_client = googleapiclient.discovery.build(
#         api_service_name, api_version, credentials=credentials)
#
#     return youtube_client

class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track

""" Log Into Youtube, Copied from Youtube Data API """
# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = 'youtube'
api_version = 'v3'
client_secrets_file = 'client_secret_desktop.json'

# Get credentials and create an API client
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()

# from the Youtube DATA API
youtube_client = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

self.spotify_user_id = spotify_user_id
self.spotify_token = spotify_token
self.youtube_client = self.get_youtube_client()
self.all_track_info = {}

"""Get the music Videos from the selected Playlists & create a dictionary of important track information"""
requests = youtube_client.videos().list(
    part="snippet,contentDetails,statistics",
    myRating="like"
)
response = requests.execute()

# Collect each video and get important information
for item in response["items"]:
    video_title = item["snippet"]["title"]
    youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

    # Use youtube_dl to collect the track and artist name
    video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
    track_name = video["track"]
    artist = video["artist"]

    # Save information
    self.all_track_info[video_title] = {
        "youtube_url": youtube_url,
        "track_name": track_name,
        "artist": artist,

        # Add the uri: easy to get track to put into a playlist
        "spotify_uri": self.get_spotify_url(track_name, artist)
    }


request = youtube_client.playlists().list(
    part="id, snippet",
    maxResults=50,
    mine=True
)
response = request.execute()

playlists = [playlist for playlist in response['items']]
playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

playlists




import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl

import json
import requests



class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class Track(object):
    def __init__(self, artist, track_name, youtube_url):
        self.artist = artist
        self.track_name = track_name
        self.youtube_url = youtube_url
        #self.spotify_uri = spotify_uri


def get_youtube_client():
    """Log into Youtube"""
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOTE* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = 'client_secret_desktop.json'

    # Get credentials and create an API client
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()

    # from the Youtube DATA API
    youtube_cred = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    return youtube_cred

youtube_cred = get_youtube_client()


def get_playlists():
    request = youtube_cred.playlists().list(
        part="id, snippet",
        maxResults=100,
        mine=True
    )
    response = request.execute()

    playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

    return playlists

playlists = get_playlists()

for index, playlist in enumerate(playlists):
    print("{}: {}".format(index, playlist.title))
choices = list(map(int, input("Enter the indexes of the different playlists to select: ").split())) # separated by a space
print("List of playlists: {}".format(choices))


def get_music_videos_from_playlist(playlist_id):
    tracks = []
    request = youtube_cred.playlistItems().list(
        playlistId=playlist_id,
        part="id, snippet",
        maxResults=500
    )
    response = request.execute()

    # Collect each video and get important information
    for item in response['items']:
        video_id = item['snippet']['resourceId']['videoId']

        # Use youtube_dl to collect the track and artist name
        youtube_url = "https://www.youtube.com/watch?v={}".format(video_id)
        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(youtube_url, download=False)

        # Save information
        artist = video['artist']
        track_name = video['track']

        # Add the uri: easy to get track to put into a playlist
        #"spotify_uri": self.get_spotify_url(track_name, artist)

        if artist and track_name:
            tracks.append(Track(artist, track_name, youtube_url))


    return tracks

tracks = get_music_videos_from_playlist(chosen_playlist.id)
print(f"Attempting to add {len(tracks)}")
print(tracks)






def get_spotify_url(track_name, artist):
    """Search for the song in Spotify"""
    query = 'https://api.spotify.com/v1/search?q=track%3A{}+artist%3A{}&type=track&offset=0&limit=20'.format(
        track_name,
        artist
    )
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()
    tracks = response_json["tracks"]["items"]

    # only use the first song
    url = tracks[0]["uri"]
    return url



def get_music_videos_from_playlist2(playlist_id):
    tracks = []
    request = youtube_client.playlistItems().list(
        playlistId=playlist_id,
        part="id, snippet",
        maxResults=500
    )
    response = request.execute()

    all_track_info = {}
    # Collect each video and get important information
    for item in response['items']:
        video_id = item['snippet']['resourceId']['videoId']

        # Use youtube_dl to collect the track and artist name
        youtube_url = "https://www.youtube.com/watch?v={}".format(video_id)
        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(youtube_url, download=False)

        # Save information
        artist = video['artist']
        track_name = video['track']

        video_title = item["snippet"]["title"]

        # Add the uri: easy to get track to put into a playlist

        #"spotify_uri": self.get_spotify_url(track_name, artist)
        if track_name is not None and artist is not None:
            # save all important info and skip any missing song and artist
            all_track_info[video_title] = {
                "youtube_url": youtube_url,
                "track_name": track_name,
                "artist": artist
                # ,

                # add the uri, easy to get song to put into playlist
                # "spotify_uri": get_spotify_uri(song_name, artist)
            }

        # Save information

        if artist and track_name:
            tracks.append(Track(artist, track_name, youtube_url))


    return tracks, all_track_info


spotify_token = "BQAJSZiN0P42G18nrzVoQGf9rnK5nyzG81c3TENk9aRplr1rfLpi8dXrRCG2HJxDY-61doOYHuOK6DygwySejDb_Fi7wJ-4mFMKD-FRvhmY0FqNBvuEQNhQG-ZTWtWP8hHPREseP2PpgzwofT3TS05dTtXOwSWAuhxG32C47mrjNFd45Row9T_yfpTTMuw8sCKRlUgu_4ib_-ao"
spotify_user_id = '1114332950'


def create_playlist():
    """Create A New Playlist"""
    request_body = json.dumps({
        "name": "Test3",  # Tracks from Youtube Playlists
        "public": True,
        "collaborative": False
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
    response = requests.post(query, data=request_body, headers={"Content-Type": "application/json",
                                                                "Authorization": "Bearer {}".format(spotify_token)}
                             )

    response_json = response.json()
    print(response_json)

    # playlist id
    playlist_id = response_json["id"]

    return playlist_id



def search_spotify_tracks_uri(artist, track_name):
    """Search For the Song"""
    query = urllib.parse.quote('{} {}'.format(artist, track_name))
    url = "https://api.spotify.com/v1/search?q={}&type=track".format(query)

    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )
    response_json = response.json()
    results = response_json['tracks']['items']

    if results:
        # let's assume the first track in the list is the song we want
        return results[0]['uri']
    else:
        # raise Exception(f"No song found for {artist} = {track_name}")
        print("No song found for {} - {}".format(artist, track_name))


def add_tracks_to_spotify_playlist(uris):
    """Add all tracks from the selected Youtube playlists to a new Spotify playlist"""

    # create a new playlist
    playlist_id = create_playlist()

    # add all songs into new playlist
    request_data = json.dumps(uris)

    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )

    response_json = response.json()

    return response_json




spotify_track_uris = []
for choice in choices:
    chosen_playlist = playlists[choice]
    print("You selected the playlist '{}'".format(chosen_playlist.title))

    songs = youtube_client.get_music_videos_from_playlist(chosen_playlist.id)

    print("Attempting to add {} tracks from '{}'".format(len(songs), chosen_playlist.title))
    print(songs)
    print(tracks.artist, '|', tracks.track_name)

    for track in tracks:
        print(track.artist, '|', track.track_name)
        spotify_track_uri = spotify_client.search_spotify_tracks_uri(track.artist, track.track_name)
        if spotify_track_uri:
            # create a list of all uris
            spotify_track_uris.append(spotify_track_uri)

added_tracks = spotify_client.add_tracks_to_spotify_playlist(spotify_track_uri)
print(added_tracks)















# collect all of uri
uris = []
uris = [info["track_name"]
        for track, info in all_track_info.items()]
type(uris)

request_data2 = json.dumps(uris)
type(request_data2)
type(request_data)


for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter your choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")

    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(songs)}")

    for playlist in Playlist:
    print(Playlist.id, Playlist.title)

    for song in songs:
    print(song.artist, song.track)
    return songs

# taking multiple inputs at a time
# and type casting using list() function
x = list(map(int, input("Enter a multiple value: ").split()))
print("List of students: ", x)

for index, playlist in enumerate(playlists):
    print("{}: {}".format(index, playlist.title))
choices = list(map(int, input("Enter the indexes of the different playlists to select: ").split()))
print("List of playlists: {}".format(choices))
choices[0]
for choice in choices:
    chosen_playlist = playlists[choice]
    print("You selected the playlist '{}'".format(chosen_playlist.title))

    tracks = get_music_videos_from_playlist(chosen_playlist.id)
    print("Attempting to add {} tracks from '{}'".format(len(tracks), chosen_playlist.title))

for track in tracks:
    print("{} - {} ({})".format(track.artist, track.track_name, track.youtube_url))


# Client ID




"""Create A New Playlist"""
request_body = json.dumps({
    "name": "Testtest", #Tracks from Youtube Playlists
    "public": True,
    "collaborative": False

})

query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
response = requests.post(query, data=request_body, headers={"Content-Type": "application/json",
                                                            "Authorization": "Bearer {}".format(spotify_token)}
                         )
response_json = response.json()
print(response_json)

# playlist id
playlist_id = response_json["id"]

create_playlist()


def get_spotify_uri(artist, song_name):
    """Search For the Song"""
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
        song_name,
        artist
    )
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()
    songs = response_json["tracks"]["items"]

    # only use the first song
    uri = songs[0]["uri"]

    return uri


get_spotify_uri(tracks[0].artist, tracks[0].track_name)
search_song(tracks[0].artist, tracks[0].track_name)

get_spotify_uri(song_name, artist)

import urllib

def search_song(artist, track_name):
    query = urllib.parse.quote('{} {}'.format(artist,track_name))
    url = "https://api.spotify.com/v1/search?q={}&type=track".format(query)
    """Search For the Song"""
    # url =   "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
    #     track_name,
    #     artist
    # )
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )
    response_json = response.json()
    results = response_json['tracks']['items']

    if results:
        # let's assume the first track in the list is the song we want
        # return results[0]['id']
        return results[0]['uri']
    else:
        # raise Exception(f"No song found for {artist} = {track_name}")
        print(f"No song found for {artist} = {track_name}")


search_song(tracks[0].artist, tracks[0].track_name)

query = urllib.parse.quote('{} {}'.format(tracks[0].artist,tracks[0].track_name))
url = "https://api.spotify.com/v1/search?q={}&type=track".format(query)
"""Search For the Song"""
# url = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
#     tracks[0].track_name,
#     tracks[0].artist
# )
url
response = requests.get(
    url,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {spotify_token}"
    }
)
response_json = response.json()
results = response_json['tracks']['items']

# only use the first song
try:
    uri = results[0]["uri"]
    print(uri)
except:
    print(f"No song found for {tracks[0].artist} = {tracks[0].track_name}")

if results != :
    print(results[0]['id'])
else:
    raise Exception(f"No song found for {artist} = {track_name}")

import requests
# def add_song_to_playlist():
"""Add all liked songs into a new Spotify playlist"""
# populate dictionary with our liked songs
# self.get_liked_videos()

# collect all of uri
uris = [info["spotify_uri"]
        for song, info in tracks.items()]

# create a new playlist
playlist_id = self.create_playlist()

# add all songs into new playlist
request_data = json.dumps(uris)

query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
    playlist_id)

response = requests.post(
    query,
    data=request_data,
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(spotify_token)
    }
)

# check for valid response status
if response.status_code != 200:
    raise ResponseException(response.status_code)

response_json = response.json()
return response_json


def add_song_to_spotify(song_id):

    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

    response = requests.put(
        url,
        json={
            "ids": [song_id]
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )


response = requests.post(
    query,
    data=request_data,
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(spotify_token)
    }




for track in tracks:
    spotify_song_id = search_song(track.artist, track.track_name)
    if spotify_song_id:
        added_song = add_song_to_spotify(spotify_song_id)
        if added_song:
            print("Added {} - {} to the Spotify playlist".format(track.artist,track.track_name))
        else:
            print("{} - {} found but not Added to the Spotify playlist".format(track.artist,track.track_name))




def add_song_to_spotify(song_id):
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

    response = requests.put(
        url,
        json={
            "ids": [song_id]
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }

    )
    return response.ok

def add__to_playlist():
    """Add all liked songs into a new Spotify playlist"""


    # create a new playlist
    #playlist_id = self.create_playlist()

    # add all songs into new playlist
    request_data = json.dumps(uris)

    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)

    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )

    # check for valid response status
    if response.status_code != 200:
        raise ResponseException(response.status_code)

    response_json = response.json()
    return response_json



uris = []

for track in tracks:
    spotify_song_id = search_song(track.artist, track.track_name)

    if spotify_song_id:
        # collect all of uri
        uris.append(spotify_song_id)


        # add all songs into new playlist
        request_data = json.dumps(uris)
print(uris)
print(request_data)



url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

response = requests.post(
    query,
    data=request_data,
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(spotify_token)
    }

)

print(response.json())


    def add_song_to_spotify2(song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={
                "ids": [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {spotify_token}"
            }
        )

        return response.ok