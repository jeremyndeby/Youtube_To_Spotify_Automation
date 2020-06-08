import os
from youtube_client import YouTubeClient
from spotify_client import SpotifyClient
# from spotify_client_secret_token import spotify_token,spotify_user_id

spotify_token = "BQAbohdeebmQFuZWRg-1PMUfnBI4gR-4hI_VFOPw9omegCyMPcbAASwXhDmnHuPqpVPikBK-Idi41iXKb_hS4v-pIJU-WqAlgwcTmC1TPKVbmnOfHALa32kO-R2UA4nAdL69R7DFFUElOX1k3uDQVTiczKWjV2Wy_lFMzx4IEQJooRkkeJJ_3qBRcbQ7PNRugu2ltl9rDL21X1s"
spotify_user_id = '1114332950'

# from spotify_client import SpotifyClient

def run():

    # 1. Get a list of our Youtube playlists
    youtube_client = YouTubeClient('client_secret_desktop.json')
    spotify_client = SpotifyClient(spotify_token, spotify_user_id)
    playlists = youtube_client.get_playlists()

    for index, playlist in enumerate(playlists):
        print("{}: {}".format(index, playlist.title))

    # 2. Select the Youtube playlists we want the music videos from
    choices = list(map(int, input("Enter the indexes of the different playlists to select: ").split())) # separated by a space
    print("List of Youtube playlists indexes entered: {}".format(choices))

    # 3. Define the name of the Spotify playlist to create
    spotify_playlist_name = input("Define the name of the Spotify playlist to create: ") # Tracks from Youtube Playlists
    print("You created a new Spotify playlist named '{}'".format(spotify_playlist_name))

    # 4. For each video in each playlist selected, get the track information from Youtube
    # and search the track in spotify thanks to its uri
    spotify_track_uris = []
    for choice in choices:
        chosen_playlist = playlists[choice]
        print("You selected the playlist '{}'".format(chosen_playlist.title))
        songs = youtube_client.get_music_videos_from_playlist(chosen_playlist.id)

        print("Attempting to add {} tracks from '{}'".format(len(songs), chosen_playlist.title))

        for song in songs:
            spotify_track_uri = spotify_client.search_spotify_tracks_uri(song.artist, song.track_name)
            if spotify_track_uri:
                # create a list of all uris
                spotify_track_uris.append(spotify_track_uri)

    # 5. If we found the track, add it to to the new Spotify playlist
    added_tracks = spotify_client.add_tracks_to_spotify_playlist(spotify_playlist_name, spotify_track_uris)
    if added_tracks:
        print("Tracks added successfully to your new Spotify playlist '{}'!".format(spotify_playlist_name))


if __name__ == '__main__':
    run()