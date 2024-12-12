import json
import os
from gtts import gTTS
from moviepy import TextClip, concatenate_videoclips, AudioFileClip

# Function to wrap text to avoid single-line overflow
def wrap_text(text, max_width=40):
    words = text.split()
    lines = []
    current_line = words[0]
    
    for word in words[1:]:
        if len(current_line + " " + word) <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)
    return "\n".join(lines)

# Function to estimate duration based on text length (in characters)
def estimate_duration(text, chars_per_second=15):
    return max(2, len(text) / chars_per_second)

# Step 1: Load questions and answers
with open("questions.json", "r") as file:
    qa_list = json.load(file)

# Step 2: Generate audio for each question and answer
audio_files = []
for idx, qa in enumerate(qa_list):
    text = f"Question: {qa['question']}. Answer: {qa['answer']}"
    audio_filename = f"audio_{idx+1}.mp3"
    
    # Check if audio file already exists, skip creation if it does
    if not os.path.exists(audio_filename):
        tts = gTTS(text)
        tts.save(audio_filename)
    
    audio_files.append(audio_filename)

# Step 3: Generate video for each question and answer
clips = []
for idx, qa in enumerate(qa_list):
    # Wrap text for better display
    wrapped_question = wrap_text(qa['question'], max_width=40)
    wrapped_answer = wrap_text(qa['answer'], max_width=40)
    
    # Estimate the duration based on text length
    question_duration = estimate_duration(qa['question'], chars_per_second=15)
    answer_duration = estimate_duration(qa['answer'], chars_per_second=15)
    
    # Create text clips for the question and answer with dynamic durations
    question_clip = TextClip(f"Q: {wrapped_question}", font="Arial", fontsize=40, color='white', bg_color='black', size=(1280, 720)).set_position('center').set_duration(question_duration)
    answer_clip = TextClip(f"A: {wrapped_answer}", font="Arial", fontsize=30, color='white', bg_color='black', size=(1280, 720)).set_position('center').set_duration(answer_duration)

    # Generate audio for the question and answer separately
    question_audio = AudioFileClip(audio_files[idx]).subclip(0, question_duration)  # Match audio to question duration
    answer_audio = AudioFileClip(audio_files[idx]).subclip(question_duration, question_duration + answer_duration)  # Match audio to answer duration
    
    # Set the audio to match their respective durations
    question_clip = question_clip.set_audio(question_audio)
    answer_clip = answer_clip.set_audio(answer_audio)
    
    # Concatenate the question and answer clips
    qa_clip = concatenate_videoclips([question_clip, answer_clip])
    
    clips.append(qa_clip)

# Step 4: Concatenate all Q&A clips into a single video
final_video = concatenate_videoclips(clips)
final_video.write_videofile("final_video.mp4", fps=24)

# Delete temporary MP3 files
for audio_file in audio_files:
    os.remove(audio_file)