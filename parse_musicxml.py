from pathlib import Path
from music21 import chord, converter, note, stream


# Input a file_path that is a string
def parse_musicxml(file_path: str):

    # Read a MusicXML score and return one record per written note
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Score not found: {path}")

    score = converter.parse(path)

    # musical_entities will be a list containing a dictionary of all the notes in the score
    musical_entities = []

    # Go through each of the score's parts
    # The right hand will have part_index 0, and the left hand part_index 1
    for part_index, part in enumerate(score.parts):
        for element in part.recurse().notesAndRests:

            # If it is a note, add a specific dictionary into musical_entities list
            if isinstance(element, note.Note):
                entity = {
                    "type": "note",
                    "pitches": [element.pitch.midi],
                    "offset": float(element.getOffsetInHierarchy(part)),
                    "duration": float(element.quarterLength),
                    "part": part_index
                }

                musical_entities.append(entity)

            # If it is a chord, do the same
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

            # If it is a rest, do the same
            elif isinstance(element, note.Rest):
                entity = {
                    "type": "rest",
                    "pitches": [],
                    "offset": float(element.getOffsetInHierarchy(part)),
                    "duration": float(element.quarterLength),
                    "part": part_index
                }

                musical_entities.append(entity)

    # Sort the musical notes by their offset time (instead of listing all RH notes and then all LH notes, list them according to their time position)
    musical_entities.sort(
        key=lambda entity: {
            entity["offset"],
            entity["part"]
        }
    )


    return musical_entities


# Test — DELETE LATER
entities = parse_musicxml("/Users/alexyang/Desktop/objective-music-analysis/data/scores/liszt_transcendental_1.mxl")

for entity in entities[:50]:
    print(entity)

    

    