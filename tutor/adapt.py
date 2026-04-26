"""Difficulty adaptation logic"""

def should_increase_difficulty(confidence):
    """Check if student should move to harder questions (>70% confidence)"""
    return confidence > 0.7

def should_decrease_difficulty(confidence):
    """Check if student should move to easier questions (<40% confidence)"""
    return confidence < 0.4
