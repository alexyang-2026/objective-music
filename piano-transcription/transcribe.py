import librosa
from piano_transcription_inference import PianoTranscription, sample_rate

audio_path = "chopinballade4.wav" # Replace with whatever .wav filename you want
output_midi_path = "chopinballade4.mid" # Replace with the new name for the midi

audio, _ = librosa.load(audio_path, sr=sample_rate, mono=True)

transcriptor = PianoTranscription(device="cpu")

transcriptor.transcribe(audio, output_midi_path)

print("Done!")
