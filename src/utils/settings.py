"""
Settings management for Kart Rush
Handles game configuration, graphics, audio, and control settings.
"""

import json
import os
from pathlib import Path


class Settings:
    """Manages game settings with save/load functionality."""
    
    DEFAULT_SETTINGS = {
        'graphics': {
            'fullscreen': False,
            'resolution': (1280, 720),
            'vsync': True,
            'fps_limit': 60,
            'shadows': True,
            'particles': True,
            'motion_blur': False,
        },
        'audio': {
            'master_volume': 0.8,
            'music_volume': 0.6,
            'sfx_volume': 0.8,
            'engine_sound': True,
        },
        'gameplay': {
            'camera_follow': True,
            'camera_shake': True,
            'motion_effects': True,
            'show_minimap': True,
            'show_waypoints': False,
        },
        'controls': {
            'accelerate': 'w',
            'brake': 's',
            'left': 'a',
            'right': 'd',
            'drift': 'space',
            'boost': 'shift',
            'use_item': 'e',
            'pause': 'escape',
        },
    }
    
    def __init__(self):
        self._settings = self._load_settings()
        self._apply_defaults()
    
    def _load_settings(self):
        """Load settings from file or return empty dict."""
        config_path = Path.home() / '.kart_rush' / 'settings.json'
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _apply_defaults(self):
        """Apply default settings for missing keys."""
        for category, defaults in self.DEFAULT_SETTINGS.items():
            if category not in self._settings:
                self._settings[category] = {}
            for key, value in defaults.items():
                if key not in self._settings[category]:
                    self._settings[category][key] = value
    
    def save(self):
        """Save current settings to file."""
        config_path = Path.home() / '.kart_rush'
        config_path.mkdir(parents=True, exist_ok=True)
        settings_file = config_path / 'settings.json'
        try:
            with open(settings_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save settings: {e}")
    
    def get(self, category, key, default=None):
        """Get a specific setting value."""
        return self._settings.get(category, {}).get(key, default)
    
    def set(self, category, key, value):
        """Set a specific setting value."""
        if category not in self._settings:
            self._settings[category] = {}
        self._settings[category][key] = value
        self.save()
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self._settings = {}
        self._apply_defaults()
        self.save()
    
    @property
    def graphics(self):
        return self._settings.get('graphics', {})
    
    @property
    def audio(self):
        return self._settings.get('audio', {})
    
    @property
    def gameplay(self):
        return self._settings.get('gameplay', {})
    
    @property
    def controls(self):
        return self._settings.get('controls', {})
