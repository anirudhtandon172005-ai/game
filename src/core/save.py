"""
Kart Rush - Save System
Versioned, corruption-proof save/load system.
Stores: settings, unlocks, best laps, championship progress.
"""

import json
import os

SAVE_VERSION = 1
SAVE_KEY = f"kartrush.save.v{SAVE_VERSION}"

DEFAULT_DATA = {
    "settings": {
        "master_volume": 1.0,
        "music_volume": 0.8,
        "sfx_volume": 1.0,
        "quality": "medium",
        "camera_distance": 2,
        "screen_shake": True
    },
    "unlocks": {
        "karts": ["kart_default"],
        "tracks": ["sunset_coast"]
    },
    "best_laps": {},
    "championships": {},
    "time_trials": {}
}


def get_save_path():
    """Get the save file path."""
    home = os.path.expanduser("~")
    save_dir = os.path.join(home, ".kart_rush")
    os.makedirs(save_dir, exist_ok=True)
    return os.path.join(save_dir, "save.json")


def save(data):
    """Save game data with versioning."""
    save_data = {
        "version": SAVE_VERSION,
        "data": data
    }
    try:
        with open(get_save_path(), 'w') as f:
            json.dump(save_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False


def load():
    """Load game data with corruption recovery."""
    try:
        with open(get_save_path(), 'r') as f:
            save_data = json.load(f)
        
        # Version check
        if save_data.get("version") != SAVE_VERSION:
            print(f"Save version mismatch: expected {SAVE_VERSION}, got {save_data.get('version')}")
            return DEFAULT_DATA.copy()
        
        data = save_data.get("data", {})
        # Merge with defaults for any missing keys
        return merge_defaults(data, DEFAULT_DATA)
    
    except FileNotFoundError:
        print("No save file found, using defaults")
        return DEFAULT_DATA.copy()
    except json.JSONDecodeError as e:
        print(f"Save corrupted: {e}, restoring defaults")
        return DEFAULT_DATA.copy()
    except Exception as e:
        print(f"Load error: {e}, restoring defaults")
        return DEFAULT_DATA.copy()


def merge_defaults(data, defaults):
    """Recursively merge data with defaults."""
    result = defaults.copy()
    for key, value in data.items():
        if key in result:
            if isinstance(value, dict) and isinstance(result[key], dict):
                result[key] = merge_defaults(value, result[key])
            else:
                result[key] = value
    return result


def corrupt_save_for_testing():
    """Write corrupted save data for QA testing."""
    with open(get_save_path(), 'w') as f:
        f.write("{{{invalid json}}}")
    print("Save corrupted for testing")


def reset_save():
    """Delete save file and reset to defaults."""
    try:
        os.remove(get_save_path())
        print("Save reset")
    except FileNotFoundError:
        pass
    return DEFAULT_DATA.copy()
