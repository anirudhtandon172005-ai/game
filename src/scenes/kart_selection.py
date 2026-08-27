"""
Kart Selection Scene for Kart Rush
"""

from ursina import *
from src.ui import MenuButton, TitleText


class KartSelection:
    """Kart selection screen with preview and stats."""
    
    KART_DATA = {
        'kart_default': {
            'name': 'Standard Kart',
            'speed': 7,
            'handling': 7,
            'acceleration': 7,
            'weight': 5,
            'color': color.blue,
        },
        'kart_speed': {
            'name': 'Speed Racer',
            'speed': 10,
            'handling': 4,
            'acceleration': 6,
            'weight': 4,
            'color': color.red,
        },
        'kart_heavy': {
            'name': 'Heavy Hitter',
            'speed': 6,
            'handling': 5,
            'acceleration': 4,
            'weight': 10,
            'color': color.orange,
        },
        'kart_balanced': {
            'name': 'Balanced Pro',
            'speed': 7,
            'handling': 8,
            'acceleration': 7,
            'weight': 6,
            'color': color.green,
        },
    }
    
    def __init__(self, scene_manager, game_manager):
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        self.current_kart_index = 0
        self.kart_list = list(self.KART_DATA.keys())
        
        # Background
        self.bg = Entity(
            model='quad',
            color=color.rgb(30, 30, 50),
            scale=(2, 1.5),
            z=10
        )
        scene_manager.register_entity('bg', self.bg)
        
        # Title
        self.title = TitleText("SELECT KART", y=0.35, scale=1.5)
        scene_manager.register_entity('title', self.title)
        
        # Kart preview area
        self.preview_area = Entity(
            model='quad',
            color=color.rgba(0, 0, 0, 100),
            scale=(0.6, 0.4),
            position=(0, 0.05),
            z=5
        )
        scene_manager.register_entity('preview', self.preview_area)
        
        # Kart name display
        self.kart_name_text = Text(
            text="",
            origin=(0, 0),
            position=(0, -0.18),
            scale=1.2,
            color=color.white
        )
        scene_manager.register_entity('kart_name', self.kart_name_text)
        
        # Stats bars
        self.stat_bars = {}
        stat_labels = ['Speed', 'Handling', 'Accel', 'Weight']
        stat_keys = ['speed', 'handling', 'acceleration', 'weight']
        
        for i, (label, key) in enumerate(zip(stat_labels, stat_keys)):
            y_pos = 0.05 - (i + 1) * 0.08
            
            # Label
            label_text = Text(
                text=label,
                position=(-0.25, y_pos + 0.015),
                scale=0.7,
                color=color.light_gray,
                origin=(0, 0)
            )
            scene_manager.register_entity(f'stat_label_{key}', label_text)
            
            # Bar background
            bar_bg = Entity(
                model='quad',
                color=color.dark_gray,
                scale=(0.3, 0.04),
                position=(0.1, y_pos),
                z=4
            )
            scene_manager.register_entity(f'stat_bar_bg_{key}', bar_bg)
            
            # Bar fill
            bar_fill = Entity(
                model='quad',
                color=color.cyan,
                scale=(0.3, 0.04),
                position=(0.1, y_pos),
                origin=(-0.5, 0),
                z=4.1
            )
            scene_manager.register_entity(f'stat_bar_{key}', bar_fill)
            self.stat_bars[key] = bar_fill
        
        # Navigation buttons
        self.prev_btn = MenuButton(
            "< Previous",
            y=-0.35,
            on_click=self.previous_kart
        )
        scene_manager.register_entity('btn_prev', self.prev_btn)
        
        self.next_btn = MenuButton(
            "Next >",
            y=-0.35,
            on_click=self.next_kart
        )
        self.next_btn.position = (0.25, -0.35)
        scene_manager.register_entity('btn_next', self.next_btn)
        
        self.select_btn = MenuButton(
            "SELECT",
            y=-0.42,
            on_click=self.select_kart
        )
        scene_manager.register_entity('btn_select', self.select_btn)
        
        self.back_btn = MenuButton(
            "BACK",
            y=-0.49,
            on_click=self.go_back
        )
        scene_manager.register_entity('btn_back', self.back_btn)
        
        # Lock indicator
        self.locked_text = Text(
            text="LOCKED",
            origin=(0, 0),
            position=(0, -0.28),
            scale=1,
            color=color.red,
            enabled=False
        )
        scene_manager.register_entity('locked', self.locked_text)
        
        # Update display
        self.update_display()
        
        print("Kart Selection initialized")
    
    def get_current_kart_id(self):
        return self.kart_list[self.current_kart_index]
    
    def update_display(self):
        """Update the kart display with current selection."""
        kart_id = self.get_current_kart_id()
        kart_data = self.KART_DATA[kart_id]
        
        # Update name
        self.kart_name_text.text = kart_data['name']
        
        # Update stats
        for key in ['speed', 'handling', 'acceleration', 'weight']:
            value = kart_data[key]
            ratio = value / 10.0
            bar = self.stat_bars[key]
            bar.scale_x = 0.3 * ratio
            bar.color = kart_data['color']
        
        # Check if locked
        is_unlocked = self.game_manager.save_system.has_unlock('karts', kart_id)
        self.locked_text.enabled = not is_unlocked
        
        if is_unlocked:
            self.select_btn.color = color.rgba(100, 200, 100, 200)
        else:
            self.select_btn.color = color.rgba(100, 100, 100, 100)
    
    def previous_kart(self):
        self.current_kart_index = (self.current_kart_index - 1) % len(self.kart_list)
        self.update_display()
    
    def next_kart(self):
        self.current_kart_index = (self.current_kart_index + 1) % len(self.kart_list)
        self.update_display()
    
    def select_kart(self):
        kart_id = self.get_current_kart_id()
        if self.game_manager.save_system.has_unlock('karts', kart_id):
            self.game_manager.select_kart(kart_id)
            print(f"Selected kart: {kart_id}")
            self.scene_manager.go_to_track_selection()
        else:
            print(f"Kart {kart_id} is locked!")
    
    def go_back(self):
        self.scene_manager.go_to_main_menu()
    
    def destroy(self):
        pass
