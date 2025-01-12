import whisper
from datetime import datetime
from helper.file_selector import select_file

start = datetime.now()

model = whisper.load_model("turbo")

assets_dir = "assets"
selected_file_path = select_file(assets_dir)

# Function to split audio into segments of a fixed duration (in seconds)
def split_audio(audio, segment_duration, sample_rate):
    segment_samples = segment_duration * sample_rate
    return [audio[i:i + segment_samples] for i in range(0, len(audio), segment_samples)]

# Load audio and split it into segments of 30 seconds
audio = whisper.load_audio(selected_file_path)
sample_rate = 16000  # Whisper's default sample rate
segments = split_audio(audio, 30, sample_rate)

# Process each segment and concatenate the results
full_transcription = []
for idx, segment in enumerate(segments):
    # Pad/trim each segment to fit 30 seconds
    segment = whisper.pad_or_trim(segment)

    # Make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(segment, n_mels=model.dims.n_mels).to(model.device)

    # Detect the spoken language
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    print(f"Segment {idx + 1}: Detected language: {detected_language}")

    # Decode the audio segment
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # Append the recognized text
    full_transcription.append(result.text)

# Combine all segments into a full transcription
final_result = " ".join(full_transcription)

# Print the final recognized text
print(final_result)

end = datetime.now()
difference = end - start
print(f"Time spent: {difference}")