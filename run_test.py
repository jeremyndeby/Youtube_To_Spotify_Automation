# 1. Log into Youtube
# 2. Get the music Videos from the selected Playlists
# 3. Log into Spotify
# 4. Create a (new) Youtube playlist in Spotify
# 5. Search for the song in Spotify
# 6. Add the song to the playlist


import json
import requests
from youtube_client_secret import youtube_data_api_key, youtube_analytics_api_key
from spotify_client_secret import spotify_user_id, spotify_token

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


class CreatePlaylist:

    def __init__(self):
        self.spotify_user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_track_info = {}

    def get_youtube_client(self):
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
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_music_videos(self):
        """Get the music Videos from the selected Playlists & create a dictionary of important track information"""
        requests = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

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

        all_track_info

    def get_spotify_client(self):
        '''Log into Spotify'''
        pass

    def create_playlist(self):
        '''Create a (new) Youtube playlist in Spotify'''
        request_body = json.dumps({
            "name": "Tracks from Youtube Playlists",
            "public": True,
            "collaborative": False
        })

        query = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }

        )
        response_json = response.json()

        # return the playlist id
        return response_json["id"]

    def get_spotify_url(self, track_name, artist):
        """Search for the song in Spotify"""
        query = 'https://api.spotify.com/v1/search?q=track%3A{}+artist%3A{}&type=track&offset=0&limit=20'.format(
            track_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        tracks = response_json["tracks"]["items"]

        # only use the first song
        url = tracks[0]["uri"]
        return url

    def add_song_to_playlist(self):
        """Add the song to the playlist"""
        # Populate our tracks dictionary
        self.get_music_videos()

        # Collect all of uri
        uris = []
        for track, info in self.all_track_info.items():
            uri.append(info["spotify_uri"])

        # Create a new playlist
        playlist_id = self.create_playlist()

        # Add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        return response_json

