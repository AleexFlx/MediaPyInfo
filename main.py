import tkinter as tk
from tkinter import filedialog, messagebox
from pymediainfo import MediaInfo
import os

def format_bitrate(bitrate_bps):
    try:
        bitrate_bps = int(bitrate_bps)
        if bitrate_bps >= 10_000_000:
            return f"{bitrate_bps / 1_000_000:.2f}"
        else:
            return f"{bitrate_bps / 1_000:.0f}"
    except (ValueError, TypeError):
        return "Unknown"

def format_fps(frame_rate):
    try:
        return f"{float(frame_rate):.2f} FPS"
    except (ValueError, TypeError):
        return "Unknown"

def get_media_info(file_path):
    try:
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "Video":
                resolution = f"{track.width}x{track.height}" if track.width and track.height else "Unknown"
                bitrate = format_bitrate(track.bit_rate)
                fps = format_fps(track.frame_rate)
                return f"{os.path.basename(file_path)}\n{resolution}\n{bitrate}\n{fps}\n"
        return f"{os.path.basename(file_path)}\nUnknown\nUnknown\nUnknown\n"
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}\n"

def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select AVI or M2V files",
        filetypes=[("AVI files", "*.avi"), ("M2V files", "*.m2v")]
    )
    return file_paths

def save_to_file(info):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Save Media Info"
    )
    if save_path:
        with open(save_path, 'w') as file:
            file.write(info)
        messagebox.showinfo("Success", f"Media info saved to {save_path}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    files = select_files()
    if not files:
        messagebox.showwarning("No Files Selected", "No files were selected.")
        return

    info = "File name / Resolution / Bitrate / FPS\n"
    for file in files:
        info += get_media_info(file) + "\n"

    save_to_file(info)

if __name__ == "__main__":
    main()
