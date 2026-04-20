import random

QUOTES = [
    "Success is the sum of small efforts repeated day in and day out. - Robert Collier",
    "Discipline is choosing between what you want now and what you want most. - Abraham Lincoln",
    "Do something today that your future self will thank you for. - Sean Patrick Flanery",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The best way out is always through. - Robert Frost",
]

def get_quote():
    return random.choice(QUOTES)