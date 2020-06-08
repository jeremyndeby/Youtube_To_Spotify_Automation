import json
import requests
import urllib.parse

class SpotifyClient(object):
    def __init__(self, spotify_token, spotify_user_id):
        self.spotify_token = spotify_token
        self.spotify_user_id = spotify_user_id

    def create_playlist(self, spotify_playlist_name):
        """Create A New Playlist"""


        request_body = json.dumps({
            "name": spotify_playlist_name,  # Tracks from Youtube Playlists
            "public": True,
            "collaborative": False
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_user_id)
        response = requests.post(query, data=request_body, headers={"Content-Type": "application/json",
                                                                    "Authorization": "Bearer {}".format(self.spotify_token)}
                                 )

        response_json = response.json()
        print(response_json)

        # playlist id
        playlist_id = response_json["id"]

        return playlist_id

    def search_spotify_tracks_uri(self, artist, track_name):
        """Search For the Song"""
        query = urllib.parse.quote('{} {}'.format(artist, track_name))
        url = "https://api.spotify.com/v1/search?q={}&type=track".format(query)

        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}"
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


    def add_tracks_to_spotify_playlist(self, spotify_playlist_name, uris):
        """Add all tracks from the selected Youtube playlists to a new Spotify playlist"""

        # create a new playlist
        playlist_id = self.create_playlist(spotify_playlist_name)

        # add all songs into new playlist
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