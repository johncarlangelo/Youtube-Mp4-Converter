# import yt_dlp
# import os

# def download_youtube_video_as_mp4(youtube_url, output_path=r"C:\Users\johnc\Downloads"):
#     try:
#         # Ensure the output path exists
#         if not os.path.exists(output_path):
#             os.makedirs(output_path)

#         # yt-dlp options for downloading video and audio
#         ydl_opts = {
#             'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Download best MP4 video + best audio
#             'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Output file name and path
#             'merge_output_format': 'mp4'  # Ensure the output format is MP4
#         }

#         # Download the video and audio
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([youtube_url])

#         print(f"Download complete! Video with audio saved in {output_path}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage
# youtube_url = input("Enter the YouTube URL: ")
# download_youtube_video_as_mp4(youtube_url)

import yt_dlp
import os
import customtkinter as ctk
import threading
from tkinter import ttk

def download_youtube_video_as_mp4(youtube_url):
    try:
        # Set the output path to the user's Downloads folder
        output_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # Ensure the output path exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Define a progress hook to update the progress bar
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes'] > 0:
                    progress_bar['value'] = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    progress_label.configure(text=f"Downloading: {d['filename']}, {d['downloaded_bytes']}/{d['total_bytes']} bytes")
                else:
                    progress_label.configure(text=f"Downloading: {d['filename']}, {d['downloaded_bytes']} bytes")
            elif d['status'] == 'finished':
                progress_bar.stop()
                progress_label.configure(text="Download complete!")

        # yt-dlp options for downloading video and audio
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Download best MP4 video + best audio
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Output file name and path
            'merge_output_format': 'mp4',  # Ensure the output format is MP4
            'progress_hooks': [progress_hook]  # Add the progress hook
        }

        # Download the video and audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

    except Exception as e:
        result_label.configure(text=f"An error occurred: {e}")
        progress_bar.stop()

def start_download_thread():
    progress_bar.start()  # Start the progress bar animation
    result_label.configure(text="Downloading Started...")
    app.after(500, lambda: threading.Thread(target=download_and_update_label, args=(url_entry.get(),)).start())

def download_and_update_label(youtube_url):
    result_label.configure(text="")  # Clear the label text before starting the download
    download_youtube_video_as_mp4(youtube_url)

# Set up the main application window
ctk.set_appearance_mode("dark")  # Change appearance mode to dark
ctk.set_default_color_theme("blue")  # Set color theme

app = ctk.CTk()
app.title("YouTube Video Downloader")
app.geometry("650x400")  # Adjust the initial window size here

# Set minimum and maximum size (optional)
app.minsize(400, 250)  # Minimum size
app.maxsize(1000, 600)  # Maximum size

# URL entry
url_label = ctk.CTkLabel(app, text="YouTube URL:")
url_label.pack(pady=10)
url_entry = ctk.CTkEntry(app, width=400)  # Adjust entry width
url_entry.pack(pady=5)

# Progress bar
progress_bar = ttk.Progressbar(app, length=400, mode='determinate')  # Adjust length
progress_bar.pack(pady=20)

# Progress label
progress_label = ctk.CTkLabel(app, text="")
progress_label.pack(pady=5)

# Download button
download_button = ctk.CTkButton(app, text="Download", command=start_download_thread)
download_button.pack(pady=10)

# Result label
result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=5)

app.mainloop()