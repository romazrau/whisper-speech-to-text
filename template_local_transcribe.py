import whisper
from datetime import datetime
from helper.file_selector import select_file

start = datetime.now()

model = whisper.load_model("turbo")

assets_dir = "assets"
selected_file_path = select_file(assets_dir)

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio(selected_file_path)
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)

end = datetime.now()
difference = end - start
print(f"Time spent: {difference}")