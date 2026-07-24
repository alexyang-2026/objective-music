from pathlib import Path

import pretty_midi

def parse_midi(file_path: str):

    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"MIDI file not found: {path}")


    midi_data = pretty_midi.PrettyMIDI(str(path))

    # List that contains all the notes we have performed
    performed_notes = []

    # A note ID that will keep increasing with each subsequent note
    note_id = 0

    for instrument_index, instrument in enumerate(midi_data.instruments):

        # Edge case - if the instrument detected is percussion don't add anything because there's no pitch
        if instrument.is_drum:
            continue

        for midi_note in instrument.notes:

            # Edge case - if the note is malformed (i.e. the end time is <= the start time of the note)
            if midi_note.end <= midi_note.start:
                continue

            performed_note = {
                "id": note_id,
                "pitch": midi_note.pitch,
                "onset": float(midi_note.start),
                "offset": float(midi_note.end),
                "duration": float(midi_note.end - midi_note.start),
                "velocity": midi_note.velocity,
                "instrument": instrument_index,
                "instrument_name": "Piano"
            }

            performed_notes.append(performed_note)
            note_id += 1

    # Sort the performed notes by the time of playing
    performed_notes.sort(
        key=lambda performed_note: (
            performed_note["onset"],
            performed_note["pitch"]
        )
    )

    return performed_notes


# Test - DELETE LATER
notes = parse_midi("data/recordings/liszt_transcendental_1_Huang.mid")

for performed_note in notes[:20]:
    print(performed_note)