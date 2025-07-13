import pyaudio
import wave
import librosa
import numpy as np
import time
from textblob import TextBlob  # For basic sentiment/style analysis

# Record audio from microphone
def record_audio(filename="temp_audio.wav", duration=5):
    print("Please play the audio now. Recording for 5 seconds...")
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Recording complete.")
    return filename

# Analyze audio features
def analyze_audio(audio_file):
    y, sr = librosa.load(audio_file)
    pitch = librosa.pitch_tuning(y)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    energy = np.mean(librosa.feature.rms(y=y))  # Volume/energy level
    return pitch, tempo, energy

# Analyze transcript for style
def analyze_transcript(transcript):
    blob = TextBlob(transcript)
    sentiment = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
    word_count = len(transcript.split())
    speed = word_count / 5  # Words per second (assuming 5-second audio)
    return sentiment, speed

# Generate descriptions with word count constraints
def generate_descriptions(pitch, tempo, energy, sentiment, speed, transcript):
    # Speech Characteristics (20-30 words)
    pitch_desc = "high" if pitch > 0 else "low"
    tone_desc = "clear" if energy > 0.01 else "soft"
    speed_desc = "fast" if speed > 2 else "slow"
    characteristics = f"The voice has a {pitch_desc} pitch, {tone_desc} tone, and {speed_desc} speed, reflecting distinct vocal traits audible throughout the recording."
    assert 20 <= len(characteristics.split()) <= 30, "Characteristics word count out of range"

    # Speech Style (25-30 words)
    formality = "formal" if sentiment > 0.2 else "informal" if sentiment < -0.2 else "neutral"
    confidence = "confident" if energy > 0.01 and speed > 1.5 else "hesitant"
    style = f"The speech style is {formality} and {confidence}, with a consistent flow of words that suggests a deliberate approach to communication, shaped by tone and pacing."
    assert 25 <= len(style.split()) <= 30, "Style word count out of range"

    # Speech Delivery (30-40 words)
    pauses = "frequent pauses" if tempo < 100 else "smooth flow"
    intonation = "varied intonation" if pitch != 0 else "monotone"
    delivery = f"The delivery features {pauses} and {intonation}, creating an engaging rhythm. Emphasis is notable in energy shifts, with a pace that holds attention effectively throughout the speech duration."
    assert 30 <= len(delivery.split()) <= 40, "Delivery word count out of range"

    return characteristics, style, delivery

# Main execution
def main():
    # Step 1: Record audio
    audio_file = record_audio()

    # Step 2: Prompt for transcript
    transcript = input("Please enter the transcript of the audio: ")

    # Step 3: Analyze and generate descriptions
    pitch, tempo, energy = analyze_audio(audio_file)
    sentiment, speed = analyze_transcript(transcript)
    characteristics, style, delivery = generate_descriptions(pitch, tempo, energy, sentiment, speed, transcript)

    # Output results
    print("\n=== Analysis Results ===")
    print(f"Speech Characteristics: {characteristics}")
    print(f"Speech Style: {style}")
    print(f"Speech Delivery: {delivery}")
    print("\nWord Counts:")
    print(f"Characteristics: {len(characteristics.split())} words")
    print(f"Style: {len(style.split())} words")
    print(f"Delivery: {len(delivery.split())} words")

if __name__ == "__main__":
    # Install dependencies: pip install pyaudio librosa numpy textblob
    main()