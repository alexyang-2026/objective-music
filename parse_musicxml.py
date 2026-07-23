from pathlib import Path
from music21 import chord, converter, note, stream


# Input a file_path that is a string
def parse_musicxml(file_path: str):

    # Read a MusicXML score and return one record per written note
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Score not found: {path}")

    score = converter.parse(path)

    right_hand = score.parts[0]
    left_hand = score.parts[1]

    musical_entities = []

    for part_index, part in enumerate(score.parts):
        for element in part.recurse().notesAndRests:

            if isinstance(element, note.Note):
                entity = {
                    "type": "note",
                    "pitches": [element.pitch.midi],
                    "offset": float(element.getOffsetInHierarchy(part)),
                    "duration": float(element.quarterLength),
                    "part": part_index
                }

                musical_entities.append(entity)

            elif isinstance(element, chord.Chord):
                entity = {
                    "type": "chord",
                    "pitches": [
                        chord_note.pitch.midi
                        for chord_note in element.notes
                    ],
                    "offset": float(element.getOffsetInHierarchy(part)),
                    "duration": float(element.quarterLength),
                    "part": part_index
                }

                musical_entities.append(entity)

            elif isinstance(element, note.Rest):
                entity = {
                    "type": "rest",
                    "pitches": [],
                    "offset": float(element.getOffsetInHierarchy(part)),
                    "duration": float(element.quarterLength),
                    "part": part_index
                }

                musical_entities.append(entity)
    return musical_entities


# Test — DELETE LATER
entities = parse_musicxml("/Users/alexyang/Desktop/objective-music-analysis/data/scores/liszt_transcendental_1.mxl")

for entity in entities[:50]:
    print(entity)

    

    