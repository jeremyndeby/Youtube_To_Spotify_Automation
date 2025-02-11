import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl

# Words to delete from the fetched title name from Youtube
IGNORE = ['(', '[', ' x', ')', ']', '&', 'lyrics', 'lyric',
          'video', 'official', '/', ' proximity', ' ft', '.', ' edit', ' feat', ' vs', ',']


class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class Track(object):
    def __init__(self, artist, track_name, youtube_url):
        self.artist = artist
        self.track_name = track_name
        self.youtube_url = youtube_url
        # self.spotify_uri = spotify_uri


class YouTubeClient(object):
    def __init__(self, credentials_location):
        """Log into Youtube"""
        print('\n Initialising Youtube Client...')
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOTE* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = credentials_location

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube_client

    def get_playlists(self):
        """"Get A List Of Your Youtube Playlists"""
        request = self.youtube_client.playlists().list(
            part="id, snippet",
            maxResults=100,  # maximum number of playlists
            mine=True
        )
        response = request.execute()

        # list of playlists
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

        return playlists

    def get_music_videos_from_playlist(self, playlist_id):
        """"Get The Artists and Track Names Of The Music Videos from A Youtube Playlists"""
        tracks = []
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id, snippet",
            maxResults=500  # maximum number of tracks per playlist
        )
        response = request.execute()

        # Collect each video and get important information
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']

            # Use youtube_dl to collect the track and artist name
            try:
                youtube_url = "https://www.youtube.com/watch?v={}".format(video_id)
                video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(youtube_url, download=False)

                # Save information
                full_title = video['title']
                artist = video['artist']
                track_name = video['track']
            except:
                continue

            # If no artist or track name use the title of the track
            if artist is None and track_name is None and full_title:
                try:
                    artist = (full_title.rsplit('-')[0]).strip()
                    track_name = (full_title.rsplit('-')[1]).strip()
                except:
                    continue

            if artist and track_name:
                # Clean the information
                artist = artist.lower()
                for ch in IGNORE:
                    if ch in artist:
                        artist = artist.replace(ch, '')

                track_name = track_name.lower()
                for ch in IGNORE:
                    if ch in track_name:
                        track_name = track_name.replace(ch, '')

                # Save the information
                tracks.append(Track(artist, track_name, youtube_url))

        return tracks
