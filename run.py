import os
from youtube_client import YouTubeClient
from spotify_client import SpotifyClient
# from spotify_client_secret_token import spotify_token,spotify_user_id

spotify_token = 'BQA635_c7mSq5FlS8NW8EmQBzeyxJYazhFfDSP8OgFBlryZ4fRAcFJ5fRTAKCSmO6LHrnj7QHP5yTSB4Tw2HOLtn4GpsmbAiaEDZfUhEqTM3ScZe1FgamRY6R6i6uhlT4iox0KzQudMaF'

spotify_user_id = '1114332950'

# from spotify_client import SpotifyClient

def run():

    # 1. Get a list of our Youtube playlists
    youtube_client = YouTubeClient('client_secret_desktop.json')
    spotify_client = SpotifyClient(spotify_token, spotify_user_id)
    playlists = youtube_client.get_playlists()

    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter your choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")

    songs = youtube_client.get_music_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(songs)}")
    print(songs)

    # for index, playlist in enumerate(playlists):
    #     print("{}: {}".format(index, playlist.title))
    # choices = list(map(int, input("Enter the indexes of the different playlists to select: ").split())) # separated by a space
    # print("List of playlists: {}".format(choices))
    #
    # spotify_track_uris = []
    # for choice in choices:
    #     chosen_playlist = playlists[choice]
    #     print("You selected the playlist '{}'".format(chosen_playlist.title))
    #
    #     songs = youtube_client.get_music_videos_from_playlist(chosen_playlist.id)
    #
    #     print("Attempting to add {} tracks from '{}'".format(len(songs), chosen_playlist.title))
    #     print(songs)
        # print(tracks.artist, '|', tracks.track_name)

        # for track in tracks:
        #     print(track.artist, '|', track.track_name)
    #         spotify_track_uri = spotify_client.search_spotify_tracks_uri(track.artist, track.track_name)
    #         if spotify_track_uri:
    #             # create a list of all uris
    #             spotify_track_uris.append(spotify_track_uri)
    #
    # added_tracks = spotify_client.add_tracks_to_spotify_playlist(spotify_track_uri)
    # print(added_tracks)


if __name__ == '__main__':
    run()