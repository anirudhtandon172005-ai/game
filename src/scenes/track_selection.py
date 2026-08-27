"""
Track Selection Scene for Kart Rush
"""

from ursina import *
from src.ui import MenuButton, TitleText


class TrackSelection:
    """Track selection screen with preview."""
    
    TRACK_DATA = {
        'sunset_coast': {
            'name': 'Sunset Coast',
            'difficulty': 'Easy',
            'laps': 3,
            'description': 'A scenic coastal track at sunset',
            'color': color.rgb(255, 150, 50),
        },
        'neon_city': {
            'name': 'Neon City',
            'difficulty': 'Medium',
            'laps': 3,
            'description': 'High-speed urban circuit',
            'color': color.rgb(0, 200, 255),
        },
        'jungle_ruins': {
            'name': 'Jungle Ruins',
            'difficulty': 'Hard',
            'laps': 3,
            'description': 'Dangerous jungle pathway',
            'color': color.rgb(50, 180, 50),
        },
        'volcano_run': {
            'name': 'Volcano Run',
            'difficulty': 'Expert',
            'laps': 3,
            'description': 'Extreme volcanic terrain',
            'color': color.rgb(255, 50, 0),
        },
    }
    
    def __init__(self, scene_manager, game_manager):
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        self.current_track_index = 0
        self.track_list = list(self.TRACK_DATA.keys())
        
        # Background
        self.bg = Entity(
            model='quad',
            color=color.rgb(30, 30, 50),
            scale=(2, 1.5),
            z=10
        )
        scene_manager.register_entity('bg', self.bg)
        
        # Title
        self.title = TitleText("SELECT TRACK", y=0.35, scale=1.5)
        scene_manager.register_entity('title', self.title)
        
        # Track preview area
        self.preview_area = Entity(
            model='quad',
            color=color.rgba(0, 0, 0, 100),
            scale=(0.7, 0.45),
            position=(0, 0.05),
            z=5
        )
        scene_manager.register_entity('preview', self.preview_area)
        
        # Track name display
        self.track_name_text = Text(
            text="",
            origin=(0, 0),
            position=(0, -0.2),
            scale=1.3,
            color=color.white
        )
        scene_manager.register_entity('track_name', self.track_name_text)
        
        # Track info
        self.track_info_text = Text(
            text="",
            origin=(0, 0),
            position=(0, -0.26),
            scale=0.8,
            color=color.light_gray
        )
        scene_manager.register_entity('track_info', self.track_info_text)
        
        # Difficulty and laps
        self.difficulty_text = Text(
            text="",
            position=(-0.3, -0.32),
            scale=0.9,
            color=color.yellow
        )
        scene_manager.register_entity('difficulty', self.difficulty_text)
        
        self.laps_text = Text(
            text="",
            position=(0.3, -0.32),
            scale=0.9,
            color=color.cyan
        )
        scene_manager.register_entity('laps', self.laps_text)
        
        # Navigation buttons
        self.prev_btn = MenuButton(
            "< Previous",
            y=-0.40,
            on_click=self.previous_track
        )
        scene_manager.register_entity('btn_prev', self.prev_btn)
        
        self.next_btn = MenuButton(
            "Next >",
            y=-0.40,
            on_click=self.next_track
        )
        self.next_btn.position = (0.25, -0.40)
        scene_manager.register_entity('btn_next', self.next_btn)
        
        self.select_btn = MenuButton(
            "START RACE",
            y=-0.47,
            on_click=self.start_race
        )
        scene_manager.register_entity('btn_select', self.select_btn)
        
        self.back_btn = MenuButton(
            "BACK",
            y=-0.54,
            on_click=self.go_back
        )
        scene_manager.register_entity('btn_back', self.back_btn)
        
        # Lock indicator
        self.locked_text = Text(
            text="LOCKED",
            origin=(0, 0),
            position=(0, -0.32),
            scale=1,
            color=color.red,
            enabled=False
        )
        scene_manager.register_entity('locked', self.locked_text)
        
        # Update display
        self.update_display()
        
        print("Track Selection initialized")
    
    def get_current_track_id(self):
        return self.track_list[self.current_track_index]
    
    def update_display(self):
        """Update the track display with current selection."""
        track_id = self.get_current_track_id()
        track_data = self.TRACK_DATA[track_id]
        
        # Update name
        self.track_name_text.text = track_data['name']
        self.track_name_text.color = track_data['color']
        
        # Update info
        self.track_info_text.text = track_data['description']
        
        # Update difficulty and laps
        self.difficulty_text.text = f"Difficulty: {track_data['difficulty']}"
        self.difficulty_text.color = track_data['color']
        
        self.laps_text.text = f"Laps: {track_data['laps']}"
        
        # Check if locked
        is_unlocked = self.game_manager.save_system.has_unlock('tracks', track_id)
        self.locked_text.enabled = not is_unlocked
        
        if is_unlocked:
            self.select_btn.color = color.rgba(100, 200, 100, 200)
            self.select_btn.enabled = True
        else:
            self.select_btn.color = color.rgba(100, 100, 100, 100)
            self.select_btn.enabled = False
    
    def previous_track(self):
        self.current_track_index = (self.current_track_index - 1) % len(self.track_list)
        self.update_display()
    
    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.track_list)
        self.update_display()
    
    def start_race(self):
        track_id = self.get_current_track_id()
        if self.game_manager.save_system.has_unlock('tracks', track_id):
            self.game_manager.select_track(track_id)
            print(f"Starting race on: {track_id}")
            
            # Determine mode
            mode = self.game_manager.race_mode
            
            if mode == 'championship':
                # Get championship race index
                race_idx = self.game_manager.championship_race_index
                expected_track = self.game_manager.get_championship_race(race_idx)
                if expected_track != track_id:
                    print(f"Championship requires: {expected_track}")
                    return
            
            self.scene_manager.start_race(track_id=track_id)
        else:
            print(f"Track {track_id} is locked!")
    
    def go_back(self):
        self.scene_manager.go_to_main_menu()
    
    def destroy(self):
        pass
