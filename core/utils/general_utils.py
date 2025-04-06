import os

def ensure_dir_exists(path):
    """
    Creates the directory if it doesn't exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def format_feedback(feedback):
    """
    Cleans up feedback strings or applies styling.
    """
    return feedback.strip().capitalize()
