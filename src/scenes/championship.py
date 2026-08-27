"""
Championship Scene for Kart Rush
"""

from ursina import *
from src.ui import MenuButton, TitleText


class ChampionshipResults:
    """Championship final results display."""
    
    def __init__(self, scene_manager, game_manager, standings):
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        self.standings = standings or []
        
        # Background
        self.bg = Entity(
            model='quad',
            color=color.rgb(20, 20, 40),
            scale=(2, 1.5),
            z=10
        )
        scene_manager.register_entity('bg', self.bg)
        
        # Title
        self.title = TitleText("CHAMPIONSHIP RESULTS", y=0.38, scale=1.3)
        scene_manager.register_entity('title', self.title)
        
        # Standings list
        y_start = 0.2
        for i, (name, points) in enumerate(self.standings[:8]):
            y_pos = y_start - i * 0.06
            
            # Position
            pos_text = Text(
                text=f"{i+1}.",
                position=(-0.5, y_pos),
                scale=0.8,
                color=color.yellow if i == 0 else color.white,
                origin=(0, 0)
            )
            scene_manager.register_entity(f'stand_pos_{i}', pos_text)
            
            # Name
            name_display = name.replace('_', ' ').title()
            if name == 'player':
                name_display = 'YOU'
            name_text = Text(
                text=name_display,
                position=(-0.4, y_pos),
                scale=0.8,
                color=color.yellow if i == 0 else color.white,
                origin=(0, 0)
            )
            scene_manager.register_entity(f'stand_name_{i}', name_text)
            
            # Points
            points_text = Text(
                text=f"{points} pts",
                position=(0.3, y_pos),
                scale=0.8,
                color=color.cyan,
                origin=(0, 0)
            )
            scene_manager.register_entity(f'stand_pts_{i}', points_text)
        
        # Buttons
        self.menu_btn = MenuButton(
            "MAIN MENU",
            y=-0.35,
            on_click=self.go_to_menu
        )
        scene_manager.register_entity('btn_menu', self.menu_btn)
        
        print("Championship results shown")
    
    def go_to_menu(self):
        """Return to main menu."""
        self.scene_manager.go_to_main_menu()
    
    def destroy(self):
        pass
