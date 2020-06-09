import spotipy
import spotipy.util as util


class SpotifyClient(object):
    """Log into Spotify"""
    def __init__(self, spotify_user_id, spotify_scope, spotify_client_id, spotify_client_secret, spotify_redirect_url):
        print('\n Initialising Spotify Client...')
        spotify_token = util.prompt_for_user_token(spotify_user_id, spotify_scope,
                                                   client_id=spotify_client_id,
                                                   client_secret=spotify_client_secret,
                                                   redirect_uri=spotify_redirect_url)

        if spotify_token:
            spotify_client = spotipy.Spotify(auth=spotify_token)

            self.spotify_user_id = spotify_user_id
            self.spotify_token = spotify_token
            self.spotify_client = spotify_client

        else:
            print("Cannot get Spotify token")

    def create_playlist(self, spotify_playlist_name):
        """Create A New Spotify Playlist"""
        self.spotify_client.user_playlist_create(self.spotify_user_id, name=spotify_playlist_name)

        playlist_id = ''
        playlists = self.spotify_client.user_playlists(self.spotify_user_id)
        for playlist in playlists['items']:  # iterate through playlists I follow
            if playlist['name'] == spotify_playlist_name:  # filter for newly created playlist
                playlist_id = playlist['id']
                print("Spotify playlist '{}' (id: {}) created.".format(spotify_playlist_name, playlist_id))

        return playlist_id

    def search_spotify_tracks_uri(self, artist, track_name):
        """Search For the Track"""
        results = self.spotify_client.search(q=f"{track_name} {artist} ",
                                             limit=5, type='track')  # get 5 responses since first isn't always accurate

        if results['tracks']['total'] > 0:  # if track isn't on spotify as queried, go to next track
            uri = results['tracks']['items'][0]['uri']
            return uri
        else:
            print("No track found for {} - {}".format(artist, track_name))

    def add_tracks_to_spotify_playlist(self, spotify_playlist_name, uris):
        """Add Tracks To a Spotify Playlist"""

        # create a new playlist
        playlist_id = self.create_playlist(spotify_playlist_name)

        # add all tracks to the new playlist
        results = self.spotify_client.user_playlist_add_tracks(self.spotify_user_id, playlist_id, uris)

        return results
