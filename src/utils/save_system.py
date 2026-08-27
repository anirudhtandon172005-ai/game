"""
Save System for Kart Rush
Handles player progression, unlocks, and persistent data.
"""

import json
import os
from pathlib import Path
from datetime import datetime


class SaveSystem:
    """Manages game save/load functionality."""
    
    DEFAULT_SAVE_DATA = {
        'player': {
            'name': 'Racer',
            'total_races': 0,
            'total_wins': 0,
            'total_podiums': 0,
            'best_lap_times': {},  # track_id -> time in seconds
        },
        'unlocks': {
            'karts': ['kart_default'],
            'tracks': ['sunset_coast'],
        },
        'progression': {
            'championship_points': 0,
            'championship_position': 0,
            'championship_race_index': 0,
        },
        'settings': {},
        'meta': {
            'save_version': 1,
            'last_played': None,
            'play_time_seconds': 0,
        }
    }
    
    def __init__(self):
        self._save_data = self._load_save()
        self._update_meta()
    
    def _load_save(self):
        """Load save data from file or return default."""
        save_path = Path.home() / '.kart_rush' / 'save.json'
        if save_path.exists():
            try:
                with open(save_path, 'r') as f:
                    data = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_with_defaults(data)
            except (json.JSONDecodeError, IOError):
                print("Warning: Save file corrupted, using defaults")
                return self.DEFAULT_SAVE_DATA.copy()
        return self._deep_copy(self.DEFAULT_SAVE_DATA)
    
    def _merge_with_defaults(self, data):
        """Merge loaded data with defaults to handle version changes."""
        result = self._deep_copy(self.DEFAULT_SAVE_DATA)
        self._recursive_update(result, data)
        return result
    
    def _deep_copy(self, obj):
        """Create a deep copy of nested dictionaries."""
        if isinstance(obj, dict):
            return {k: self._deep_copy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(item) for item in obj]
        else:
            return obj
    
    def _recursive_update(self, base, update):
        """Recursively update nested dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._recursive_update(base[key], value)
            else:
                base[key] = value
    
    def _update_meta(self):
        """Update metadata like last played timestamp."""
        self._save_data['meta']['last_played'] = datetime.now().isoformat()
    
    def save(self):
        """Save current data to file."""
        save_path = Path.home() / '.kart_rush'
        save_path.mkdir(parents=True, exist_ok=True)
        save_file = save_path / 'save.json'
        try:
            with open(save_file, 'w') as f:
                json.dump(self._save_data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save game: {e}")
    
    def get(self, *keys):
        """Get nested value using multiple keys."""
        data = self._save_data
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data
    
    def set(self, value, *keys):
        """Set nested value using multiple keys."""
        data = self._save_data
        for key in keys[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]
        data[keys[-1]] = value
        self.save()
    
    def add_unlock(self, unlock_type, unlock_id):
        """Add an unlock (kart or track)."""
        unlocks = self._save_data['unlocks'].get(unlock_type, [])
        if unlock_id not in unlocks:
            unlocks.append(unlock_id)
            self._save_data['unlocks'][unlock_type] = unlocks
            self.save()
    
    def has_unlock(self, unlock_type, unlock_id):
        """Check if player has unlocked something."""
        unlocks = self._save_data['unlocks'].get(unlock_type, [])
        return unlock_id in unlocks
    
    def record_race_result(self, position, total_racers, track_id=None):
        """Record race results for progression."""
        player = self._save_data['player']
        player['total_races'] += 1
        
        if position == 1:
            player['total_wins'] += 1
        
        if position <= 3:
            player['total_podiums'] += 1
        
        self.save()
    
    def record_lap_time(self, track_id, time_seconds):
        """Record best lap time for a track."""
        best_times = self._save_data['player']['best_lap_times']
        if track_id not in best_times or time_seconds < best_times[track_id]:
            best_times[track_id] = time_seconds
            self.save()
            return True  # New record
        return False
    
    def get_best_lap_time(self, track_id):
        """Get best lap time for a track."""
        return self._save_data['player']['best_lap_times'].get(track_id)
    
    def reset_progress(self):
        """Reset all progression (for testing/debugging)."""
        self._save_data = self._deep_copy(self.DEFAULT_SAVE_DATA)
        self.save()
    
    @property
    def data(self):
        return self._save_data
