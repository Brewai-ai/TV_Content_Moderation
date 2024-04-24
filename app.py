import streamlit as st
from moviepy.editor import VideoFileClip
from openai import OpenAI
import csv
import pysrt
import tempfile

client = OpenAI()

def convert_video_to_audio(video_file, audio_file_path):
    # Save the uploaded video file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(video_file.getvalue())
        video_file_path = tmpfile.name

    video_clip = VideoFileClip(video_file_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_file_path, codec='mp3')
    audio_clip.close()
    video_clip.close()

    # os.remove(video_file_path)


def transcribe_audio_to_srt(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language='en',
            response_format='srt'
        )
    return transcript

def check_moderation_and_log(srt_content):
    flagged_content = []
    subs = pysrt.from_string(srt_content)
    with open("flagged_content.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Timestamp", "Content"])
        for sub in subs:
            response =  client.moderations.create(input=sub.text)
            output = response.results[0] 
            if output.flagged == True:
                timestamp = f"{sub.start} --> {sub.end}"
                writer.writerow([timestamp, sub.text])
                flagged_content.append((timestamp, sub.text))
    return flagged_content

# Streamlit UI
st.title("Content Moderation")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])
if uploaded_file is not None:
    video_file_path = uploaded_file.name
    audio_file_path = "sample.mp3"

    with st.spinner('Converting video to audio...'):
        convert_video_to_audio(uploaded_file, audio_file_path)
        st.success("Conversion to audio complete!")

    with st.spinner('Transcribing audio to text...'):
        transcript = transcribe_audio_to_srt(audio_file_path)
        st.success("Transcription complete!")

    with st.spinner('Checking content for moderation...'):
        flagged_content = check_moderation_and_log(transcript)
        if flagged_content:
            st.write("Flagged content found:")
            for timestamp, text in flagged_content:
                st.write(f"{timestamp}: {text}")
        else:
            st.write("No flagged content found.")
        st.success("Moderation check complete.")
