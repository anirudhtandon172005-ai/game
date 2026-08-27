"""
KART RUSH - TRACK SYSTEM
Core infrastructure for track creation, checkpoints, racing lines, and world building.
"""

from ursina import *
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import math

@dataclass
class Checkpoint:
    """A checkpoint that racers must pass through in order."""
    id: int
    position: Vec3
    direction: Vec3  # Normal vector pointing along the track
    width: float = 10.0
    next_checkpoint_id: Optional[int] = None
    respawn_point: Optional[Vec3] = None
    respawn_rotation: Optional[Vec3] = None
    trigger_entity: Optional[Entity] = None
    
    def get_bounds(self) -> Tuple[Vec3, Vec3]:
        """Get the left and right bounds of the checkpoint."""
        perpendicular = Vec3(-self.direction.z, 0, self.direction.x).normalized()
        left = self.position - perpendicular * (self.width / 2)
        right = self.position + perpendicular * (self.width / 2)
        return left, right
    
    def is_passed(self, kart_position: Vec3) -> bool:
        """Check if a kart has passed this checkpoint."""
        left, right = self.get_bounds()
        # Check if kart is within the checkpoint bounds
        to_kart = kart_position - self.position
        projection = dot(to_kart, self.direction)
        lateral = dot(to_kart, Vec3(-self.direction.z, 0, self.direction.x))
        
        return abs(lateral) < (self.width / 2) and projection > -2

@dataclass
class RacingWaypoint:
    """A waypoint on the AI racing line."""
    position: Vec3
    target_speed: float = 100.0
    brake_point: bool = False
    apex: bool = False
    acceleration_zone: bool = False
    drift_zone: bool = False
    overtaking_zone: bool = False
    defensive_zone: bool = False

@dataclass
class TrackSection:
    """A section of the track with specific characteristics."""
    name: str
    start_checkpoint: int
    end_checkpoint: int
    section_type: str  # 'straight', 'sweeper', 'hairpin', 'chicane', 'jump', 'shortcut'
    difficulty: int  # 1-5
    overtaking_opportunity: bool = False
    hazard_zone: bool = False
    boost_zone: bool = False
    powerup_zone: bool = False

@dataclass
class Shortcut:
    """A shortcut route on the track."""
    name: str
    entry_checkpoint: int
    exit_checkpoint: int
    is_major: bool = True
    risk_level: int = 3  # 1-5
    time_saved_if_successful: float = 3.0  # seconds
    penalty_if_failed: float = 5.0  # seconds lost

@dataclass
class Hazard:
    """A dynamic or static hazard on the track."""
    position: Vec3
    hazard_type: str  # 'oil', 'rock', 'moving_obstacle', 'lava', 'water', 'mud'
    radius: float = 2.0
    damage: float = 0.0
    slowdown_factor: float = 0.5
    duration: float = 0.0  # 0 = permanent
    warning_distance: float = 10.0
    entity: Optional[Entity] = None

@dataclass
class PowerUpZone:
    """A zone where power-ups can spawn."""
    position: Vec3
    radius: float = 3.0
    respawn_time: float = 5.0
    max_items: int = 1
    preferred_items: List[str] = field(default_factory=list)
    entity: Optional[Entity] = None
    respawn_timer: float = 0.0

@dataclass
class RespawnPoint:
    """A safe location to respawn a kart."""
    position: Vec3
    rotation: Vec3
    checkpoint_id: int
    is_safe: bool = True

@dataclass
class TrackDesign:
    """Complete design document for a track."""
    name: str
    theme: str
    difficulty: str  # 'easy', 'medium', 'hard', 'expert'
    target_lap_time: float  # seconds
    total_laps: int = 3
    track_length: float = 0.0  # meters
    average_speed: float = 0.0  # km/h
    num_corners: int = 0
    num_hairpins: int = 0
    num_sweepers: int = 0
    num_chicanes: int = 0
    num_jumps: int = 0
    num_shortcuts: int = 0
    elevation_range: float = 0.0  # meters
    
    checkpoints: List[Checkpoint] = field(default_factory=list)
    racing_line: List[RacingWaypoint] = field(default_factory=list)
    sections: List[TrackSection] = field(default_factory=list)
    shortcuts: List[Shortcut] = field(default_factory=list)
    hazards: List[Hazard] = field(default_factory=list)
    powerup_zones: List[PowerUpZone] = field(default_factory=list)
    respawn_points: List[RespawnPoint] = field(default_factory=list)
    
    start_position: Vec3 = Vec3(0, 0, 0)
    start_rotation: Vec3 = Vec3(0, 0, 0)
    finish_position: Vec3 = Vec3(0, 0, 0)
    
    # Visual settings
    time_of_day: str = "day"
    weather: str = "clear"
    color_palette: List[Color] = field(default_factory=list)
    primary_landmark: str = ""
    secondary_landmarks: List[str] = field(default_factory=list)


class TrackSystem(Entity):
    """Main track system manager."""
    
    def __init__(self, track_design: TrackDesign, **kwargs):
        super().__init__(**kwargs)
        self.design = track_design
        self.current_lap = 1
        self.total_laps = track_design.total_laps
        self.active_checkpoints = set()
        self.last_checkpoint_passed = -1
        self.racers = []
        self.powerup_entities = []
        self.hazard_entities = []
        
        self._setup_track()
    
    def _setup_track(self):
        """Initialize the track from design."""
        self._create_checkpoints()
        self._create_racing_line()
        self._create_powerup_zones()
        self._create_hazards()
        self._create_respawn_points()
    
    def _create_checkpoints(self):
        """Create visual checkpoint markers."""
        for checkpoint in self.design.checkpoints:
            # Create invisible trigger entity
            trigger = Entity(
                model='cube',
                scale=(checkpoint.width, 10, 2),
                position=checkpoint.position,
                rotation=(0, math.degrees(math.atan2(checkpoint.direction.x, checkpoint.direction.z)), 0),
                color=color.rgba(0, 255, 0, 50),
                collider='box',
                visible=False  # Invisible trigger
            )
            trigger.checkpoint_id = checkpoint.id
            checkpoint.trigger_entity = trigger
    
    def _create_racing_line(self):
        """Create visual racing line for debugging."""
        if not self.design.racing_line:
            return
        
        points = [wp.position for wp in self.design.racing_line]
        if len(points) > 1:
            self.racing_line_entity = Entity(
                model=Line(points, thickness=2),
                color=color.rgba(255, 255, 0, 100),
                visible=False  # Only for debugging
            )
    
    def _create_powerup_zones(self):
        """Create power-up spawn zones."""
        for zone in self.design.powerup_zones:
            # Create visual indicator
            indicator = Entity(
                model='sphere',
                scale=(zone.radius * 2, 1, zone.radius * 2),
                position=zone.position + Vec3(0, 0.5, 0),
                color=color.rgba(255, 215, 0, 100),
                texture='circle',
                visible=True
            )
            zone.entity = indicator
            zone.respawn_timer = 0.0
    
    def _create_hazards(self):
        """Create hazard entities."""
        for hazard in self.design.hazards:
            if hazard.hazard_type == 'oil':
                entity = Entity(
                    model='plane',
                    scale=(hazard.radius * 2, hazard.radius * 2),
                    position=hazard.position + Vec3(0, 0.01, 0),
                    color=color.rgba(0, 0, 0, 150),
                    rotation_x=90
                )
            elif hazard.hazard_type == 'lava':
                entity = Entity(
                    model='plane',
                    scale=(hazard.radius * 2, hazard.radius * 2),
                    position=hazard.position + Vec3(0, 0.01, 0),
                    color=color.rgba(255, 69, 0, 200),
                    rotation_x=90
                )
            else:
                entity = Entity(
                    model='sphere',
                    scale=(hazard.radius, hazard.radius, hazard.radius),
                    position=hazard.position,
                    color=color.red
                )
            
            hazard.entity = entity
    
    def _create_respawn_points(self):
        """Ensure respawn points are valid."""
        for point in self.design.respawn_points:
            # Verify the point is on solid ground
            if not self._is_safe_position(point.position):
                print(f"Warning: Unsafe respawn point at {point.position}")
    
    def _is_safe_position(self, position: Vec3) -> bool:
        """Check if a position is safe for respawning."""
        # Raycast down to check for ground
        hit_info = raycast(position, direction=Vec3(0, -1, 0), distance=5, ignore=[self, ])
        return hit_info.hit
    
    def check_checkpoint(self, racer, position: Vec3) -> Optional[int]:
        """Check if a racer has passed a checkpoint."""
        next_cp_id = self.last_checkpoint_passed + 1
        if next_cp_id >= len(self.design.checkpoints):
            next_cp_id = 0  # Loop back to start for new lap
        
        checkpoint = self.design.checkpoints[next_cp_id]
        
        if checkpoint.is_passed(position):
            self.last_checkpoint_passed = next_cp_id
            
            # Check for lap completion
            if next_cp_id == len(self.design.checkpoints) - 1:
                self.current_lap += 1
                if self.current_lap > self.total_laps:
                    return -1  # Race finished
            
            return next_cp_id
        
        return None
    
    def get_respawn_point(self, position: Vec3) -> RespawnPoint:
        """Get the best respawn point based on current position."""
        best_point = None
        min_distance = float('inf')
        
        for point in self.design.respawn_points:
            distance = distance_2d(position, point.position)
            if distance < min_distance:
                min_distance = distance
                best_point = point
        
        return best_point or self.design.respawn_points[0]
    
    def get_next_waypoint(self, current_position: Vec3, lookahead: int = 3) -> RacingWaypoint:
        """Get the next racing waypoint for AI."""
        if not self.design.racing_line:
            return None
        
        # Find closest waypoint
        min_dist = float('inf')
        closest_idx = 0
        
        for i, wp in enumerate(self.design.racing_line):
            dist = distance_3d(current_position, wp.position)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
        
        # Return waypoint ahead
        next_idx = (closest_idx + lookahead) % len(self.design.racing_line)
        return self.design.racing_line[next_idx]
    
    def update(self):
        """Update track systems."""
        # Update power-up respawns
        for zone in self.design.powerup_zones:
            if hasattr(zone, 'respawn_timer'):
                zone.respawn_timer -= time.dt
                if zone.respawn_timer <= 0:
                    # Respawn power-up
                    zone.respawn_timer = zone.respawn_time


# Helper functions
def distance_2d(a: Vec3, b: Vec3) -> float:
    """Calculate 2D distance (ignoring Y)."""
    return math.sqrt((a.x - b.x)**2 + (a.z - b.z)**2)

def distance_3d(a: Vec3, b: Vec3) -> float:
    """Calculate 3D distance."""
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)

def dot(a: Vec3, b: Vec3) -> float:
    """Dot product."""
    return a.x * b.x + a.y * b.y + a.z * b.z


if __name__ == '__main__':
    app = Ursina()
    
    # Test track
    test_design = TrackDesign(
        name="Test Track",
        theme="test",
        difficulty="easy",
        target_lap_time=90.0,
        checkpoints=[
            Checkpoint(id=0, position=Vec3(0, 0, 0), direction=Vec3(0, 0, 1), width=10),
            Checkpoint(id=1, position=Vec3(0, 0, 50), direction=Vec3(1, 0, 0), width=10),
            Checkpoint(id=2, position=Vec3(50, 0, 50), direction=Vec3(0, 0, -1), width=10),
            Checkpoint(id=3, position=Vec3(50, 0, 0), direction=Vec3(-1, 0, 0), width=10),
        ]
    )
    
    track = TrackSystem(test_design)
    
    EditorCamera()
    app.run()
