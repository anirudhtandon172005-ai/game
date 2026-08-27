"""
Kart Rush - Main Game Controller
Implements simulation/render split for deterministic QA testing.
Manages all game systems: karts, race, track, input, state.
"""

from panda3d.core import ClockObject
from direct.showbase.ShowBase import ShowBase

from src.core.state import GameState
from src.core.input import InputSystem
from src.game.kart import Kart


class FPSCounter:
    """Rolling FPS calculator."""
    
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.frame_times = []
        self.fps = 60.0
    
    def accumulate(self, dt):
        """Add a frame time and update rolling FPS."""
        if dt <= 0:
            return
        
        fps = 1.0 / dt
        self.frame_times.append(fps)
        
        # Keep only last N frames
        if len(self.frame_times) > self.window_size:
            self.frame_times.pop(0)
        
        # Calculate average
        self.fps = sum(self.frame_times) / len(self.frame_times)
    
    def get_fps(self):
        """Get current rolling FPS."""
        return self.fps


class Game(ShowBase):
    """
    Main game class with simulate/render separation.
    
    Usage:
        Normal: game = Game(); game.start_realtime_loop()
        QA:     game = Game(); harness.install(game); run_qa_suite()
    """
    
    def __init__(self):
        super().__init__()
        
        # Disable default mouse movement
        self.disableMouse()
        
        # Set up clock for fixed timestep
        self.clock = ClockObject()
        
        # Core systems
        self.state = GameState()
        self.input_system = InputSystem(self)
        
        # Game objects
        self.player = None
        self.ai_karts = []
        self.all_karts = []
        
        # Track/Race data
        self.current_track = None
        self.track_data = None
        
        # Timing
        self.dt = 1.0 / 60.0
        self.fixed_timestep = 1.0 / 60.0
        self.accumulator = 0.0
        
        # QA mode flag
        self.qa_mode = False
        
        # Frame counter for determinism
        self.frame_count = 0
        
        # FPS counter for debug overlay
        self.fps_counter = FPSCounter()
        
        # Debug overlay reference (set by harness)
        self.debug_overlay_node = None
    
    def setup_scene(self):
        """Set up the basic scene (called once at startup)."""
        # Set background color
        self.setBackgroundColor(0.5, 0.7, 1.0)
        
        # Add ambient light
        from panda3d.core import AmbientLight
        ambient = AmbientLight('ambient')
        ambient.setColor((0.6, 0.6, 0.6, 1))
        self.ambient_light = self.render.attachNewNode(ambient)
        self.render.setLight(self.ambient_light)
        
        # Add directional light (sun)
        from panda3d.core import DirectionalLight
        sun = DirectionalLight('sun')
        sun.setColor((1, 1, 0.9, 1))
        self.sun_light = self.render.attachNewNode(sun)
        self.sun_light.setHpr(45, -45, 0)
        self.render.setLight(self.sun_light)
        
        # Create simple ground plane
        from panda3d.core import GeomNode, Geom, GeomVertexFormat, GeomVertexData
        from panda3d.core import GeomVertexWriter, GeomTriangles
        from panda3d.core import NodePath
        
        # Simple colored plane for now
        from panda3d.core import CardMaker
        cm = CardMaker('ground')
        cm.setFrame(-100, 100, -100, 100)
        cm.setColor(0.2, 0.6, 0.2, 1)
        self.ground = self.render.attachNewNode(cm.generate())
        self.ground.setR(90)
        self.ground.setZ(-0.1)
    
    def start_race(self, track_id='sunset_coast', num_ai=3, autopilot=False):
        """
        Start a race on the specified track.
        
        Args:
            track_id: Track identifier
            num_ai: Number of AI opponents
            autopilot: If True, player kart uses AI controls (for QA)
        """
        # Reset state
        self.state.reset()
        self.state.set('LOADING')
        
        # Clear existing karts
        self.all_karts.clear()
        self.ai_karts.clear()
        self.player = None
        
        # Load track data (placeholder for now)
        self.current_track = track_id
        self.track_data = self._get_track_data(track_id)
        
        # Create player kart at starting position
        start_pos = self.track_data.get('start_position', (0, 0, 80))
        start_rot = self.track_data.get('start_rotation', 0)
        
        self.player = Kart(position=start_pos)
        self.player.rotation = start_rot
        self.player.autopilot = autopilot
        self.all_karts.append(self.player)
        
        # Create AI karts
        for i in range(num_ai):
            ai = Kart(position=start_pos)
            ai.rotation = start_rot + (i + 1) * 5  # Staggered start
            ai.is_ai = True
            ai.difficulty = ['rookie', 'cautious', 'balanced', 'aggressive'][i % 4]
            self.ai_karts.append(ai)
            self.all_karts.append(ai)
        
        # Set up camera
        self.setup_camera()
        
        # Start countdown
        self.state.set('COUNTDOWN')
    
    def _get_track_data(self, track_id):
        """Get track data from Track system."""
        from src.game.track import create_test_track
        
        # Create procedural track
        track = create_test_track()
        
        # Find start position (first checkpoint)
        start_cp = track.get_checkpoint_at_index(0)
        start_pos = start_cp['position'] if start_cp else (0, 0, 80)
        start_tangent = start_cp['tangent'] if start_cp else (0, 0, 1)
        
        # Calculate rotation from tangent
        import math
        start_rot = math.degrees(math.atan2(start_tangent[0], start_tangent[2]))
        
        return {
            'track': track,
            'start_position': (start_pos[0], start_pos[1], start_pos[2]),
            'start_rotation': start_rot,
            'checkpoints': [cp['position'] for cp in track.checkpoints],
            'laps_to_finish': 3
        }
    
    def setup_camera(self):
        """Set up follow camera."""
        if self.player:
            self.camera.setPos(self.player.position[0], 
                              self.player.position[1] + 5, 
                              self.player.position[2] + 3)
            self.camera.lookAt(self.player.position[0],
                              self.player.position[1],
                              self.player.position[2])
    
    def simulate(self, dt):
        """
        Pure simulation step - no rendering.
        Updates: input, physics, AI, race state.
        """
        self.frame_count += 1
        
        # Get input
        input_state = self.input_system.get_state()
        
        # Handle pause
        if input_state.get('pause'):
            if self.state.current == 'RACING':
                self.state.set('PAUSED')
            elif self.state.current == 'PAUSED':
                self.state.set('RACING')
            return  # Skip simulation while paused
        
        # Handle countdown
        if self.state.is_counting_down():
            self.state.countdown_timer -= dt
            if self.state.countdown_timer <= 0:
                self.state.set('RACING')
            return  # No control during countdown
        
        # Update player
        if self.player and self.state.is_racing():
            # Get surface under kart
            if self.track_data and 'track' in self.track_data:
                track = self.track_data['track']
                surface = track.surface_at(self.player.position)
            else:
                surface = None
            
            if getattr(self.player, 'autopilot', False):
                # Simple autopilot for QA
                input_state = {'forward': True, 'backward': False, 
                              'left': False, 'right': False, 
                              'drift': False, 'boost': False}
            
            self.player.set_input(input_state)
            self.player.update(dt, surface)
            
            # Update camera to follow player
            if not self.qa_mode:
                self.update_camera(dt)
        
        # Update AI
        for ai in self.ai_karts:
            if self.state.is_racing():
                # Get surface under AI kart
                if self.track_data and 'track' in self.track_data:
                    track = self.track_data['track']
                    surface = track.surface_at(ai.position)
                else:
                    surface = None
                
                ai.set_input({'forward': True, 'backward': False,
                             'left': False, 'right': False,
                             'drift': False, 'boost': False})
                ai.update(dt, surface)
        
        # Update race timer
        if self.state.current == 'RACING':
            self.state.race_timer += dt
    
    def render(self):
        """Pure render step - called by Panda3D's task manager."""
        # Camera and visual updates happen here
        pass
    
    def update_camera(self, dt):
        """Update camera to follow player."""
        if not self.player:
            return
        
        import math
        pos = self.player.position
        rad = math.radians(self.player.rotation)
        
        # Calculate camera position behind kart
        cam_dist = 8
        cam_height = 3
        
        target_x = pos[0] - math.sin(rad) * cam_dist
        target_y = pos[2] - math.cos(rad) * cam_dist  # Z is forward in Panda3D
        target_z = pos[1] + cam_height
        
        # Smooth lerp
        lerp_factor = 5.0 * dt
        current_pos = self.camera.getPos()
        
        new_x = current_pos[0] + (target_x - current_pos[0]) * lerp_factor
        new_y = current_pos[2] + (target_y - current_pos[2]) * lerp_factor  # Y/Z swap
        new_z = current_pos[1] + (target_z - current_pos[1]) * lerp_factor
        
        self.camera.setPos(new_x, new_z, new_y)
        self.camera.lookAt(pos[0], pos[1] + 5, pos[2])
    
    def start_realtime_loop(self):
        """Start the normal realtime game loop."""
        self.setup_scene()
        self.taskMgr.add(self._realtime_tick, 'realtime_tick')
    
    def _realtime_tick(self, task):
        """Main game loop tick."""
        dt = globalClock.getDt()
        dt = min(dt, 0.1)  # Cap delta time
        
        # Update FPS counter
        self.fps_counter.accumulate(dt)
        
        # Update debug overlay if present
        if self.debug_overlay_node and hasattr(self, 'qa_harness'):
            self.qa_harness._update_debug_overlay(dt)
        
        self.simulate(dt)
        # Render is handled by Panda3D automatically
        
        return task.cont
    
    def reset(self):
        """Full game reset for restart."""
        self.state.reset()
        self.input_system.reset()
        self.all_karts.clear()
        self.ai_karts.clear()
        self.player = None
        self.frame_count = 0
    
    def snap(self):
        """Return game state snapshot for QA."""
        return {
            'state': self.state.current,
            'countdown': self.state.countdown_timer,
            'race_time': self.state.race_timer,
            'player': self.player.snap() if self.player else None,
            'ai': [ai.snap() for ai in self.ai_karts],
            'frame_count': self.frame_count
        }
