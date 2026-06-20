import json
import os

SAVE_FILE = os.path.join(os.path.dirname(__file__), "save.json")

DEFAULT_SAVE = {
    "completed_levels": [],
}


def load_save():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return DEFAULT_SAVE.copy()
    return DEFAULT_SAVE.copy()


def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def complete_level(level_id):
    data = load_save()
    if level_id not in data["completed_levels"]:
        data["completed_levels"].append(level_id)
    save_game(data)


def is_level_unlocked(level_id, all_levels, completed_levels):
    for i, level in enumerate(all_levels):
        if level["id"] == level_id:
            if i == 0:
                return True
            return all_levels[i - 1]["id"] in completed_levels
    return False


def get_next_level(level_id, all_levels):
    for i, level in enumerate(all_levels):
        if level["id"] == level_id:
            if i + 1 < len(all_levels):
                return all_levels[i + 1]
            return None
    return None


def reset_progress():
    save_game(DEFAULT_SAVE.copy())
