import pyttsx3
from docx import Document
import os

# 1. Load the Word document
def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():  # Ignore empty lines
            full_text.append(para.text.strip())
    return '\n'.join(full_text)

# 2. Split the text into smaller chunks
def split_text(text, max_length=5000):
    paragraphs = text.split('\n')
    chunks, current_chunk = [], ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < max_length:
            current_chunk += para + '\n'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + '\n'
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# 3. Convert text chunks to speech
def text_to_speech_offline(text_chunks, output_prefix="audiobook_part"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)       # Adjust speed here
    engine.setProperty('volume', 1.0)

    # Choose a voice (0 = male, 1 = female)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    for idx, chunk in enumerate(text_chunks):
        output_file = f"{output_prefix}{idx+1}.mp3"
        print(f"🔊 Saving part {idx+1} as {output_file}...")
        engine.save_to_file(chunk, output_file)
        engine.runAndWait()

    engine.stop()
    print("✅ Audiobook conversion complete!")

# 4. Main function
if __name__ == "__main__":
    docx_path = "novel.docx"  # Replace with your file path
    print("📖 Reading the document...")
    full_text = read_docx(docx_path)

    print("✂️ Splitting text into chunks...")
    chunks = split_text(full_text, max_length=5000)

    print("🎙️ Converting text to speech...")
    text_to_speech_offline(chunks)
