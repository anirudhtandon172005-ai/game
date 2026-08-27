"""
Title Text Component for Kart Rush
"""

from ursina import *


class TitleText(Text):
    """
    Styled title text for screens.
    """
    
    def __init__(self, text="", y=0, scale=1.5, **kwargs):
        super().__init__(
            text=text,
            origin=(0, 0),
            position=(0, y),
            scale=scale,
            color=color.rgb(255, 200, 50),
            font='Proxima Nova',
            **kwargs
        )
        
        # Add glow effect using a shadow
        self.shadow = Text(
            text=text,
            origin=(0, 0),
            position=(0.02, y - 0.02),
            scale=scale,
            color=color.rgba(0, 0, 0, 100),
            z=1
        )
    
    def destroy(self):
        """Clean up shadow."""
        if hasattr(self, 'shadow') and self.shadow:
            destroy(self.shadow)
        super().destroy()
