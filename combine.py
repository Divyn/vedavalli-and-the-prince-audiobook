import os
import subprocess

def combine_mp3_files(folder="output", output_filename="audiobook_combined.mp3", prefix="audiobook_part"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, folder)
    
    # Find and sort MP3 files
    mp3_files = [
        f for f in os.listdir(output_dir)
        if f.endswith(".mp3") and f.startswith(prefix)
    ]
    mp3_files.sort()

    if not mp3_files:
        print("❗ No MP3 files found to combine.")
        return

    # Create a file list for ffmpeg, requires a text file that lists all the file paths in the correct format.
    list_file_path = os.path.join(output_dir, "file_list.txt")
    with open(list_file_path, "w") as f:
        for filename in mp3_files:
            filepath = os.path.join(output_dir, filename)
            f.write(f"file '{filepath}'\n")

    # Output combined file
    output_path = os.path.join(output_dir, output_filename)

    # Run ffmpeg to combine
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_file_path, "-c", "copy", output_path
    ])

    os.remove(list_file_path)
    print(f"✅ Combined audiobook saved as: {output_path}")

if __name__ == "__main__":
    combine_mp3_files()
