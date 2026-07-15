"""
storage.py
-----------
Utility module that handles all reading/writing of JSON data files.
Keeping storage logic in one place makes it easy to switch to a
different backend (CSV, SQLite, etc.) later without touching the
business-logic modules.
"""

import json
import os


def load_data(file_path, default=None):
    """
    Load JSON data from a file.

    If the file does not exist, it is created with the given default
    value (an empty list, by default) so the rest of the application
    can always assume the file is present.

    Args:
        file_path (str): Path to the JSON file.
        default: Value to use/write if the file does not exist.

    Returns:
        The parsed JSON data (usually a list of dicts).
    """
    if default is None:
        default = []

    # Make sure the folder that should contain the file exists.
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(file_path):
        save_data(file_path, default)
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except (json.JSONDecodeError, OSError) as error:
        print(f"⚠️  Warning: Could not read '{file_path}' ({error}). "
              f"Starting with empty data.")
        return default


def save_data(file_path, data):
    """
    Save data to a JSON file with nice formatting.

    Args:
        file_path (str): Path to the JSON file.
        data: JSON-serialisable data (list/dict) to save.
    """
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"❌ Error: Could not save data to '{file_path}' ({error}).")
