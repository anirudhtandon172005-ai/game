"""
Time Trial Scene for Kart Rush
"""

from ursina import *
from src.ui import MenuButton, TitleText


class TimeTrialScene:
    """Time trial mode scene."""
    
    def __init__(self, scene_manager, game_manager):
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        
        # Background
        self.bg = Entity(
            model='quad',
            color=color.rgb(30, 30, 50),
            scale=(2, 1.5),
            z=10
        )
        scene_manager.register_entity('bg', self.bg)
        
        # Title
        self.title = TitleText("TIME TRIAL", y=0.35, scale=1.5)
        scene_manager.register_entity('title', self.title)
        
        # Info text
        self.info_text = Text(
            text="Race against the clock!\nNo opponents, just pure speed.",
            origin=(0, 0),
            position=(0, 0.15),
            scale=0.9,
            color=color.light_gray
        )
        scene_manager.register_entity('info', self.info_text)
        
        # Best times section
        self.best_times_title = Text(
            text="BEST LAP TIMES",
            position=(-0.5, 0.02),
            scale=0.8,
            color=color.yellow,
            origin=(0, 0)
        )
        scene_manager.register_entity('best_times_title', self.best_times_title)
        
        # Display best times for each track
        tracks = ['sunset_coast', 'neon_city', 'jungle_ruins', 'volcano_run']
        track_names = {
            'sunset_coast': 'Sunset Coast',
            'neon_city': 'Neon City',
            'jungle_ruins': 'Jungle Ruins',
            'volcano_run': 'Volcano Run'
        }
        
        for i, track_id in enumerate(tracks):
            y_pos = -0.05 - i * 0.06
            best_time = self.game_manager.save_system.get_best_lap_time(track_id)
            
            time_str = "--:--"
            if best_time and best_time > 0:
                minutes = int(best_time // 60)
                seconds = best_time % 60
                time_str = f"{minutes}:{seconds:.2f}"
            
            track_text = Text(
                text=f"{track_names[track_id]}: {time_str}",
                position=(-0.3, y_pos),
                scale=0.7,
                color=color.white,
                origin=(0, 0)
            )
            scene_manager.register_entity(f'best_time_{i}', track_text)
        
        # Buttons
        self.start_btn = MenuButton(
            "SELECT TRACK",
            y=-0.35,
            on_click=self.select_track
        )
        scene_manager.register_entity('btn_start', self.start_btn)
        
        self.back_btn = MenuButton(
            "BACK",
            y=-0.42,
            on_click=self.go_back
        )
        scene_manager.register_entity('btn_back', self.back_btn)
        
        print("Time Trial scene initialized")
    
    def select_track(self):
        """Go to track selection for time trial."""
        self.game_manager.set_race_mode('time_trial')
        self.scene_manager.go_to_track_selection()
    
    def go_back(self):
        """Return to main menu."""
        self.scene_manager.go_to_main_menu()
    
    def destroy(self):
        pass
