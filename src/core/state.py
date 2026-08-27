"""
Kart Rush - Core State Management
Manages game state machine: MENU → LOADING → COUNTDOWN → RACING → FINISHED → RESULTS → PAUSED
"""

class GameState:
    STATES = ['MENU', 'LOADING', 'COUNTDOWN', 'RACING', 'FINISHED', 'RESULTS', 'PAUSED']
    
    def __init__(self):
        self._current = 'MENU'
        self._previous = None
        self.countdown_timer = 0.0
        self.race_timer = 0.0
        self.paused = False
    
    @property
    def current(self):
        return self._current
    
    @property
    def previous(self):
        return self._previous
    
    def set(self, new_state):
        if new_state not in self.STATES:
            raise ValueError(f"Invalid state: {new_state}")
        self._previous = self._current
        self._current = new_state
        
        # Auto-reset timers on state changes
        if new_state == 'COUNTDOWN':
            self.countdown_timer = 3.0  # 3, 2, 1, GO
        elif new_state == 'RACING':
            self.race_timer = 0.0
        elif new_state == 'MENU':
            self.countdown_timer = 0.0
            self.race_timer = 0.0
    
    def is_racing(self):
        return self._current in ['RACING', 'FINISHED']
    
    def is_counting_down(self):
        return self._current == 'COUNTDOWN'
    
    def reset(self):
        self._current = 'MENU'
        self._previous = None
        self.countdown_timer = 0.0
        self.race_timer = 0.0
        self.paused = False
