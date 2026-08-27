"""
Kart Rush - Input System
Handles keyboard input and simulated QA input for deterministic testing.
Supports both real-time and simulated (QA harness) input modes.
"""


class InputSystem:
    """
    Unified input system supporting:
    - Real keyboard input (normal gameplay)
    - Simulated input (QA harness deterministic testing)
    """
    
    def __init__(self, base=None):
        self.base = base
        self.simulated_mode = False
        self.simulated_state = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'drift': False,
            'boost': False,
            'pause': False
        }
        
        # Key bindings
        self.bindings = {
            'forward': ['w', 'arrow_up'],
            'backward': ['s', 'arrow_down'],
            'left': ['a', 'arrow_left'],
            'right': ['d', 'arrow_right'],
            'drift': ['space'],
            'boost': ['shift'],
            'pause': ['escape', 'p']
        }
    
    def set_simulated(self, **kwargs):
        """Set simulated input state for QA testing."""
        self.simulated_mode = True
        for key, value in kwargs.items():
            if key in self.simulated_state:
                self.simulated_state[key] = value
    
    def clear_simulated(self):
        """Clear simulated mode, return to real input."""
        self.simulated_mode = False
        self.simulated_state = {k: False for k in self.simulated_state}
    
    def get_state(self):
        """Get current input state (real or simulated)."""
        if self.simulated_mode:
            return self.simulated_state.copy()
        
        return {
            'forward': self._is_pressed('forward'),
            'backward': self._is_pressed('backward'),
            'left': self._is_pressed('left'),
            'right': self._is_pressed('right'),
            'drift': self._is_pressed('drift'),
            'boost': self._is_pressed('boost'),
            'pause': self._is_pressed('pause')
        }
    
    def _is_pressed(self, action):
        """Check if action is currently pressed."""
        if self.base is None:
            return False
        
        if not hasattr(self.base, 'mouseWatcherNode') or self.base.mouseWatcherNode is None:
            return False
        
        keys = self.bindings.get(action, [])
        for key in keys:
            try:
                if self.base.mouseWatcherNode.is_button_down(key):
                    return True
            except Exception:
                # Handle case where key name is invalid for this system
                pass
        return False
    
    def was_just_pressed(self, action):
        """Check if action was just pressed this frame (edge detection)."""
        # For QA harness, we'll implement edge detection in the game loop
        return self._is_pressed(action)
    
    def reset(self):
        """Reset input system."""
        self.simulated_mode = False
        self.simulated_state = {k: False for k in self.simulated_state}
