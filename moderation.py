from moviepy.editor import VideoFileClip
import moviepy.editor as mp
from openai import OpenAI

client = OpenAI()

# Step 1: Convert video to audio
input_video_path = 'sample.mp4'
output_audio_path = 'output_audio.mp3'

video_clip = VideoFileClip(input_video_path)
audio_clip = video_clip.audio
audio_clip.write_audiofile(output_audio_path, codec='mp3')
audio_clip.close()
video_clip.close()

print("Conversion to Audio complete!")

# Step 2: Transcribe the audio
audio_file = open("output_audio.mp3", "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    language='en',
    file=audio_file,
    response_format='srt'
)

# Step 3: Check transcription using Moderation API
moderation_result = client.moderations.create(
    input=transcript
)

# Check for moderation violations
if moderation_result['status'] == 'failed':
    print("Transcription contains moderation violations.")
    print("Violations: ", moderation_result['violations'])
else:
    print("Transcription does not contain moderation violations.")

# Step 4: Save the transcription
with open("output_transcript.srt", "w") as srt_file:
    srt_file.write(transcript)

print("Transcript written to output_transcript.srt")
