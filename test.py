import spotipy
import spotipy.util as util

spotify_user_id = '1114332950'
spotify_client_id = "68fd722d2269433e8ace7bb187c49492"
spotify_client_secret = "f5af369c6d084ebc9ec066be6c9157d7"



#Initiate Spotipy
scope = 'playlist-modify-public'
username = '1114332950'
client_id = '68fd722d2269433e8ace7bb187c49492'
client_secret = 'f5af369c6d084ebc9ec066be6c9157d7'
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri='https://github.com/jeremyndeby') #Follow Directions in Console
sp = spotipy.Spotify(auth=token)
sp

