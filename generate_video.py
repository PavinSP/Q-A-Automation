import json
from gtts import gTTS
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
from moviepy.editor import TextClip, concatenate_videoclips, AudioFileClip

# Step 1: Load questions and answers
with open("questions.json", "r") as file:
    qa_list = json.load(file)

# Step 2: Generate audio for each question and answer
audio_files = []
for idx, qa in enumerate(qa_list):
    text = f"Question: {qa['question']}. Answer: {qa['answer']}"
    tts = gTTS(text)
    audio_filename = f"audio_{idx+1}.mp3"
    tts.save(audio_filename)
    audio_files.append(audio_filename)

# Step 3: Generate video for each question and answer
clips = []
for idx, qa in enumerate(qa_list):
    # Create text clips for the question and answer
    question_clip = TextClip(f"Q: {qa['question']}", fontsize=50, color='white', bg_color='black', size=(1280, 720)).set_duration(5)
    answer_clip = TextClip(f"A: {qa['answer']}", fontsize=40, color='white', bg_color='black', size=(1280, 720)).set_duration(10)
    
    # Add audio to the combined clips
    audio = AudioFileClip(audio_files[idx])
    qa_clip = concatenate_videoclips([question_clip, answer_clip]).set_audio(audio)
    clips.append(qa_clip)

# Step 4: Concatenate all Q&A clips into a single video
final_video = concatenate_videoclips(clips)
final_video.write_videofile("final_video.mp4", fps=24)