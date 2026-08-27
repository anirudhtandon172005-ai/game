"""
Results Screen for Kart Rush
"""

from ursina import *
from src.ui import MenuButton, TitleText


class ResultsScreen:
    """Race results display."""
    
    def __init__(self, scene_manager, game_manager, results_data):
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        self.results = results_data or {}
        
        # Background
        self.bg = Entity(
            model='quad',
            color=color.rgb(20, 20, 40),
            scale=(2, 1.5),
            z=10
        )
        scene_manager.register_entity('bg', self.bg)
        
        # Title based on position
        position = self.results.get('position', 1)
        if position == 1:
            title_text = "VICTORY!"
            title_color = color.gold
        elif position <= 3:
            title_text = "PODIUM!"
            title_color = color.cyan
        else:
            title_text = "FINISHED"
            title_color = color.white
        
        self.title = TitleText(title_text, y=0.35, scale=1.8)
        self.title.color = title_color
        scene_manager.register_entity('title', self.title)
        
        # Position display
        self.position_text = Text(
            text=f"Position: {position}/{self.results.get('total_racers', 8)}",
            origin=(0, 0),
            position=(0, 0.2),
            scale=1.2,
            color=color.white
        )
        scene_manager.register_entity('position', self.position_text)
        
        # Time info
        total_time = self.results.get('total_time', 0)
        minutes = int(total_time // 60)
        seconds = total_time % 60
        self.time_text = Text(
            text=f"Total Time: {minutes}:{seconds:.2f}",
            origin=(0, 0),
            position=(0, 0.1),
            scale=0.9,
            color=color.light_gray
        )
        scene_manager.register_entity('time', self.time_text)
        
        # Best lap
        best_lap = self.results.get('best_lap', 0)
        if best_lap > 0:
            lap_min = int(best_lap // 60)
            lap_sec = best_lap % 60
            self.best_lap_text = Text(
                text=f"Best Lap: {lap_min}:{lap_sec:.2f}",
                origin=(0, 0),
                position=(0, 0.02),
                scale=0.8,
                color=color.yellow
            )
            scene_manager.register_entity('best_lap', self.best_lap_text)
        
        # Buttons
        self.retry_btn = MenuButton(
            "RACE AGAIN",
            y=-0.15,
            on_click=self.retry_race
        )
        scene_manager.register_entity('btn_retry', self.retry_btn)
        
        self.menu_btn = MenuButton(
            "MAIN MENU",
            y=-0.25,
            on_click=self.go_to_menu
        )
        scene_manager.register_entity('btn_menu', self.menu_btn)
        
        print(f"Results screen shown - Position: {position}")
    
    def retry_race(self):
        """Restart the race."""
        track = self.game_manager.selected_track
        kart = self.game_manager.selected_kart or 'kart_default'
        self.scene_manager.start_race(track_id=track, player_kart=kart)
    
    def go_to_menu(self):
        """Return to main menu."""
        self.scene_manager.go_to_main_menu()
    
    def destroy(self):
        pass
