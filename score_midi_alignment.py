# Call our functions from the other two files
from midi_parser import parse_midi
from parse_musicxml import parse_musicxml

def extract_score_pitch_sequence(score_entities):
    pitch_sequence = []

    for entity in  score_entities:
        if entity["type"] == "rest":
            continue

        for pitch in entity["pitches"]:
            pitch_sequence.append(pitch)

    return pitch_sequence


def extract_midi_pitch_sequence(performed_notes):
    return [note["pitch"] for note in performed_notes]


# Function that allows us to compare the midi to the score
def compare_sequences(score_entities, performed_notes):
    score_pitches = extract_score_pitch_sequence(score_entities)
    midi_pitches = extract_midi_pitch_sequence(performed_notes)

    print(f"Score pitch count: {len(score_pitches)}")
    print(f"MIDI pitch count: {len(midi_pitches)}")

    print("\nFirst 20 score pitches:")
    print(score_pitches[:20])

    print("\nFirst 20 MIDI pitches:")
    print(midi_pitches[:20])


### TEST (DELETE LATER)
score_entities = parse_musicxml(
    "data/scores/liszt_transcendental_1.mxl"
)

performed_notes = parse_midi(
    "data/recordings/liszt_transcendental_1_Huang.mid"
)

compare_sequences(score_entities, performed_notes)