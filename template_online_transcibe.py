import openai
from datetime import datetime

start = datetime.now()

client = openai.OpenAI()

audio_file = open("assets/Sonnet_18_William_Shakespeare.mp3", "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

print(transcript.text)

end = datetime.now()
difference = end - start
print(f"Time spent: {difference}")
