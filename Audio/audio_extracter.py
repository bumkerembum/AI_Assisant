from pydub import AudioSegment


def mp3_to_wav(path): # Convert mp3 to wav
    sound = AudioSegment.from_mp3(path)
    wav_sound = sound.export(path.replace('.mp3', '.wav'), format='wav')
    return wav_sound

