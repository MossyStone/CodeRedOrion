
# ==========================================
# CODERED ORION - SAY IT! PRACTICE GAME
# ==========================================

# Practice exercises
# Each exercise has an ID, phrase, and difficulty.

SAY_IT_EXERCISES = [
    {
        "id": 1,
        "phrase": "Hello",
        "emoji": "👋",
        "difficulty": "easy",
        "category": "greetings"
    },
    {
        "id": 2,
        "phrase": "Water",
        "emoji": "💧",
        "difficulty": "easy",
        "category": "needs"
    },
    {
        "id": 3,
        "phrase": "Thank you",
        "emoji": "💜",
        "difficulty": "easy",
        "category": "social"
    },
    {
        "id": 4,
        "phrase": "I need help",
        "emoji": "🫶",
        "difficulty": "medium",
        "category": "needs"
    },
    {
        "id": 5,
        "phrase": "I need water",
        "emoji": "🥤",
        "difficulty": "medium",
        "category": "needs"
    },
    {
        "id": 6,
        "phrase": "Can you help me?",
        "emoji": "🤝",
        "difficulty": "hard",
        "category": "needs"
    },
    {
        "id": 7,
        "phrase": "I would like a break",
        "emoji": "🌿",
        "difficulty": "hard",
        "category": "feelings"
    }
]


def get_say_it_exercises(difficulty=None):
    """
    Return all exercises or filter by difficulty.
    """

    if difficulty is None:
        return SAY_IT_EXERCISES

    return [
        exercise
        for exercise in SAY_IT_EXERCISES
        if exercise["difficulty"] == difficulty
    ]


def get_say_it_exercise(exercise_id):
    """
    Return a single exercise by ID.
    """

    for exercise in SAY_IT_EXERCISES:
        if exercise["id"] == exercise_id:
            return exercise

    return None
