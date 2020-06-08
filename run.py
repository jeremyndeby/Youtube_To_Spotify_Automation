import os
from youtube_client import YouTubeClient
from spotify_client import SpotifyClient
# from spotify_client_secret_token import spotify_token,spotify_user_id

spotify_token = "BQD4XQHNoWMGfwrVyoKWc8a_EHxK_R9bD9c9TwaeKG4Ukr37qUklN5ag5yTVtx-WMaAZIGiZhskVpaRlTh45pX0scAIc66mXtMLRVeQdP9nEnj1NloMTaKUCi9Rqq7PKKh7M3IUlye_-4iiiK-04h6RAhhqyEtQeBBpcYI2osm8hR_FxPfMxEll8obf8mTDvcvaYqCAcauUsISs"
spotify_user_id = '1114332950'

# from spotify_client import SpotifyClient

def run():

    # 1. Get a list of our Youtube playlists
    youtube_client = YouTubeClient('client_secret_desktop.json')
    spotify_client = SpotifyClient(spotify_token, spotify_user_id)
    playlists = youtube_client.get_playlists()

    for index, playlist in enumerate(playlists):
        print("{}: {}".format(index, playlist.title))
    choices = list(map(int, input("Enter the indexes of the different playlists to select: ").split())) # separated by a space
    print("List of playlists: {}".format(choices))

    spotify_playlist_name = input("Define the name of the Spotify playlist to create: ") # Tracks from Youtube Playlists

    spotify_track_uris = []
    for choice in choices:
        chosen_playlist = playlists[choice]
        print("You selected the playlist '{}'".format(chosen_playlist.title))

        songs = youtube_client.get_music_videos_from_playlist(chosen_playlist.id)

        print("Attempting to add {} tracks from '{}'".format(len(songs), chosen_playlist.title))

        for song in songs:
            print(song.artist, '|', song.track_name)
            spotify_track_uri = spotify_client.search_spotify_tracks_uri(song.artist, song.track_name)
            if spotify_track_uri:
                # create a list of all uris
                spotify_track_uris.append(spotify_track_uri)

    added_tracks = spotify_client.add_tracks_to_spotify_playlist(spotify_playlist_name, spotify_track_uris)
    print(added_tracks)


if __name__ == '__main__':
    run()