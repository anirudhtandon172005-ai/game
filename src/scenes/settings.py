"""
Settings Scene for Kart Rush
"""

from ursina import *
from src.ui import MenuButton, TitleText


class SettingsScene:
    """Settings screen for game configuration."""
    
    def __init__(self, scene_manager, game_manager):
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        self.settings = game_manager.settings
        
        # Background
        self.bg = Entity(
            model='quad',
            color=color.rgb(30, 30, 50),
            scale=(2, 1.5),
            z=10
        )
        scene_manager.register_entity('bg', self.bg)
        
        # Title
        self.title = TitleText("SETTINGS", y=0.35, scale=1.5)
        scene_manager.register_entity('title', self.title)
        
        # Audio settings section
        self.audio_title = Text(
            text="AUDIO",
            position=(-0.6, 0.2),
            scale=1,
            color=color.yellow,
            origin=(0, 0)
        )
        scene_manager.register_entity('audio_title', self.audio_title)
        
        # Master volume slider placeholder
        self.master_vol_text = Text(
            text=f"Master Volume: {int(self.settings.get('audio', 'master_volume', 0.8) * 100)}%",
            position=(-0.4, 0.12),
            scale=0.7,
            color=color.white
        )
        scene_manager.register_entity('master_vol', self.master_vol_text)
        
        # Music volume
        self.music_vol_text = Text(
            text=f"Music Volume: {int(self.settings.get('audio', 'music_volume', 0.6) * 100)}%",
            position=(-0.4, 0.06),
            scale=0.7,
            color=color.white
        )
        scene_manager.register_entity('music_vol', self.music_vol_text)
        
        # SFX volume
        self.sfx_vol_text = Text(
            text=f"SFX Volume: {int(self.settings.get('audio', 'sfx_volume', 0.8) * 100)}%",
            position=(-0.4, 0.0),
            scale=0.7,
            color=color.white
        )
        scene_manager.register_entity('sfx_vol', self.sfx_vol_text)
        
        # Graphics settings section
        self.graphics_title = Text(
            text="GRAPHICS",
            position=(-0.6, -0.1),
            scale=1,
            color=color.yellow,
            origin=(0, 0)
        )
        scene_manager.register_entity('graphics_title', self.graphics_title)
        
        # Fullscreen toggle info
        fullscreen = "ON" if self.settings.get('graphics', 'fullscreen', False) else "OFF"
        self.fullscreen_text = Text(
            text=f"Fullscreen: {fullscreen}",
            position=(-0.4, -0.18),
            scale=0.7,
            color=color.white
        )
        scene_manager.register_entity('fullscreen', self.fullscreen_text)
        
        # Gameplay settings section
        self.gameplay_title = Text(
            text="GAMEPLAY",
            position=(-0.6, -0.28),
            scale=1,
            color=color.yellow,
            origin=(0, 0)
        )
        scene_manager.register_entity('gameplay_title', self.gameplay_title)
        
        # Camera shake toggle
        cam_shake = "ON" if self.settings.get('gameplay', 'camera_shake', True) else "OFF"
        self.cam_shake_text = Text(
            text=f"Camera Shake: {cam_shake}",
            position=(-0.4, -0.36),
            scale=0.7,
            color=color.white
        )
        scene_manager.register_entity('cam_shake', self.cam_shake_text)
        
        # Buttons
        self.apply_btn = MenuButton(
            "APPLY",
            y=-0.45,
            on_click=self.apply_settings
        )
        scene_manager.register_entity('btn_apply', self.apply_btn)
        
        self.back_btn = MenuButton(
            "BACK",
            y=-0.52,
            on_click=self.go_back
        )
        scene_manager.register_entity('btn_back', self.back_btn)
        
        print("Settings scene initialized")
    
    def apply_settings(self):
        """Apply and save settings."""
        self.settings.save()
        print("Settings saved!")
    
    def go_back(self):
        """Return to main menu."""
        self.scene_manager.go_to_main_menu()
    
    def destroy(self):
        pass
