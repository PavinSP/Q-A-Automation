import json
from gtts import gTTS
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
from moviepy.editor import TextClip, concatenate_videoclips, AudioFileClip

# Step 1: Load questions and answers
with open("questions.json", "r") as file:
    qa_list = json.load(file)

def wrap_text(text, max_width):
    # This function will wrap the text to fit within the specified width
    # 'max_width' is the maximum length per line
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
    
    return "\n".join(lines)

def wrap_text(text, max_width):
    # This function will wrap the text to fit within the specified width
    # 'max_width' is the maximum length per line
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
    
    return "\n".join(lines)

# Step 2: Generate audio for each question and answer
audio_files = []
for idx, qa in enumerate(qa_list):
    text = f"Question: {qa['question']}. Answer: {qa['answer']}"
    tts = gTTS(text)
    audio_filename = f"audio_{idx+1}.mp3"
    tts.save(audio_filename)
    audio_files.append(audio_filename)

# Step 3: Generate video for each question and answer
max_width = 40  # Define the max characters per line

# Step 3: Generate video for each question and answer
clips = []
for idx, qa in enumerate(qa_list):
    # Wrap the question and answer
    wrapped_question = wrap_text(qa['question'], max_width)
    wrapped_answer = wrap_text(qa['answer'], max_width)
    
    # Create text clips for the question and answer
    question_clip = TextClip(f"Q: {wrapped_question}", fontsize=40, color='white', bg_color='black', size=(1280, 720)).set_position('center').set_duration(5)
    answer_clip = TextClip(f"A: {wrapped_answer}", fontsize=30, color='white', bg_color='black', size=(1280, 720)).set_position('center').set_duration(10)
    
    # Add audio to the combined clips
    audio = AudioFileClip(audio_files[idx])
    qa_clip = concatenate_videoclips([question_clip, answer_clip]).set_audio(audio)
    clips.append(qa_clip)

# Step 4: Concatenate all Q&A clips into a single video
final_video = concatenate_videoclips(clips)
final_video.write_videofile("final_video.mp4", fps=24)
