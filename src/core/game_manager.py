"""
Game Manager - Central coordinator for game state and systems.
"""

from enum import Enum


class GameState(Enum):
    """Enumeration of possible game states."""
    MAIN_MENU = "main_menu"
    KART_SELECTION = "kart_selection"
    TRACK_SELECTION = "track_selection"
    RACING = "racing"
    PAUSED = "paused"
    RESULTS = "results"
    CHAMPIONSHIP = "championship"
    TIME_TRIAL = "time_trial"
    SETTINGS = "settings"
    QUIT = "quit"


class GameManager:
    """
    Central manager for game state, mode selection, and coordination between systems.
    """
    
    def __init__(self, settings, save_system):
        self.settings = settings
        self.save_system = save_system
        self._current_state = GameState.MAIN_MENU
        self._previous_state = None
        
        # Current session data
        self._selected_kart = None
        self._selected_track = None
        self._race_mode = None  # 'quick_race', 'championship', 'time_trial'
        self._race_results = None
        
        # Championship state
        self._championship_races = []
        self._championship_points = {}
        self._championship_current_race = 0
    
    @property
    def current_state(self):
        return self._current_state
    
    @current_state.setter
    def current_state(self, value):
        self._previous_state = self._current_state
        self._current_state = value
    
    def set_state(self, state):
        """Transition to a new game state."""
        if isinstance(state, str):
            state = GameState(state)
        self.current_state = state
    
    def go_to_main_menu(self):
        """Return to main menu."""
        self._reset_session_data()
        self.current_state = GameState.MAIN_MENU
    
    def _reset_session_data(self):
        """Reset temporary session data when returning to menu."""
        self._selected_kart = None
        self._selected_track = None
        self._race_mode = None
        self._race_results = None
    
    # Kart Selection
    def select_kart(self, kart_id):
        """Select a kart for the next race."""
        if self.save_system.has_unlock('karts', kart_id):
            self._selected_kart = kart_id
            return True
        return False
    
    @property
    def selected_kart(self):
        return self._selected_kart
    
    @property
    def available_karts(self):
        """Get list of unlocked karts."""
        return self.save_system.data['unlocks'].get('karts', ['kart_default'])
    
    # Track Selection
    def select_track(self, track_id):
        """Select a track for the next race."""
        if self.save_system.has_unlock('tracks', track_id):
            self._selected_track = track_id
            return True
        return False
    
    @property
    def selected_track(self):
        return self._selected_track
    
    @property
    def available_tracks(self):
        """Get list of unlocked tracks."""
        return self.save_system.data['unlocks'].get('tracks', ['sunset_coast'])
    
    # Race Mode
    def set_race_mode(self, mode):
        """Set the current race mode."""
        self._race_mode = mode
    
    @property
    def race_mode(self):
        return self._race_mode
    
    # Results handling
    def record_race_complete(self, position, total_racers, lap_times=None):
        """Record race completion results."""
        self._race_results = {
            'position': position,
            'total_racers': total_racers,
            'lap_times': lap_times or [],
        }
        
        # Update save system
        self.save_system.record_race_result(position, total_racers, self._selected_track)
        
        # Record best lap time if available
        if lap_times:
            best_lap = min(lap_times)
            self.save_system.record_lap_time(self._selected_track, best_lap)
    
    @property
    def race_results(self):
        return self._race_results
    
    # Championship methods
    def start_championship(self):
        """Initialize championship mode."""
        self._race_mode = 'championship'
        self._championship_races = [
            'sunset_coast',
            'neon_city', 
            'jungle_ruins',
            'volcano_run'
        ]
        self._championship_points = {'player': 0}
        self._championship_current_race = 0
    
    def get_championship_race(self, index):
        """Get track for championship race at index."""
        if 0 <= index < len(self._championship_races):
            return self._championship_races[index]
        return None
    
    def record_championship_result(self, position, ai_points=None):
        """Record championship race result."""
        # Points system: 1st=15, 2nd=12, 3rd=10, 4th=8, 5th=6, 6th=5, 7th=4, 8th=3
        points_map = {1: 15, 2: 12, 3: 10, 4: 8, 5: 6, 6: 5, 7: 4, 8: 3}
        player_points = points_map.get(min(position, 8), 0)
        
        self._championship_points['player'] = self._championship_points.get('player', 0) + player_points
        
        if ai_points:
            for i, points in enumerate(ai_points):
                ai_key = f'ai_{i}'
                self._championship_points[ai_key] = self._championship_points.get(ai_key, 0) + points
        
        self._championship_current_race += 1
        
        # Check if championship is complete
        if self._championship_current_race >= len(self._championship_races):
            return True  # Championship complete
        return False
    
    def get_championship_standings(self):
        """Get current championship standings."""
        sorted_points = sorted(
            self._championship_points.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_points
    
    @property
    def championship_race_index(self):
        return self._championship_current_race
    
    # Time Trial methods
    def start_time_trial(self, track_id):
        """Start time trial mode on specified track."""
        self._race_mode = 'time_trial'
        self._selected_track = track_id
    
    def is_time_trial_active(self):
        """Check if time trial mode is active."""
        return self._race_mode == 'time_trial'
