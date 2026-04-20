import random

LOCATIONS = [
    {
        "name": "Yosemite National Park",
        "type": "Hiking",
        "description": "Granite cliffs, waterfalls, and unforgettable valley trails.",
    },
    {
        "name": "Great Smoky Mountains",
        "type": "Hiking/Camping",
        "description": "Lush forests, scenic overlooks, and lots of wildlife.",
    },
    {
        "name": "Zion National Park",
        "type": "Hiking",
        "description": "Canyon hikes with dramatic views and red rock landscapes.",
    },
    {
        "name": "Banff National Park",
        "type": "Hiking/Camping",
        "description": "Turquoise lakes, mountain trails, and alpine campsites.",
    },
    {
        "name": "Joshua Tree National Park",
        "type": "Camping",
        "description": "Desert landscapes, starry nights, and unique rock formations.",
    },
]

def get_location():
    return random.choice(LOCATIONS)