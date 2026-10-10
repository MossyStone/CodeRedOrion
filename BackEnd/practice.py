
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


# ==========================================
# SAY IT! PRACTICE FEEDBACK
# ==========================================

def check_say_it_attempt(exercise_id, transcription):
    """
    Compare recognized speech with the target phrase.
    This is NOT a pronunciation assessment.
    """

    exercise = get_say_it_exercise(exercise_id)

    if exercise is None:
        return None

    target = exercise["phrase"]
    heard = transcription.strip()

    # Normalize text for comparison
    def normalize(text):
        return " ".join(
            text.casefold()
            .replace(".", "")
            .replace("!", "")
            .replace("?", "")
            .replace(",", "")
            .split()
        )

    matches = bool(heard) and (
        normalize(heard) == normalize(target)
    )

    if not heard:
        message = (
            "We couldn't recognize any words this time. "
            "You can listen again, retry, or move on."
        )

    elif matches:
        message = (
            "The speech recognizer heard the target phrase! "
            "You can practice again or try another phrase."
        )

    else:
        message = (
            "Here's what the speech recognizer heard. "
            "You can listen again, retry, or move on."
        )

    return {
        "exercise_id": exercise_id,
        "target_phrase": target,
        "transcription": heard,
        "text_matches": matches,
        "feedback": message
    }


# END OF SAY IT!


# ==========================================
# GAME 2: MATCH IT!
# ==========================================

MATCH_IT_ROUNDS = [
    {
        "id": 1,
        "phrase": "Water",
        "difficulty": "easy",
        "category": "needs",
        "options": [
            {"id": "water", "label": "Water", "emoji": "💧"},
            {"id": "food", "label": "Food", "emoji": "🍎"},
            {"id": "sleep", "label": "Sleep", "emoji": "🛏️"},
            {"id": "help", "label": "Help", "emoji": "🫶"}
        ],
        "answer": "water"
    },
    {
        "id": 2,
        "phrase": "I feel happy",
        "difficulty": "easy",
        "category": "feelings",
        "options": [
            {"id": "sad", "label": "Sad", "emoji": "😢"},
            {"id": "happy", "label": "Happy", "emoji": "😊"},
            {"id": "tired", "label": "Tired", "emoji": "😴"},
            {"id": "angry", "label": "Angry", "emoji": "😠"}
        ],
        "answer": "happy"
    },
    {
        "id": 3,
        "phrase": "I need a break",
        "difficulty": "medium",
        "category": "needs",
        "options": [
            {"id": "eat", "label": "Eat", "emoji": "🍽️"},
            {"id": "break", "label": "Break", "emoji": "🌿"},
            {"id": "read", "label": "Read", "emoji": "📖"},
            {"id": "walk", "label": "Walk", "emoji": "🚶"}
        ],
        "answer": "break"
    },
    {
        "id": 4,
        "phrase": "Please help me",
        "difficulty": "medium",
        "category": "needs",
        "options": [
            {"id": "water", "label": "Water", "emoji": "💧"},
            {"id": "help", "label": "Help", "emoji": "🤝"},
            {"id": "happy", "label": "Happy", "emoji": "😊"},
            {"id": "sleep", "label": "Sleep", "emoji": "🛏️"}
        ],
        "answer": "help"
    }
]


def get_match_it_rounds(difficulty=None):
    """Return all rounds or filter by difficulty."""

    if difficulty is None:
        return MATCH_IT_ROUNDS

    return [
        round_data
        for round_data in MATCH_IT_ROUNDS
        if round_data["difficulty"] == difficulty
    ]


def get_match_it_round(round_id):
    """Return a specific round."""

    for round_data in MATCH_IT_ROUNDS:
        if round_data["id"] == round_id:
            return round_data

    return None


def check_match_it_answer(round_id, selected_option):
    """Check whether the selected card matches the audio."""

    round_data = get_match_it_round(round_id)

    if round_data is None:
        return None

    valid_options = {
        option["id"]
        for option in round_data["options"]
    }

    if selected_option not in valid_options:
        return {"error": "invalid_option"}

    is_match = selected_option == round_data["answer"]

    return {
        "round_id": round_id,
        "selected_option": selected_option,
        "is_match": is_match,
        "feedback": (
            "You found the matching card!"
            if is_match
            else "Not that one. You can try again or move on."
        )
    }


# END OF MATCH IT!



