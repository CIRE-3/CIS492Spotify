from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Define the required scopes
scope = "user-library-read playlist-modify-public playlist-modify-private"

# Set up Spotify OAuth with user login
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id="74d0eadfabc340e19f2741a78d83c98e",
    client_secret="21a175dc73f547579d0381d9181bdfc2",
    redirect_uri="http://localhost/",
    scope=scope
))

def get_liked_songs(sp):
    """
    Retrieve the logged-in user's liked songs.
    """
    liked_songs = []
    results = sp.current_user_saved_tracks()
    
    # Handle pagination to retrieve all liked songs
    while results:
        for item in results['items']:
            track = item['track']
            liked_songs.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'id': track['id']
            })
        # Get the next page of results if available
        results = sp.next(results) if results['next'] else None
    
    return liked_songs

def create_playlist(sp, user_id, playlist_name):
    """
    Create a new playlist on the user's profile.
    """
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description="Playlist created via API")
    print(f"Created playlist '{playlist_name}' with ID: {playlist['id']}")
    return playlist['id']

def add_songs_to_playlist(sp, playlist_id, song_ids):
    """
    Add songs to the specified playlist.
    """
    # Spotify API limits to 100 tracks at once, so chunk the list if necessary
    for i in range(0, len(song_ids), 100):
        sp.playlist_add_items(playlist_id, song_ids[i:i+100])
    print("Added songs to playlist.")

def main():
    """
    Main function to handle Spotify user login, retrieve liked songs, and create a playlist.
    """
    # Fetch the user's liked songs
    print("Fetching your liked songs...")
    liked_songs = get_liked_songs(sp)
    
    if not liked_songs:
        print("No liked songs found!")
        return

    # Display liked songs (optional)
    print(f"Found {len(liked_songs)} liked songs.")
    for song in liked_songs[:10]:  # Display only the first 10 songs
        print(f"{song['name']} by {song['artist']}")

    # Get the current user's ID
    user_id = sp.current_user()['id']

    # Create a new playlist
    playlist_name = "Liked Songs Playlist"
    playlist_id = create_playlist(sp, user_id, playlist_name)

    # Add liked songs to the new playlist
    song_ids = [song['id'] for song in liked_songs]
    add_songs_to_playlist(sp, playlist_id, song_ids)
    print(f"Playlist '{playlist_name}' created with {len(song_ids)} liked songs!")

# Run the main function
if __name__ == "__main__":
    main()

'''def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type":  "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

token = get_token()'''
