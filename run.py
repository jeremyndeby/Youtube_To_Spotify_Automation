from credentials import spotify_user_id
from credentials import spotify_client_id
from credentials import spotify_client_secret
from credentials import spotify_scope
from credentials import spotify_redirect_url

from youtube_client import YouTubeClient
from spotify_client import SpotifyClient


def run():
    # 0. Initialisation of Youtube and Spotify clients
    youtube_client = YouTubeClient('client_secret_desktop.json')
    # spotify_client = SpotifyClient(spotify_token, spotify_user_id)
    spotify_client = SpotifyClient(spotify_user_id, spotify_scope, spotify_client_id, spotify_client_secret,
                                   spotify_redirect_url)

    # 1. Get a list of our Youtube playlists
    playlists = youtube_client.get_playlists()
    for index, playlist in enumerate(playlists):
        print("{}: {}".format(index, playlist.title))

    # 2. Select the Youtube playlists we want the music videos from
    choices = list(
        map(int, input("Enter the indexes of the different playlists to select: ").split()))  # separated by a space
    print("List of Youtube playlists indexes entered: {}".format(choices))

    # 3. Define the name of the Spotify playlist to create
    spotify_playlist_name = input(
        "Define the name of the Spotify playlist to create: ")  # Tracks from Youtube Playlists

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
