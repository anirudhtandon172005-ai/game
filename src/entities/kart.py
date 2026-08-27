"""
Kart Entity for Kart Rush
Player and AI controlled kart with physics.
"""

from ursina import *
import math


class Kart(Entity):
    """Base kart entity with physics and controls."""
    
    def __init__(self, position=(0, 0, 0), color=color.blue, 
                 speed=10, handling=7, acceleration=7, weight=5,
                 is_player=False, **kwargs):
        super().__init__(**kwargs)
        
        # Properties
        self.is_player = is_player
        self.kart_color = color
        
        # Physics parameters
        self.max_speed = speed * 1.5
        self.acceleration = acceleration * 0.8
        self.handling = handling * 0.03
        self.drag = 0.98
        self.brake_force = 15
        
        # State
        self.velocity = Vec3(0, 0, 0)
        self.speed = 0
        self.steering = 0
        self.throttle = 0
        self.is_drifting = False
        self.drift_boost = 0
        self.boost_active = False
        self.boost_timer = 0
        
        # Create kart model
        self.model = 'cube'
        self.scale = (0.8, 0.4, 1.2)
        self.position = position
        self.color = color
        
        # Add wheels
        self.wheels = []
        wheel_positions = [
            (-0.5, -0.2, 0.4),
            (0.5, -0.2, 0.4),
            (-0.5, -0.2, -0.4),
            (0.5, -0.2, -0.4),
        ]
        for pos in wheel_positions:
            wheel = Entity(
                parent=self,
                model='sphere',
                scale=0.3,
                color=color.dark_gray,
                position=pos
            )
            self.wheels.append(wheel)
        
        # Trail effect entity
        self.trail = Entity(
            parent=self,
            model='cube',
            scale=(0.1, 0.05, 0.1),
            color=color.rgba(100, 100, 100, 100),
            position=(0, -0.2, 0)
        )
        self.trail.visible = False
        
        # Collision box
        self.collider = BoxCollider(self, center=(0, 0, 0), size=self.scale)
        
        # Lap tracking
        self.current_lap = 0
        self.checkpoints_passed = []
        self.lap_times = []
        self.current_lap_start = 0
        self.finished = False
        self.finish_position = 0
        self.finish_time = 0
        
        # Item/Powerup
        self.current_item = None
        self.has_shield = False
        
        print(f"Kart created at {position}, player={is_player}")
    
    def update(self):
        """Update kart physics and movement."""
        if self.finished:
            return
        
        # Apply drag
        self.velocity *= self.drag
        
        # Apply velocity
        self.position += self.velocity * time.dt
        
        # Update speed value
        self.speed = length(self.velocity)
        
        # Handle boost
        if self.boost_active:
            self.boost_timer -= time.dt
            if self.boost_timer <= 0:
                self.boost_active = False
    
    def accelerate(self, amount):
        """Apply acceleration in forward direction."""
        forward = self.forward
        self.velocity += forward * amount * self.acceleration * time.dt
    
    def brake(self, amount):
        """Apply braking force."""
        if length(self.velocity) > 0.1:
            brake_dir = -normalized(self.velocity)
            self.velocity += brake_dir * amount * self.brake_force * time.dt
    
    def steer(self, amount):
        """Apply steering."""
        # Steering effectiveness depends on speed
        speed_factor = min(1.0, self.speed / 5)
        turn_amount = amount * self.handling * speed_factor * time.dt
        
        # Rotate kart
        self.rotation_y += turn_amount * 60
        
        # Add some lateral movement for arcade feel
        right = self.right
        self.velocity += right * turn_amount * 2
    
    def start_drift(self):
        """Initiate drift."""
        self.is_drifting = True
        self.drift_boost = 0
    
    def end_drift(self):
        """End drift and apply boost if earned."""
        self.is_drifting = False
        if self.drift_boost >= 3:
            # Apply boost
            self.activate_boost(2.0)
        self.drift_boost = 0
    
    def update_drift(self):
        """Update drift mechanics."""
        if self.is_drifting:
            self.drift_boost = min(self.drift_boost + time.dt * 0.5, 5)
    
    def activate_boost(self, duration=3.0):
        """Activate speed boost."""
        self.boost_active = True
        self.boost_timer = duration
        # Apply initial boost
        self.velocity += self.forward * 10
    
    def apply_boost_physics(self):
        """Apply boost speed modifier."""
        if self.boost_active:
            boost_multiplier = 1.5
            if length(self.velocity) > 0:
                target_velocity = normalized(self.velocity) * self.max_speed * boost_multiplier
                self.velocity = lerp(self.velocity, target_velocity, time.dt * 2)
    
    def reset(self, position, rotation=(0, 0, 0)):
        """Reset kart to starting position."""
        self.position = position
        self.rotation = rotation
        self.velocity = Vec3(0, 0, 0)
        self.speed = 0
        self.finished = False
        self.current_lap = 0
        self.checkpoints_passed = []
        self.lap_times = []
        self.current_item = None
        self.has_shield = False
    
    def record_checkpoint(self, checkpoint_id):
        """Record passing a checkpoint."""
        if checkpoint_id not in self.checkpoints_passed:
            self.checkpoints_passed.append(checkpoint_id)
    
    def complete_lap(self, time_seconds):
        """Record completed lap."""
        self.current_lap += 1
        self.lap_times.append(time_seconds)
        self.checkpoints_passed = []
        
        # Reset for next lap timer
        self.current_lap_start = 0
    
    def finish_race(self, position, total_time):
        """Mark kart as finished."""
        self.finished = True
        self.finish_position = position
        self.finish_time = total_time
