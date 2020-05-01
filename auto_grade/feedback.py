import random


BAD_RESPONSES = (
    "Please use the learning aids and spend more time on each task.",
    "Next time, re-attempt the task if you get below 50%.",
    "Please review this topic and re-attempt.",
)
AVG_RESPONSES = (
    "Please look at the learning aids for the tasks you've got low scores in.",
    "Well done for correctly completing some of the tasks!",
    "Next time please re-attempt those tasks you scored low in.",
)
GOOD_RESPONSES = (
    "Excellent!",
    "Well done!",
    "Fantastic!",
    "Outstanding in all regards.",
    "Keep up the great work!",
)


def get_feedback_comment(score: int) -> str:
    """Get the feedback comment for this score."""
    if score < 40:
        return random.choice(BAD_RESPONSES)
    if 40 <= score < 70:
        return random.choice(AVG_RESPONSES)
    return random.choice(GOOD_RESPONSES)
