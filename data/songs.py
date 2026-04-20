import random

SONGS = [
    {
        "title": "Knockin' on Heaven's Door",
        "artist": "Bob Dylan",
        "chords": "G - D - Am",
        "difficulty": "easy",
    },
    {
        "title": "Horse with No Name",
        "artist": "America",
        "chords": "Em - D6add9/F#",
        "difficulty": "easy",
    },
    {
        "title": "Wonderwall",
        "artist": "Oasis",
        "chords": "Em7 - G - Dsus4 - A7sus4",
        "difficulty": "medium",
    },
    {
        "title": "Stand by Me",
        "artist": "Ben E. King",
        "chords": "G - Em - C - D",
        "difficulty": "medium",
    },
    {
        "title": "Sweet Home Alabama",
        "artist": "Lynyrd Skynyrd",
        "chords": "D - C - G",
        "difficulty": "hard",
    },
    {
        "title": "Hotel California",
        "artist": "Eagles",
        "chords": "Bm - F# - A - E - G - D - Em - F#",
        "difficulty": "hard",
    },
]


DIFFICULTY_ORDER = ["easy", "medium", "hard"]


def _song_id(song):
    return f"{song['title']}::{song['artist']}"


def get_song(used_song_ids=None, target_difficulty=None, excluded_artist=None):
    used_song_ids = set(used_song_ids or [])
    available_songs = [song for song in SONGS if _song_id(song) not in used_song_ids]
    if target_difficulty:
        difficulty_filtered = [
            song for song in available_songs if song["difficulty"] == target_difficulty
        ]
        if difficulty_filtered:
            available_songs = difficulty_filtered

    if excluded_artist:
        non_repeating_artist = [
            song for song in available_songs if song["artist"] != excluded_artist
        ]
        if non_repeating_artist:
            available_songs = non_repeating_artist

    if not available_songs:
        available_songs = SONGS
    return random.choice(available_songs)
