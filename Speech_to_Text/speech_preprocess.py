# %%
import os
import queue
import sounddevice as sd
import vosk
from vosk import Model
import json
import time 

# %%

# Set and load the model  
MODEL_PATH = "C:/Users/Gaming/Desktop/bum\Model/vosk-model-en-us-0.22"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Ensure it's downloaded and extracted.")

# %%
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)
# %%
# Queue for processing audio input -> Helps in real-time processing
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Puts the recorded audio into a queue for processing."""
    if status:
        print(status, flush=True)
    audio_queue.put(bytes(indata))

# Function to capture and transcribe audio in real time
def transcribe_audio():
    with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype="int16",
                           channels=1, callback=audio_callback):
        print("Listening... (Press Ctrl+C to stop)")

        last_time = time.time()
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print("You said:", result["text"])
                last_time = time.time()
                recognizer.Reset()  # Reset the recognizer state after printing the result
            elif time.time() - last_time > 1:  # 1 second of silence
                if recognizer.PartialResult():
                    result = json.loads(recognizer.PartialResult())
                    print("You said:", result["partial"])
                last_time = time.time()

# Run the speech-to-text function
try:
    transcribe_audio()
except KeyboardInterrupt:
    print("\nStopped.")#



# %%
