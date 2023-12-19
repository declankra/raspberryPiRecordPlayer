

## Request user authorization
CLIENT_ID = 'SPOTIFY_CLIENT_ID'
SCOPE = 'SPOTIFY_SCOPE'  
REDIRECT_URI = 'http://localhost:8888/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'

def get_auth_url():
    return f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"