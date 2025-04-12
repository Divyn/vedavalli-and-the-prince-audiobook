import os
import subprocess
from docx import Document

# 1. Convert AIFF to MP3
def convert_to_mp3(aiff_file, mp3_file):
    subprocess.run(["ffmpeg", "-y", "-i", aiff_file, mp3_file])

# 2. Read DOCX
def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())
    return '\n'.join(full_text)

# 3. Split Text with Natural Breaks
def split_text(text, max_length=3000):
    paragraphs = text.split('\n')
    chunks, current_chunk = [], ""

    for para in paragraphs:
        if para.strip():
            para += " "
            # Add artificial pause (period + double newline)
            para = para.strip() + ".\n\n"
        if len(current_chunk) + len(para) < max_length:
            current_chunk += para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# 4. Convert to Speech with Better Voice Handling
def save_with_say(text_chunks, output_folder="output", output_prefix="audiobook_part", voice="Moira"):
    os.makedirs(output_folder, exist_ok=True)

    for idx, chunk in enumerate(text_chunks):
        aiff_path = os.path.join(output_folder, f"{output_prefix}{idx+1}.aiff")
        mp3_path = os.path.join(output_folder, f"{output_prefix}{idx+1}.mp3")
        temp_txt_path = os.path.join(output_folder, "temp.txt")

        # Save chunk to temp file for better punctuation handling
        with open(temp_txt_path, "w") as f:
            f.write(chunk)

        # Use 'say' to read from file
        subprocess.run(["say", "-v", voice, "-o", aiff_path, "-f", temp_txt_path])

        # Convert to MP3
        convert_to_mp3(aiff_path, mp3_path)
        print(f"🗣️ Saved part {idx+1} as {mp3_path}")

        # Cleanup
        os.remove(aiff_path)
        os.remove(temp_txt_path)

# 5. Main Flow
if __name__ == "__main__":
    docx_path = "novel.docx"  # Replace with your actual file
    print("📖 Reading the document...")
    full_text = read_docx(docx_path)

    print("✂️ Splitting text into chunks with natural pauses...")
    chunks = split_text(full_text, max_length=3000)

    print("🎙️ Converting text to speech using macOS 'say'...")
    save_with_say(chunks)

    print("✅ Audiobook conversion complete using macOS TTS!")
