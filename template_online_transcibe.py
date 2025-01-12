import openai
from datetime import datetime
from helper.file_selector import select_file

start = datetime.now()

client = openai.OpenAI()

assets_dir = "assets"
selected_file_path = select_file(assets_dir)

audio_file = open(selected_file_path, "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

print(transcript.text)

end = datetime.now()
difference = end - start
print(f"Time spent: {difference}")
