from moviepy.editor import VideoFileClip
import moviepy.editor as mp
from openai import OpenAI
import csv
import pysrt

client = OpenAI()

# Step 1: Convert video to audio
input_video_path = 'sample.mp4'
output_audio_path = 'sample.mp3'

video_clip = VideoFileClip(input_video_path)
audio_clip = video_clip.audio
audio_clip.write_audiofile(output_audio_path, codec='mp3')
audio_clip.close()
video_clip.close()

print("Conversion to Audio complete!")

# Step 2: Transcribe the audio
audio_file = open(output_audio_path, "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    language='en',
    file=audio_file,
    response_format='srt'
)
audio_file.close()

# Step 3: Save the transcription to an SRT file
with open("sample.srt", "w") as srt_file:
    srt_file.write(transcript)

print("Transcript written to sample.srt")

# Step 4: Parse SRT and check each segment for moderation
subs = pysrt.open("sample.srt")

# Prepare a CSV file to log flagged content
with open("flagged_content.csv", "w", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Timestamp", "Content"])

    for sub in subs:
        # Send each subtitle text to the moderation API
        response = client.moderations.create(input=sub.text)
        output = response.results[0]    

        if output.flagged == True:
            timestamp = f"{sub.start} --> {sub.end}"
            writer.writerow([timestamp, sub.text])
            print(f"Flagged content logged: {timestamp}")

print("Moderation check complete and flagged content logged to flagged_content.csv.")



