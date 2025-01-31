from pydub import AudioSegment


def mp3_to_wav(path): # Convert mp3 to wav
    sound = AudioSegment.from_mp3(path)
    wav_sound = sound.export(path.replace('.mp3', '.wav'), format='wav')
    return wav_sound


def audio_splitter(audio, silence_thresh, min_silence_len, export_path):

    full_audio = AudioSegment.from_wav(audio)
    segments = split_on_silence(full_audio, silence_thresh=silence_thresh, min_silence_len=min_silence_len)

    for i, segment in enumerate(segments):
        segment.export(export_path + f'/{i}.wav', format='wav')
    
