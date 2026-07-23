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


parse_musicxml("/Users/alexyang/Desktop/objective-music-analysis/data/scores/liszt_transcendental_1.mxl")

    

    