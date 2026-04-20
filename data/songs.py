import random

SONGS = [
    {
        "title": "Knockin' on Heaven's Door",
        "artist": "Bob Dylan",
        "chords": "G - D - Am",
    },
    {
        "title": "Horse with No Name",
        "artist": "America",
        "chords": "Em - D6add9/F#",
    },
    {
        "title": "Wonderwall",
        "artist": "Oasis",
        "chords": "Em7 - G - Dsus4 - A7sus4",
    },
    {
        "title": "Stand by Me",
        "artist": "Ben E. King",
        "chords": "G - Em - C - D",
    },
    {
        "title": "Sweet Home Alabama",
        "artist": "Lynyrd Skynyrd",
        "chords": "D - C - G",
    },
]

def get_song():
    return random.choice(SONGS)