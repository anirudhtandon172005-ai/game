"""
Main Menu Scene for Kart Rush
"""

from ursina import *
from src.ui.menu_button import MenuButton
from src.ui.title_text import TitleText


class MainMenu:
    """
    Main menu with options for different game modes.
    """
    
    def __init__(self, scene_manager, game_manager):
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        
        # Create background
        self.bg = Entity(
            model='quad',
            color=color.rgb(20, 20, 40),
            scale=(2, 1.5),
            z=10
        )
        scene_manager.register_entity('bg', self.bg)
        
        # Create title
        self.title = TitleText("KART RUSH", y=0.35, scale=2)
        scene_manager.register_entity('title', self.title)
        
        # Create menu buttons
        button_y_start = 0.15
        button_spacing = 0.12
        
        self.buttons = {}
        
        self.buttons['quick_race'] = MenuButton(
            "Quick Race",
            y=button_y_start,
            on_click=self.on_quick_race
        )
        scene_manager.register_entity('btn_quick', self.buttons['quick_race'])
        
        self.buttons['championship'] = MenuButton(
            "Championship",
            y=button_y_start - button_spacing,
            on_click=self.on_championship
        )
        scene_manager.register_entity('btn_champ', self.buttons['championship'])
        
        self.buttons['time_trial'] = MenuButton(
            "Time Trial",
            y=button_y_start - button_spacing * 2,
            on_click=self.on_time_trial
        )
        scene_manager.register_entity('btn_time', self.buttons['time_trial'])
        
        self.buttons['karts'] = MenuButton(
            "Karts",
            y=button_y_start - button_spacing * 3,
            on_click=self.on_karts
        )
        scene_manager.register_entity('btn_karts', self.buttons['karts'])
        
        self.buttons['tracks'] = MenuButton(
            "Tracks",
            y=button_y_start - button_spacing * 4,
            on_click=self.on_tracks
        )
        scene_manager.register_entity('btn_tracks', self.buttons['tracks'])
        
        self.buttons['settings'] = MenuButton(
            "Settings",
            y=button_y_start - button_spacing * 5,
            on_click=self.on_settings
        )
        scene_manager.register_entity('btn_settings', self.buttons['settings'])
        
        self.buttons['quit'] = MenuButton(
            "Quit",
            y=button_y_start - button_spacing * 6,
            on_click=self.on_quit
        )
        scene_manager.register_entity('btn_quit', self.buttons['quit'])
        
        # Version text
        self.version = Text(
            text="v1.0.0",
            position=(-0.95, -0.45),
            scale=0.7,
            color=color.rgba(255, 255, 255, 150)
        )
        scene_manager.register_entity('version', self.version)
        
        print("Main Menu initialized")
    
    def on_quick_race(self):
        """Handle quick race button click."""
        self.scene_manager.go_to_track_selection()
    
    def on_championship(self):
        """Handle championship button click."""
        self.game_manager.start_championship()
        self.scene_manager.go_to_track_selection()
    
    def on_time_trial(self):
        """Handle time trial button click."""
        self.scene_manager.go_to_track_selection()
    
    def on_karts(self):
        """Handle karts button click."""
        self.scene_manager.go_to_kart_selection()
    
    def on_tracks(self):
        """Handle tracks button click."""
        # For now, just show available tracks info
        tracks = self.game_manager.available_tracks
        print(f"Available tracks: {tracks}")
        # Could open a track preview/info screen here
    
    def on_settings(self):
        """Handle settings button click."""
        self.scene_manager.show_settings()
    
    def on_quit(self):
        """Handle quit button click."""
        application.exit()
    
    def destroy(self):
        """Clean up menu resources."""
        pass
