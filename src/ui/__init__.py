"""
UI Components for Kart Rush
"""

from ursina import *


class MenuButton(Button):
    """Styled button for menu screens."""
    
    def __init__(self, text="", on_click=None, y=0, **kwargs):
        super().__init__(
            text=text,
            color=color.rgba(100, 100, 100, 200),
            highlight_color=color.rgba(150, 150, 150, 255),
            press_color=color.rgba(80, 80, 80, 255),
            scale=(0.3, 0.06),
            position=(0, y),
            on_click=on_click,
            **kwargs
        )
        self.original_scale = self.scale
    
    def mouse_enter(self):
        self.scale = (self.original_scale[0] * 1.05, self.original_scale[1] * 1.05)
    
    def mouse_exit(self):
        self.scale = self.original_scale


class TitleText(Text):
    """Styled title text for screens."""
    
    def __init__(self, text="", y=0, scale=1.5, **kwargs):
        super().__init__(
            text=text,
            origin=(0, 0),
            position=(0, y),
            scale=scale,
            color=color.rgb(255, 200, 50),
            **kwargs
        )


class HUDText(Text):
    """Text element for HUD display."""
    
    def __init__(self, text="", position=(0, 0), scale=1, color=color.white, **kwargs):
        super().__init__(
            text=text,
            position=position,
            scale=scale,
            color=color,
            origin=(0, 0),
            **kwargs
        )
