import random

LOCATIONS = [
    {
        "name": "Shouf Biosphere Reserve",
        "type": "Hiking",
        "difficulty": "easy",
        "country": "Lebanon",
        "description": "Cedar forests, fresh mountain air, and gentle scenic trails.",
    },
    {
        "name": "Tannourine Cedars Reserve",
        "type": "Hiking/Camping",
        "difficulty": "easy",
        "country": "Lebanon",
        "description": "Beautiful cedar groves with family-friendly routes and viewpoints.",
    },
    {
        "name": "Baatara Gorge",
        "type": "Hiking",
        "difficulty": "medium",
        "country": "Lebanon",
        "description": "A dramatic sinkhole and waterfall trail with rewarding scenery.",
    },
    {
        "name": "Qadisha Valley",
        "type": "Hiking/Camping",
        "difficulty": "medium",
        "country": "Lebanon",
        "description": "Historic valley paths, monasteries, and excellent mountain views.",
    },
    {
        "name": "Jabal Moussa Biosphere Reserve",
        "type": "Camping",
        "difficulty": "hard",
        "country": "Lebanon",
        "description": "Steeper climbs and longer routes for a full outdoor challenge.",
    },
    {
        "name": "Mount Sannine Trail",
        "type": "Hiking",
        "difficulty": "hard",
        "country": "Lebanon",
        "description": "High-altitude trail with strong climbs and wide panoramic views.",
    },
]


DIFFICULTY_ORDER = ["easy", "medium", "hard"]


def get_location(used_location_names=None, target_difficulty=None, excluded_type=None):
    used_location_names = set(used_location_names or [])
    available_locations = [loc for loc in LOCATIONS if loc["name"] not in used_location_names]
    if target_difficulty:
        difficulty_filtered = [
            loc for loc in available_locations if loc["difficulty"] == target_difficulty
        ]
        if difficulty_filtered:
            available_locations = difficulty_filtered

    if excluded_type:
        varied_type = [loc for loc in available_locations if loc["type"] != excluded_type]
        if varied_type:
            available_locations = varied_type

    if not available_locations:
        available_locations = LOCATIONS
    return random.choice(available_locations)
