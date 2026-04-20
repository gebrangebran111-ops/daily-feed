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

def _song_id(song):
    return f"{song['title']}::{song['artist']}"


def get_song(used_song_ids=None):
    used_song_ids = set(used_song_ids or [])
    available_songs = [song for song in SONGS if _song_id(song) not in used_song_ids]
    if not available_songs:
        available_songs = SONGS
    return random.choice(available_songs)