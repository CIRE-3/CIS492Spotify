import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import ttk, messagebox

# Load environment variables
load_dotenv()

# Spotify API Configuration
scope = "user-library-read playlist-modify-public playlist-modify-private"
spotifyClient = None  # Global variable for Spotify client


def loginToSpotify():
    """Log in to Spotify and enable mood selection."""
    global spotifyClient
    try:
        # Authenticate Spotify
        spotifyClient = Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=scope
        ))
        messagebox.showinfo("Login Successful", "You are now logged in to Spotify!")
        loginFrame.pack_forget()  # Hide login frame
        moodFrame.pack(pady=20)  # Show mood selection frame
    except Exception as e:
        messagebox.showerror("Login Error", f"Failed to log in to Spotify: {e}")


def detectMood(audio_features):
    """
    Detect the mood of a song based on its audio features.
    """
    valence = audio_features["valence"]
    energy = audio_features["energy"]

    # Determine mood based on valence and energy
    if valence > 0.5:
        if energy > 0.5:
            return "Happy"
        else:
            return "Relaxed"
    else:
        if energy > 0.5:
            return "Angry"
        else:
            return "Sad"


def filterLikedSongsByMood(mood):
    """
    Filter liked songs based on the detected mood.
    """
    if not spotifyClient:
        messagebox.showerror("Error", "Spotify client is not authenticated.")
        return []

    likedSongs = getLikedSongs()
    filteredSongs = []

    try:
        for song in likedSongs:
            # Skip songs without valid IDs
            if not song["id"]:
                continue

            # Get audio features for the song
            audio_features = spotifyClient.audio_features(song["id"])
            if audio_features and audio_features[0]:  # Ensure the response is not empty
                detectedMood = detectMood(audio_features[0])
                if detectedMood == mood:
                    filteredSongs.append(song)
            else:
                print(f"Skipping song with invalid audio features: {song['name']}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze song mood: {e}")

    return filteredSongs


def getLikedSongs():
    """
    Fetch the user's liked songs.
    """
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


def generatePlaylist():
    """
    Generate a playlist after login and mood selection.
    """
    if not spotifyClient:
        messagebox.showerror("Error", "You must log in to Spotify first!")
        return

    selectedMood = moodVar.get()
    if not selectedMood:
        messagebox.showwarning("No Mood Selected", "Please select a mood first.")
        return

    try:
        # Filter liked songs by the selected mood
        filteredSongs = filterLikedSongsByMood(selectedMood)

        if not filteredSongs:
            messagebox.showwarning("No Songs Found", f"No liked songs match the {selectedMood} mood.")
            return

        # Create a new playlist for the selected mood
        userId = spotifyClient.me()["id"]
        playlist = spotifyClient.user_playlist_create(userId, f"{selectedMood} Mood Playlist", public=False)
        playlistId = playlist["id"]

        # Add filtered songs to the playlist
        trackIds = [song["id"] for song in filteredSongs[:50]]  # Add up to 50 songs
        spotifyClient.user_playlist_add_tracks(userId, playlistId, trackIds)

        messagebox.showinfo("Playlist Generated", f"{selectedMood} playlist created with {len(trackIds)} songs!")
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

moods = ["Happy", "Sad", "Angry", "Relaxed"]
moodVar = tk.StringVar()
moodCombobox = ttk.Combobox(moodFrame, values=moods, textvariable=moodVar, state="readonly", font=("Arial", 12))
moodCombobox.pack(pady=10)

tk.Button(moodFrame, text="Generate Playlist", font=("Circular", 12, "bold"),
          command=generatePlaylist, bg="white", fg="black", width=20).pack(pady=20)

root.mainloop()
