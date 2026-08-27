"""
Kart Rush - Settings System
Manages game settings with real-time effects.
"""

from src.core.save import load, save

DEFAULT_SETTINGS = {
    "master_volume": 1.0,
    "music_volume": 0.8,
    "sfx_volume": 1.0,
    "quality": "medium",  # low, medium, high
    "camera_distance": 2,  # 0=near, 1=mid, 2=far
    "screen_shake": True
}

QUALITY_PRESETS = {
    "low": {
        "shadow_quality": 0,
        "particle_count": 50,
        "prop_density": 0.3,
        "pixel_ratio": 1.0,
        "anti_aliasing": False
    },
    "medium": {
        "shadow_quality": 1,
        "particle_count": 150,
        "prop_density": 0.6,
        "pixel_ratio": 1.0,
        "anti_aliasing": False
    },
    "high": {
        "shadow_quality": 2,
        "particle_count": 300,
        "prop_density": 1.0,
        "pixel_ratio": 1.5,
        "anti_aliasing": True
    }
}


class SettingsManager:
    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()
    
    def load(self):
        """Load settings from save."""
        save_data = load()
        saved_settings = save_data.get("settings", {})
        for key, value in saved_settings.items():
            if key in self.settings:
                self.settings[key] = value
    
    def save(self):
        """Save current settings."""
        save_data = load()
        save_data["settings"] = self.settings
        save(save_data)
    
    def get(self, key):
        return self.settings.get(key, DEFAULT_SETTINGS.get(key))
    
    def set(self, key, value):
        if key in self.settings:
            self.settings[key] = value
            self.save()
            return True
        return False
    
    def get_quality_preset(self, quality=None):
        if quality is None:
            quality = self.settings["quality"]
        return QUALITY_PRESETS.get(quality, QUALITY_PRESETS["medium"])
    
    def reset_to_defaults(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.save()
    
    def validate(self):
        """Validate settings are within acceptable ranges."""
        valid = True
        
        # Volume ranges
        for vol_key in ["master_volume", "music_volume", "sfx_volume"]:
            if not (0.0 <= self.settings.get(vol_key, 0) <= 1.0):
                print(f"Invalid {vol_key}: {self.settings.get(vol_key)}")
                self.settings[vol_key] = DEFAULT_SETTINGS[vol_key]
                valid = False
        
        # Quality level
        if self.settings.get("quality") not in QUALITY_PRESETS:
            print(f"Invalid quality: {self.settings.get('quality')}")
            self.settings["quality"] = "medium"
            valid = False
        
        # Camera distance
        if not (0 <= self.settings.get("camera_distance", 0) <= 2):
            print(f"Invalid camera_distance: {self.settings.get('camera_distance')}")
            self.settings["camera_distance"] = 2
            valid = False
        
        return valid
