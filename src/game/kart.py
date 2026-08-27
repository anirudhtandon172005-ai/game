"""
Kart Rush - Kart Physics Entity
Stat-driven handling with drift, boost, and surface detection.
Implements simulation/update separate from rendering.
"""

from panda3d.core import Vec3, Point3, Quat


# Base kart stats - variants override these
KART_STATS = {
    'maxSpeed': 60.0,
    'accel': 22.0,
    'brake': 34.0,
    'reverseMax': 18.0,
    'friction': 10.0,
    'turn': 2.6,
    'highSpeedSteerCut': 0.55,
    'grip': 1.0,
    'offroadGrip': 0.5,
    'offroadSpeedMul': 0.45,
    'airControl': 0.35,
    'gravity': -30.0,
    'driftTurnMult': 1.5,
    'driftFrictionMult': 0.15,
    'boostMult': 1.5,
}


class Kart:
    def __init__(self, position=(0, 0, 0), stats_override=None):
        # Position/rotation
        self.position = Vec3(*position)
        self.rotation = 0.0  # yaw in degrees
        self.velocity = Vec3(0, 0, 0)
        self.speed = 0.0
        
        # Stats
        self.stats = {**KART_STATS, **(stats_override or {})}
        
        # State flags
        self.is_drifting = False
        self.is_airborne = False
        self.is_boosting = False
        
        # Drift system
        self.drift_time = 0.0
        self.drift_tier = 0
        self.boost_time = 0.0
        
        # Timers
        self.stuck_timer = 0.0
        self.offtrack_timer = 0.0
        self.flipped_timer = 0.0
        
        # Lap/race state
        self.lap = 1
        self.track_t = 0.0  # 0-1 progress along track
        self.checkpoint_index = 0
        self.finished = False
        self.finish_time = 0.0
        
        # Input state (set by input system)
        self.input_state = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'drift': False,
            'boost': False
        }
    
    def reset(self, position=(0, 0, 0), rotation=0):
        """Full reset for restart."""
        self.position = Vec3(*position)
        self.rotation = rotation
        self.velocity = Vec3(0, 0, 0)
        self.speed = 0.0
        self.is_drifting = False
        self.is_airborne = False
        self.is_boosting = False
        self.drift_time = 0.0
        self.drift_tier = 0
        self.boost_time = 0.0
        self.stuck_timer = 0.0
        self.offtrack_timer = 0.0
        self.flipped_timer = 0.0
        self.lap = 1
        self.track_t = 0.0
        self.checkpoint_index = 0
        self.finished = False
        self.finish_time = 0.0
    
    def set_input(self, input_state):
        self.input_state = input_state
    
    def update(self, dt, track_surface=None):
        """
        Simulate kart physics.
        track_surface: dict with 'on_road', 'dist_from_center', 'tangent' if available
        """
        # Handle boost
        if self.boost_time > 0:
            self.boost_time -= dt
            if self.boost_time <= 0:
                self.is_boosting = False
        
        # Get effective speed limit
        speed_limit = self.stats['maxSpeed']
        if self.is_boosting:
            speed_limit *= self.stats['boostMult']
        
        # Surface check
        on_road = True
        if track_surface:
            on_road = track_surface.get('on_road', True)
            if not on_road:
                speed_limit *= self.stats['offroadSpeedMul']
        
        # Steering effectiveness (reduced at high speed)
        steer_factor = 1.0
        if self.speed > 15:
            t = min(1.0, (self.speed - 15) / (speed_limit - 15)) if speed_limit > 15 else 1.0
            steer_factor = 1.0 - t * (1.0 - self.stats['highSpeedSteerCut'])
        
        # Air control
        if self.is_airborne:
            steer_factor *= self.stats['airControl']
        
        # Apply steering
        steer_input = 0.0
        if self.input_state['left']:
            steer_input = -1.0
        elif self.input_state['right']:
            steer_input = 1.0
        
        if steer_input != 0 and not self.is_airborne:
            turn_rate = self.stats['turn'] * steer_factor
            if self.is_drifting:
                turn_rate *= self.stats['driftTurnMult']
            self.rotation += steer_input * turn_rate * dt * (self.speed / max(1, self.stats['maxSpeed']))
        
        # Acceleration / braking
        accel = self.stats['accel']
        brake = self.stats['brake']
        
        if self.input_state['forward']:
            if self.speed < speed_limit:
                self.speed += accel * dt
                if self.is_boosting:
                    self.speed += accel * 0.5 * dt
        elif self.input_state['backward']:
            if self.speed > 0:
                self.speed -= brake * dt
                if self.speed < 0:
                    self.speed = -self.stats['reverseMax']
            else:
                self.speed -= accel * 0.5 * dt
                if self.speed < -self.stats['reverseMax']:
                    self.speed = -self.stats['reverseMax']
        else:
            # Friction
            friction = self.stats['friction']
            if self.is_drifting:
                friction *= self.stats['driftFrictionMult']
            if not on_road:
                friction *= self.stats['offroadGrip']
            
            if self.speed > 0:
                self.speed -= friction * dt
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += friction * dt
                if self.speed > 0:
                    self.speed = 0
        
        # Clamp speed
        if self.speed > speed_limit:
            self.speed = speed_limit
        elif self.speed < -self.stats['reverseMax']:
            self.speed = -self.stats['reverseMax']
        
        # Calculate velocity vector from rotation and speed
        import math
        rad = math.radians(self.rotation)
        forward = Vec3(math.sin(rad), 0, math.cos(rad))
        
        # Lateral slide during drift
        if self.is_drifting and not self.is_airborne:
            lateral_magnitude = self.speed * 0.3 * dt
            if steer_input != 0:
                lateral_dir = Vec3(math.cos(rad), 0, -math.sin(rad)) * steer_input
                self.position += lateral_dir * lateral_magnitude
        
        # Apply velocity
        self.velocity = forward * self.speed
        self.position += self.velocity * dt
        
        # Gravity if airborne
        if self.is_airborne:
            self.position += Vec3(0, self.stats['gravity'] * dt, 0)
        
        # Drift logic
        self._update_drift(dt, steer_input, self.speed)
        
        # Stuck detection
        self._update_stuck_detection(dt, self.input_state['forward'], on_road)
    
    def _update_drift(self, dt, steer_input, speed):
        """Update drift state and charging."""
        if self.input_state['drift'] and speed > 15 and steer_input != 0 and not self.is_airborne:
            if not self.is_drifting:
                self.is_drifting = True
                self.drift_time = 0.0
                # Small hop
                self.position += Vec3(0, 2.0, 0)
            
            self.drift_time += dt
            
            # Update tier
            if self.drift_time >= 3.2:
                self.drift_tier = 3
            elif self.drift_time >= 2.0:
                self.drift_tier = 2
            elif self.drift_time >= 1.0:
                self.drift_tier = 1
        else:
            # Release drift
            if self.is_drifting and self.drift_tier > 0:
                # Grant boost
                boost_durations = [0, 1.0, 1.8, 2.6]
                self.boost_time = boost_durations[self.drift_tier]
                self.is_boosting = True
            
            self.is_drifting = False
            self.drift_time = 0.0
            self.drift_tier = 0
    
    def _update_stuck_detection(self, dt, moving_forward, on_road):
        """Detect stuck/off-track/flipped conditions."""
        if moving_forward and self.speed < 2 and on_road:
            self.stuck_timer += dt
        else:
            self.stuck_timer = 0.0
        
        if not on_road:
            self.offtrack_timer += dt
        else:
            self.offtrack_timer = 0.0
        
        # Flipped detection (simplified - needs up-vector check in render)
        # This is a placeholder for the full implementation
    
    def needs_respawn(self):
        """Check if kart needs to be respawned."""
        return (self.stuck_timer > 3.5 or 
                self.offtrack_timer > 3.5 or 
                self.flipped_timer > 3.5)
    
    def apply_boost(self, duration=1.6):
        """Apply item boost."""
        self.boost_time = duration
        self.is_boosting = True
    
    def get_progress_score(self):
        """Calculate progress score for position determination."""
        return self.lap * 1000 + self.checkpoint_index * 100
    
    def snap(self):
        """Return snapshot of current state for QA."""
        return {
            'pos': [self.position[0], self.position[1], self.position[2]],
            'speed': self.speed,
            'rotation': self.rotation,
            'lap': self.lap,
            'track_t': self.track_t,
            'checkpoint_index': self.checkpoint_index,
            'is_drifting': self.is_drifting,
            'drift_tier': self.drift_tier,
            'boost_time': self.boost_time,
            'is_boosting': self.is_boosting,
            'is_airborne': self.is_airborne,
            'progress': self.get_progress_score()
        }
