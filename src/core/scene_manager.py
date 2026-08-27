"""
Scene Manager - Handles transitions between game scenes.
"""

from ursina import Scene


class SceneManager:
    """
    Manages scene transitions and lifecycle.
    Coordinates between different UI scenes and the race scene.
    """
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self._current_scene = None
        self._scene_entities = {}
    
    def transition_to(self, scene_class, *args, **kwargs):
        """
        Transition to a new scene.
        
        Args:
            scene_class: The class of the scene to create
            *args, **kwargs: Arguments to pass to the scene constructor
        """
        # Clean up current scene
        if self._current_scene:
            self.cleanup_scene()
        
        # Create new scene
        self._current_scene = scene_class(self, self.game_manager, *args, **kwargs)
        
        return self._current_scene
    
    def cleanup_scene(self):
        """Clean up entities from the current scene."""
        # Destroy all scene entities
        for entity_list in self._scene_entities.values():
            for entity in entity_list:
                if hasattr(entity, 'destroy'):
                    entity.destroy()
        self._scene_entities.clear()
        self._current_scene = None
    
    def register_entity(self, name, entity):
        """Register an entity for cleanup when scene changes."""
        if name not in self._scene_entities:
            self._scene_entities[name] = []
        self._scene_entities[name].append(entity)
    
    def unregister_entity(self, name, entity):
        """Unregister an entity from cleanup list."""
        if name in self._scene_entities:
            if entity in self._scene_entities[name]:
                self._scene_entities[name].remove(entity)
    
    @property
    def current_scene(self):
        return self._current_scene
    
    def go_to_main_menu(self):
        """Transition back to main menu."""
        from src.scenes.main_menu import MainMenu
        self.game_manager.go_to_main_menu()
        self.transition_to(MainMenu)
    
    def go_to_kart_selection(self):
        """Transition to kart selection screen."""
        from src.scenes.kart_selection import KartSelection
        self.game_manager.set_state('kart_selection')
        self.transition_to(KartSelection)
    
    def go_to_track_selection(self):
        """Transition to track selection screen."""
        from src.scenes.track_selection import TrackSelection
        self.game_manager.set_state('track_selection')
        self.transition_to(TrackSelection)
    
    def start_race(self, track_id=None, ai_count=7, laps=3):
        """Start a race on the specified track."""
        from src.scenes.race_scene import RaceScene
        self.game_manager.set_state('racing')
        
        track = track_id or self.game_manager.selected_track
        kart = self.game_manager.selected_kart or 'kart_default'
        
        scene = RaceScene(
            self,
            self.game_manager,
            track_id=track,
            player_kart=kart,
            ai_count=ai_count,
            laps=laps
        )
        self._current_scene = scene
        return scene
    
    def start_time_trial(self, track_id=None, laps=3):
        """Start a time trial on the specified track."""
        from src.scenes.race_scene import RaceScene
        self.game_manager.start_time_trial(track_id or self.game_manager.selected_track)
        self.game_manager.set_state('racing')
        
        track = track_id or self.game_manager.selected_track
        kart = self.game_manager.selected_kart or 'kart_default'
        
        scene = RaceScene(
            self,
            self.game_manager,
            track_id=track,
            player_kart=kart,
            ai_count=0,  # No AI in time trial
            laps=laps,
            is_time_trial=True
        )
        self._current_scene = scene
        return scene
    
    def show_results(self, results_data):
        """Show race results screen."""
        from src.scenes.results import ResultsScreen
        self.game_manager.set_state('results')
        self.transition_to(ResultsScreen, results_data)
    
    def show_championship_results(self, standings):
        """Show championship final results."""
        from src.scenes.championship import ChampionshipResults
        self.game_manager.set_state('championship')
        self.transition_to(ChampionshipResults, standings)
    
    def show_settings(self):
        """Show settings screen."""
        from src.scenes.settings import SettingsScene
        self.game_manager.set_state('settings')
        self.transition_to(SettingsScene)
