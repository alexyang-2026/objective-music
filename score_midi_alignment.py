# Call our functions from the other two files
from midi_parser import parse_midi
from parse_musicxml import parse_musicxml

def extract_score_notes(score_entities):
    score_notes = []

    for entity_index, entity in enumerate(score_entities):
        if entity["type"] == "rest":
            continue

        for pitch in sorted(entity["pitches"]):
            score_notes.append({
                "pitch": pitch,
                "offset": entity["offset"],
                "duration": entity["duration"],
                "part": entity["part"],
                "entity_index": entity_index
            })

        score_notes.sort(
            key=lambda score_note: (
                score_note["offset"],
                score_note["pitch"],
                score_note["part"]
            )
        )

        for score_note_id, score_note in enumerate(score_notes):
            score_note["id"] = score_note_id

        return score_notes


def extract_midi_pitch_sequence(performed_notes):
    return [note["pitch"] for note in performed_notes]


def align_score_to_midi(score_notes, performed_notes):
    score_count = len(score_notes)
    midi_count = len(performed_notes)

    # Let each gap cost = 1 to represent the cost if there is a missing score note or an extra MIDI note 
    gap_cost = 1

    # Create the dynamic programming table
    # Create a table of all zeros so later, Python can add the note values inside the table
    # The top-left cell, dp[0][0], will remain = 0 because it means "no score notes processed / no MIDI notes processed"
    # The other zeros will be replaced soon by the cost it will take to move from one note to another
    dp = [
            [0] * (midi_count + 1)
            for _ in range(score_count + 1)
        ]

    """
    What the DP Table Setup Looks Like:

                        Number of MIDI notes considered
                    0   1   2   3   4   5   ...
    Number      0
    of          1
    score       2
    notes       3
    considered  ...

    Each cell stores the lowest cost needed to account for the score notes and MIDI notes included at that position.
    Basically, the first column assumes that we are considering 0 notes, and hence all values in that column will contain the costs needed if the MIDI list was completely empty.

    Thus, we can just go ahead and put those cost values in the first column.
    """
    for score_index in range(1, score_count + 1):
        dp[score_index][0] = score_index * gap_cost



### TEST (DELETE LATER)
score_entities = parse_musicxml(
    "data/scores/liszt_transcendental_1.mxl"
)

performed_notes = parse_midi(
    "data/recordings/liszt_transcendental_1_Huang.mid"
)
