import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import ttk, messagebox

# Load environment variables
load_dotenv()

# Spotify API Configuration
scope = "user-library-read, playlist-modify-public, playlist-modify-private, playlist-read-private"
spotifyClient = None  # Global variable for Spotify client


def loginToSpotify():
    """Log in to Spotify and enable mood selection."""
    global spotifyClient
    try:
        # Authenticate Spotify
        spotifyClient = Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=scope
        ))
        messagebox.showinfo("Login Successful", "You are now logged in to Spotify!")
        loginFrame.pack_forget()  # Hide login frame
        moodFrame.pack(pady=20)  # Show mood selection frame
    except Exception as e:
        messagebox.showerror("Login Error", f"Failed to log in to Spotify: {e}")
        
        
def getLikedSongs():
    """Fetch the user's liked songs."""
    likedSongs = []
    try:
        results = spotifyClient.current_user_saved_tracks()
        while results:
            for item in results['items']:
                track = item['track']
                likedSongs.append({
                    'name': track['name'],
                    'id': track['id'],
                    'artist': track['artists'][0]['name']
                })
            results = spotifyClient.next(results) if results['next'] else None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch liked songs: {e}")
    return likedSongs

moodCriteria = {
    "Happy": {"min_valence": 0.7, "min_energy": 0.6},
    "Sad": {"max_valence": 0.4, "max_energy": 0.5},
    "Angry": {"min_energy": 0.8},
    "Inspired": {"min_valence": 0.6, "min_energy": 0.5},
    "Relaxed": {"max_tempo": 100, "max_energy": 0.5}
}
def filterSongsByMood(likedSongs, mood):
    """Filter songs based on mood criteria."""
    criteria = moodCriteria.get(mood, {})
    filteredSongs = []
    
    for song in likedSongs:
        audioFeatures = spotifyClient.audio_features([song['id']])[0]
        
        if not audioFeatures:
            continue  # Skip if no audio features are available
        
        match = True
        if "min_valence" in criteria and audioFeatures["valence"] < criteria["min_valence"]:
            match = False
        if "max_valence" in criteria and audioFeatures["valence"] > criteria["max_valence"]:
            match = False
        if "min_energy" in criteria and audioFeatures["energy"] < criteria["min_energy"]:
            match = False
        if "max_energy" in criteria and audioFeatures["energy"] > criteria["max_energy"]:
            match = False
        if "max_tempo" in criteria and audioFeatures["tempo"] > criteria["max_tempo"]:
            match = False

        if match:
            filteredSongs.append(song)
    
    return filteredSongs



def generatePlaylist():
    """Generate a playlist after login and mood selection."""
    if not spotifyClient:
        messagebox.showerror("Error", "You must log in to Spotify first!")
        return

    selectedMood = moodVar.get()
    if not selectedMood:
        messagebox.showwarning("No Mood Selected", "Please select a mood first.")
        return

    try:
        # Generate playlist
        userId = spotifyClient.me()["id"]
        playlist = spotifyClient.user_playlist_create(userId, f"{selectedMood} Mood Playlist", public=False)
        playlistId = playlist["id"]

        # Fetch and filter liked songs
        likedSongs = getLikedSongs()
        filteredSongs = filterSongsByMood(likedSongs, selectedMood)

        # Add filtered songs to the playlist
        trackIds = [song['id'] for song in filteredSongs]
        if trackIds:
            spotifyClient.user_playlist_add_tracks(userId, playlistId, trackIds)
            messagebox.showinfo("Playlist Generated", f"{selectedMood} playlist created with {len(trackIds)} songs!")
        else:
            messagebox.showwarning("No Songs Found", "No songs matched the mood criteria.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate playlist: {e}")







# Tkinter GUI
root = tk.Tk()
root.title("Spotify Playlist Mood Generator")
root.geometry("400x500")
root.configure(bg="#121212")

# Login Frame
loginFrame = tk.Frame(root, bg="#121212")
loginFrame.pack(pady=50)

tk.Label(loginFrame, text="Sign In to Spotify", font=("Circular", 20, "bold"), fg="white", bg="#121212").pack(pady=10)

tk.Button(loginFrame, text="Login with Spotify", font=("Circular", 12, "bold"),
          command=loginToSpotify, bg="white", fg="black", width=20).pack(pady=20)

# Mood Selection Frame
moodFrame = tk.Frame(root, bg="#121212")

tk.Label(moodFrame, text="Select Your Mood", font=("Arial", 18, "bold"), fg="white", bg="#121212").pack(pady=10)

moods = ["Happy", "Sad", "Angry", "Inspired", "Relaxed"]
moodVar = tk.StringVar()
moodCombobox = ttk.Combobox(moodFrame, values=moods, textvariable=moodVar, state="readonly", font=("Arial", 12))
moodCombobox.pack(pady=10)

tk.Button(moodFrame, text="Generate Playlist", font=("Circular", 12, "bold"),
          command=generatePlaylist, bg="white", fg="black", width=20).pack(pady=20)

root.mainloop()
