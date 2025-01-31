import os
import queue
import sounddevice as sd
import vosk
import json

# Set and load the model  
MODEL_PATH = "C:/Users/Gaming/Desktop/bum\Model/vosk-model-en-us-0.22"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Ensure it's downloaded and extracted.")

model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Queue for processing audio input -> Helps in real-time processing
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Puts the recorded audio into a queue for processing."""
    if status:
        print(status, flush=True)
    audio_queue.put(bytes(indata))

# Function to capture and transcribe audio in real time
def transcribe_audio():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=audio_callback):
        print("Listening... (Press Ctrl+C to stop)")

        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print("You said:", result["text"])

# Run the speech-to-text function
try:
    transcribe_audio()
except KeyboardInterrupt:
    print("\nStopped.")
