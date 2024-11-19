import tkinter as tk
from tkinter import ttk, messagebox

def handleLogin():
    username = entryUsername.get()
    password = entryPassword.get()
    if username and password:
        messagebox.showinfo("Success", f"Welcome, {username}!")
        loginFrame.pack_forget() 
        moodFrame.pack(pady=20) 
    else:
        messagebox.showerror("Error", "Please enter both username and password.")

def generatePlaylist():
    selectedMood = moodVar.get()
    if selectedMood:
        messagebox.showinfo("Playlist Generated", f"Generating a {selectedMood} playlist!")
    else:
        messagebox.showwarning("No Mood Selected", "Please select a mood first.")

root = tk.Tk()
root.title("Spotify Playlist Mood Generator")
root.geometry("400x500")
root.configure(bg="#121212") 

# Login Frame
loginFrame = tk.Frame(root, bg="#121212")
loginFrame.pack(pady=50)

tk.Label(loginFrame, text="Sign In", font=("Circular", 20, "bold"), fg="white", bg="#121212").pack(pady=10)

tk.Label(loginFrame, text="Username", font=("Arial", 12), fg="white", bg="#121212").pack()
entryUsername = tk.Entry(loginFrame, font=("Arial", 12), width=30)
entryUsername.pack(pady=5)

tk.Label(loginFrame, text="Password", font=("Arial", 12), fg="white", bg="#121212").pack()
entryPassword = tk.Entry(loginFrame, font=("Arial", 12), width=30, show="*")
entryPassword.pack(pady=5)

tk.Button(loginFrame, text="Login", font=("Circular", 12, "bold"), command=handleLogin, bg="white", fg="black", width=20).pack(pady=20)

# Mood Selection Frame
moodFrame = tk.Frame(root, bg="#121212")

tk.Label(moodFrame, text="Select Your Mood", font=("Arial", 18, "bold"), fg="white", bg="#121212").pack(pady=10)

moods = ["Happy", "Sad", "Angry", "Inspired", "Relaxed"]
moodVar = tk.StringVar()
moodCombobox = ttk.Combobox(moodFrame, values=moods, textvariable=moodVar, state="readonly", font=("Arial", 12))
moodCombobox.pack(pady=10)

tk.Button(moodFrame, text="Generate Playlist", font=("Circular", 12, "bold"), command=generatePlaylist, bg="white", fg="black", width=20).pack(pady=20)

root.mainloop()
