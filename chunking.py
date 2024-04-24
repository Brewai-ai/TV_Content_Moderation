from pydub import AudioSegment

# Load your audio file (replace 'your_large_audio_file.mp3' with your file's path)
audio_file_path = 'output_audio.mp3'
audio = AudioSegment.from_file(audio_file_path)

# Calculate the target duration for each chunk in milliseconds
# 1 byte = 8 bits, so 10 MB = 10 * 1024 * 1024 * 8 bits
target_size_bits = 10 * 1024 * 1024 * 8
# Calculate duration in milliseconds for approximately 10 MB chunk
# Note: audio.frame_rate * audio.frame_width gives the byte rate
target_duration_ms = (target_size_bits / (audio.frame_rate * audio.frame_width * audio.channels)) * 1000

chunks = []
start_point = 0
end_point = target_duration_ms
while start_point < len(audio):
    # Ensure the end point does not exceed the audio length
    end_point = min(start_point + target_duration_ms, len(audio))
    chunk = audio[start_point:end_point]
    chunks.append(chunk)
    start_point = end_point

# Export each chunk to separate files
for i, chunk in enumerate(chunks):
    chunk_file_path = f"chunk{i}.mp3"  # You can change the format to wav or other supported formats
    print(f"Exporting {chunk_file_path}...")
    chunk.export(chunk_file_path, format="mp3")
