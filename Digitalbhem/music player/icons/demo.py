import os
import cv2
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import random

def add_music():
    global music_folder
    music_folder = filedialog.askdirectory(title="Select Music Folder")
    songs = [os.path.join(music_folder, song) for song in os.listdir(music_folder) if song.endswith(".mpeg")]
    for i, song_path in enumerate(songs, start=1):
        os.rename(song_path, os.path.join(music_folder, f"Song{i}.mpeg"))  # Rename the song files
        playlist.insert(END, f"Song{i}")  # Add renamed song names to the playlist

def play_music():
    global current_song, music_folder
    selected_index = playlist.curselection()
    if selected_index and music_folder:
        selected_music = playlist.get(selected_index)
        if current_song != selected_music:  # Only change animation if the song is changed
            current_song = selected_music
            toggle_animation()

        mixer.music.load(os.path.join(music_folder, f"{selected_music}.mpeg"))
        mixer.music.play()

def stop_music():
    mixer.music.stop()

def volume_up():
    current_volume = mixer.music.get_volume()
    if current_volume < 1:
        mixer.music.set_volume(current_volume + 0.1)

def volume_down():
    current_volume = mixer.music.get_volume()
    if current_volume > 0:
        mixer.music.set_volume(current_volume - 0.1)

def loop_music():
    pass  # Add loop functionality here

def pause_music():
    global is_paused
    if is_paused:
        mixer.music.unpause()
    else:
        mixer.music.pause()
    is_paused = not is_paused

def toggle_animation():
    global current_animation_index
    current_animation_index = (current_animation_index + 1) % len(animation_paths)
    display_animation(animation_paths[current_animation_index])

root = Tk()
root.title("Apna Music")
root.geometry("485x700+290+10")
root.configure(background='#333333')
root.resizable(False, False)
mixer.init()

# Function to load and display animations
def display_animation(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    label = Label(root)
    label.place(x=0, y=0)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (485, 400))
            frame_photo = PhotoImage(data=cv2.imencode('.png', frame_resized)[1].tobytes())
            label.configure(image=frame_photo)
            label.image = frame_photo
            root.after(random.randint(20, 200), update_frame)  # Randomize animation update interval
        else:
            cap.release()

    update_frame()

# Get the absolute path of the current script and navigate to the icons folder
script_folder = os.path.dirname(os.path.abspath(__file__))

# Load and display animations alternately
animation_folder = os.path.join(script_folder, "..", "animations")
animation_files = [file for file in os.listdir(animation_folder) if file.endswith(('.mp4', '.avi', '.mov'))]
animation_paths = [os.path.join(animation_folder, file) for file in animation_files]
current_animation_index = 0

# Displaying the first animation at the start
display_animation(animation_paths[current_animation_index])

Button(root, text="Browse Music", command=add_music, bg='#ffffff').place(x=0, y=400, width=485, height=30)
playlist = Listbox(root, width=100, font=("Times New Roman", 10), bg="#333333", fg="grey", selectbackground="lightblue", cursor="hand2", bd=0)
playlist.place(x=0, y=430, width=485, height=200)

scroll = Scrollbar(root, command=playlist.yview)
scroll.place(x=465, y=430, height=200)

# Load images using relative paths
icon_folder = os.path.join(script_folder, "..", "icons")
start_img = PhotoImage(file=os.path.join(icon_folder, "play.png")).subsample(3, 3)
stop_img = PhotoImage(file=os.path.join(icon_folder, "stop.png")).subsample(3, 3)
pause_img = PhotoImage(file=os.path.join(icon_folder, "pause.png")).subsample(3, 3)
loop_img = PhotoImage(file=os.path.join(icon_folder, "loop.png")).subsample(3, 3)

Button(root, image=start_img, command=play_music, bg='#ffffff').place(x=100, y=650, width=50, height=30)
Button(root, image=stop_img, command=stop_music, bg='#ffffff').place(x=170, y=650, width=50, height=30)
Button(root, image=pause_img, command=pause_music, bg='#ffffff').place(x=240, y=650, width=50, height=30)
Button(root, image=loop_img, command=loop_music, bg='#ffffff').place(x=310, y=650, width=50, height=30)

Button(root, text="Volume Up", command=volume_up, bg='#ffffff').place(x=20, y=650, width=80, height=30)
Button(root, text="Volume Down", command=volume_down, bg='#ffffff').place(x=380, y=650, width=90, height=30)

is_paused = False  # Variable to track if music is paused
current_song = None  # Variable to store the current song
music_folder = None  # Variable to store the selected music folder

root.mainloop()
