"""
KART RUSH - SUNSET COAST TRACK
Track 1: Tropical coastal racing circuit during golden hour.

CORE FANTASY: FAST, SUNNY, EXPANSIVE, COLORFUL, DANGEROUS

ROUTE:
Start Grid → Beachfront Straight → Wide Sweeper → Resort Section → 
Cliff Hairpin → Lighthouse Road → Beach Jump → Pier Shortcut → 
Coastal Highway → Final Sweeper → Finish
"""

from ursina import *
from src.tracks.track_system import (
    TrackDesign, Checkpoint, RacingWaypoint, TrackSection, 
    Shortcut, Hazard, PowerUpZone, RespawnPoint, TrackSystem
)
import math


def create_sunset_coast_track() -> TrackDesign:
    """Create the complete Sunset Coast track design."""
    
    # Track design document
    track = TrackDesign(
        name="Sunset Coast",
        theme="tropical_beach",
        difficulty="easy",
        target_lap_time=90.0,  # 1.5 minutes per lap
        total_laps=3,
        track_length=2500.0,  # meters
        average_speed=100.0,  # km/h
        num_corners=12,
        num_hairpins=2,
        num_sweepers=3,
        num_chicanes=1,
        num_jumps=2,
        num_shortcuts=2,
        elevation_range=40.0,  # meters
        
        time_of_day="sunset",
        weather="clear",
        color_palette=[
            color.rgb(255, 140, 90),   # Sunset orange
            color.rgb(30, 144, 255),   # Ocean blue
            color.rgb(238, 213, 150),  # Sand
            color.rgb(34, 139, 34),    # Palm green
        ],
        primary_landmark="Lighthouse",
        secondary_landmarks=["Beach Resort", "Pier", "Cliff Mansion", "Ocean"]
    )
    
    # ============= CHECKPOINTS =============
    # Strategic checkpoints around the track
    track.checkpoints = [
        # Start/Finish line
        Checkpoint(
            id=0,
            position=Vec3(0, 0, 0),
            direction=Vec3(0, 0, 1),
            width=15.0,
            respawn_point=Vec3(-5, 0.5, 0),
            respawn_rotation=Vec3(0, 0, 0)
        ),
        # Beachfront straight - checkpoint 1
        Checkpoint(
            id=1,
            position=Vec3(0, 0, 80),
            direction=Vec3(0, 0, 1),
            width=12.0,
            respawn_point=Vec3(-5, 0.5, 70),
            respawn_rotation=Vec3(0, 0, 0)
        ),
        # Entry to wide sweeper - checkpoint 2
        Checkpoint(
            id=2,
            position=Vec3(30, 0, 120),
            direction=Vec3(1, 0, 0),
            width=14.0,
            respawn_point=Vec3(20, 0.5, 115),
            respawn_rotation=Vec3(0, 90, 0)
        ),
        # Mid-sweeper - checkpoint 3
        Checkpoint(
            id=3,
            position=Vec3(80, 0, 100),
            direction=Vec3(0, 0, -1),
            width=16.0,
            respawn_point=Vec3(75, 0.5, 110),
            respawn_rotation=Vec3(0, 90, 0)
        ),
        # Resort section - checkpoint 4
        Checkpoint(
            id=4,
            position=Vec3(100, 2, 60),
            direction=Vec3(0, 0, -1),
            width=10.0,
            respawn_point=Vec3(95, 2.5, 70),
            respawn_rotation=Vec3(0, 0, 0)
        ),
        # Cliff hairpin entry - checkpoint 5
        Checkpoint(
            id=5,
            position=Vec3(100, 5, 20),
            direction=Vec3(-1, 0, 0),
            width=12.0,
            respawn_point=Vec3(95, 5.5, 30),
            respawn_rotation=Vec3(0, -90, 0)
        ),
        # Cliff hairpin apex - checkpoint 6
        Checkpoint(
            id=6,
            position=Vec3(60, 8, 10),
            direction=Vec3(0, 0, 1),
            width=10.0,
            respawn_point=Vec3(65, 8.5, 5),
            respawn_rotation=Vec3(0, 90, 0)
        ),
        # Lighthouse road - checkpoint 7
        Checkpoint(
            id=7,
            position=Vec3(40, 10, 30),
            direction=Vec3(1, 0, 0),
            width=8.0,
            respawn_point=Vec3(40, 10.5, 25),
            respawn_rotation=Vec3(0, 90, 0)
        ),
        # Beach jump approach - checkpoint 8
        Checkpoint(
            id=8,
            position=Vec3(80, 5, 40),
            direction=Vec3(0, 0, -1),
            width=10.0,
            respawn_point=Vec3(75, 5.5, 45),
            respawn_rotation=Vec3(0, -90, 0)
        ),
        # Beach jump landing - checkpoint 9
        Checkpoint(
            id=9,
            position=Vec3(80, 1, 10),
            direction=Vec3(-1, 0, 0),
            width=12.0,
            respawn_point=Vec3(85, 1.5, 15),
            respawn_rotation=Vec3(0, -90, 0)
        ),
        # Pier shortcut entry - checkpoint 10
        Checkpoint(
            id=10,
            position=Vec3(40, 1, 0),
            direction=Vec3(-1, 0, 0),
            width=10.0,
            respawn_point=Vec3(45, 1.5, 5),
            respawn_rotation=Vec3(0, -90, 0)
        ),
        # Coastal highway - checkpoint 11
        Checkpoint(
            id=11,
            position=Vec3(0, 0, -40),
            direction=Vec3(0, 0, -1),
            width=14.0,
            respawn_point=Vec3(-5, 0.5, -35),
            respawn_rotation=Vec3(0, 180, 0)
        ),
        # Final sweeper - checkpoint 12
        Checkpoint(
            id=12,
            position=Vec3(-40, 0, -60),
            direction=Vec3(-1, 0, 0),
            width=16.0,
            respawn_point=Vec3(-35, 0.5, -55),
            respawn_rotation=Vec3(0, -90, 0)
        ),
        # Finish line approach - checkpoint 13
        Checkpoint(
            id=13,
            position=Vec3(-80, 0, -30),
            direction=Vec3(0, 0, 1),
            width=15.0,
            respawn_point=Vec3(-75, 0.5, -40),
            respawn_rotation=Vec3(0, 0, 0)
        ),
    ]
    
    # Set finish position
    track.finish_position = Vec3(0, 0, 10)
    
    # ============= RACING LINE WAYPOINTS =============
    # AI racing line with speed hints
    track.racing_line = [
        # Start straight
        RacingWaypoint(position=Vec3(0, 0, 10), target_speed=120.0),
        RacingWaypoint(position=Vec3(0, 0, 50), target_speed=140.0),
        RacingWaypoint(position=Vec3(0, 0, 90), target_speed=150.0),
        
        # Wide sweeper entry
        RacingWaypoint(position=Vec3(20, 0, 115), target_speed=130.0, brake_point=True),
        RacingWaypoint(position=Vec3(50, 0, 115), target_speed=110.0, drift_zone=True),
        RacingWaypoint(position=Vec3(80, 0, 110), target_speed=100.0, apex=True),
        
        # Sweeper exit
        RacingWaypoint(position=Vec3(95, 0, 90), target_speed=120.0, acceleration_zone=True),
        RacingWaypoint(position=Vec3(100, 2, 60), target_speed=130.0),
        
        # Cliff section
        RacingWaypoint(position=Vec3(100, 5, 30), target_speed=100.0, brake_point=True),
        RacingWaypoint(position=Vec3(90, 7, 15), target_speed=80.0, drift_zone=True),
        RacingWaypoint(position=Vec3(60, 8, 10), target_speed=70.0, apex=True),
        
        # Lighthouse road
        RacingWaypoint(position=Vec3(40, 10, 20), target_speed=90.0, acceleration_zone=True),
        RacingWaypoint(position=Vec3(50, 8, 35), target_speed=110.0),
        
        # Beach jump approach
        RacingWaypoint(position=Vec3(70, 6, 40), target_speed=130.0),
        RacingWaypoint(position=Vec3(80, 5, 35), target_speed=140.0),
        
        # Jump
        RacingWaypoint(position=Vec3(80, 3, 20), target_speed=150.0),
        RacingWaypoint(position=Vec3(80, 1, 5), target_speed=120.0),
        
        # Pier area
        RacingWaypoint(position=Vec3(60, 1, 0), target_speed=100.0),
        RacingWaypoint(position=Vec3(40, 1, 0), target_speed=110.0, overtaking_zone=True),
        
        # Coastal highway
        RacingWaypoint(position=Vec3(10, 0, -10), target_speed=140.0),
        RacingWaypoint(position=Vec3(0, 0, -40), target_speed=150.0),
        
        # Final sweeper
        RacingWaypoint(position=Vec3(-20, 0, -55), target_speed=130.0, brake_point=True),
        RacingWaypoint(position=Vec3(-50, 0, -60), target_speed=100.0, drift_zone=True),
        RacingWaypoint(position=Vec3(-75, 0, -50), target_speed=110.0, apex=True),
        
        # Finish straight
        RacingWaypoint(position=Vec3(-80, 0, -20), target_speed=140.0, acceleration_zone=True),
        RacingWaypoint(position=Vec3(-60, 0, 5), target_speed=150.0, overtaking_zone=True),
        RacingWaypoint(position=Vec3(-20, 0, 10), target_speed=160.0),
    ]
    
    # ============= TRACK SECTIONS =============
    track.sections = [
        TrackSection(
            name="Beachfront Straight",
            start_checkpoint=0,
            end_checkpoint=2,
            section_type="straight",
            difficulty=1,
            overtaking_opportunity=True,
            boost_zone=True
        ),
        TrackSection(
            name="Wide Sweeper",
            start_checkpoint=2,
            end_checkpoint=4,
            section_type="sweeper",
            difficulty=2,
            overtaking_opportunity=True,
            powerup_zone=True
        ),
        TrackSection(
            name="Resort Section",
            start_checkpoint=4,
            end_checkpoint=5,
            section_type="straight",
            difficulty=1,
            hazard_zone=False
        ),
        TrackSection(
            name="Cliff Hairpin",
            start_checkpoint=5,
            end_checkpoint=7,
            section_type="hairpin",
            difficulty=4,
            overtaking_opportunity=True,
            powerup_zone=True
        ),
        TrackSection(
            name="Lighthouse Road",
            start_checkpoint=7,
            end_checkpoint=8,
            section_type="straight",
            difficulty=2,
            hazard_zone=False
        ),
        TrackSection(
            name="Beach Jump",
            start_checkpoint=8,
            end_checkpoint=10,
            section_type="jump",
            difficulty=3,
            boost_zone=True
        ),
        TrackSection(
            name="Pier Shortcut Zone",
            start_checkpoint=10,
            end_checkpoint=11,
            section_type="shortcut",
            difficulty=3,
            overtaking_opportunity=True
        ),
        TrackSection(
            name="Coastal Highway",
            start_checkpoint=11,
            end_checkpoint=12,
            section_type="straight",
            difficulty=1,
            boost_zone=True,
            powerup_zone=True
        ),
        TrackSection(
            name="Final Sweeper",
            start_checkpoint=12,
            end_checkpoint=13,
            section_type="sweeper",
            difficulty=2,
            overtaking_opportunity=True
        ),
    ]
    
    # ============= SHORTCUTS =============
    track.shortcuts = [
        # Major shortcut: Pier route
        Shortcut(
            name="Pier Shortcut",
            entry_checkpoint=9,
            exit_checkpoint=11,
            is_major=True,
            risk_level=3,
            time_saved_if_successful=4.0,
            penalty_if_failed=6.0
        ),
        # Minor shortcut: Beach path
        Shortcut(
            name="Beach Path",
            entry_checkpoint=1,
            exit_checkpoint=3,
            is_major=False,
            risk_level=2,
            time_saved_if_successful=2.0,
            penalty_if_failed=3.0
        ),
    ]
    
    # ============= HAZARDS =============
    track.hazards = [
        # Beach sand slowdown zones
        Hazard(
            position=Vec3(20, 0.1, 100),
            hazard_type="sand",
            radius=5.0,
            slowdown_factor=0.7
        ),
        Hazard(
            position=Vec3(70, 0.1, 90),
            hazard_type="sand",
            radius=4.0,
            slowdown_factor=0.7
        ),
        # Cliff edge danger zone
        Hazard(
            position=Vec3(110, 5, 15),
            hazard_type="cliff",
            radius=3.0,
            damage=0.0
        ),
        # Pier water hazard
        Hazard(
            position=Vec3(30, 0.5, -5),
            hazard_type="water",
            radius=8.0,
            slowdown_factor=0.3
        ),
    ]
    
    # ============= POWER-UP ZONES =============
    track.powerup_zones = [
        PowerUpZone(
            position=Vec3(15, 0.5, 85),
            radius=3.0,
            respawn_time=5.0,
            preferred_items=["boost", "oil", "shield"]
        ),
        PowerUpZone(
            position=Vec3(85, 0.5, 105),
            radius=3.0,
            respawn_time=5.0,
            preferred_items=["rocket", "boost", "magnet"]
        ),
        PowerUpZone(
            position=Vec3(70, 8.5, 12),
            radius=3.0,
            respawn_time=5.0,
            preferred_items=["shield", "turbo", "lightning"]
        ),
        PowerUpZone(
            position=Vec3(80, 1.5, 25),
            radius=3.0,
            respawn_time=5.0,
            preferred_items=["boost", "oil", "rocket"]
        ),
        PowerUpZone(
            position=Vec3(10, 0.5, -45),
            radius=3.0,
            respawn_time=5.0,
            preferred_items=["lightning", "boost", "shield"]
        ),
        PowerUpZone(
            position=Vec3(-60, 0.5, -55),
            radius=3.0,
            respawn_time=5.0,
            preferred_items=["rocket", "magnet", "turbo"]
        ),
    ]
    
    # ============= RESPAWN POINTS =============
    track.respawn_points = [
        RespawnPoint(position=Vec3(-5, 0.5, 0), rotation=Vec3(0, 0, 0), checkpoint_id=0),
        RespawnPoint(position=Vec3(-5, 0.5, 70), rotation=Vec3(0, 0, 0), checkpoint_id=1),
        RespawnPoint(position=Vec3(20, 0.5, 115), rotation=Vec3(0, 90, 0), checkpoint_id=2),
        RespawnPoint(position=Vec3(75, 0.5, 110), rotation=Vec3(0, 90, 0), checkpoint_id=3),
        RespawnPoint(position=Vec3(95, 2.5, 70), rotation=Vec3(0, 0, 0), checkpoint_id=4),
        RespawnPoint(position=Vec3(95, 5.5, 30), rotation=Vec3(0, -90, 0), checkpoint_id=5),
        RespawnPoint(position=Vec3(65, 8.5, 5), rotation=Vec3(0, 90, 0), checkpoint_id=6),
        RespawnPoint(position=Vec3(40, 10.5, 25), rotation=Vec3(0, 90, 0), checkpoint_id=7),
        RespawnPoint(position=Vec3(75, 5.5, 45), rotation=Vec3(0, -90, 0), checkpoint_id=8),
        RespawnPoint(position=Vec3(85, 1.5, 15), rotation=Vec3(0, -90, 0), checkpoint_id=9),
        RespawnPoint(position=Vec3(45, 1.5, 5), rotation=Vec3(0, -90, 0), checkpoint_id=10),
        RespawnPoint(position=Vec3(-5, 0.5, -35), rotation=Vec3(0, 180, 0), checkpoint_id=11),
        RespawnPoint(position=Vec3(-35, 0.5, -55), rotation=Vec3(0, -90, 0), checkpoint_id=12),
        RespawnPoint(position=Vec3(-75, 0.5, -40), rotation=Vec3(0, 0, 0), checkpoint_id=13),
    ]
    
    return track


def build_sunset_coast_world(track_system: TrackSystem):
    """Build the visual world for Sunset Coast track."""
    
    # ============= TERRAIN & GROUND =============
    
    # Ocean base
    ocean = Entity(
        model='plane',
        scale=(1000, 1000),
        position=Vec3(0, -2, 0),
        color=color.rgb(30, 144, 255),
        texture='water',
        texture_scale=(50, 50),
        collider=None
    )
    
    # Beach sand
    beach = Entity(
        model='plane',
        scale=(300, 200),
        position=Vec3(50, 0.1, 50),
        rotation_x=90,
        color=color.rgb(238, 213, 150),
        texture='sand',
        collider=None
    )
    
    # Main road surface - beachfront section
    road_segments = []
    
    # Segment 1: Start straight
    road1 = Entity(
        model='cube',
        scale=(12, 0.5, 100),
        position=Vec3(0, 0.25, 50),
        color=color.rgb(100, 100, 100),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(road1)
    
    # Segment 2: Sweeper curve (approximated)
    road2 = Entity(
        model='cube',
        scale=(14, 0.5, 60),
        position=Vec3(60, 0.25, 110),
        rotation_y=-30,
        color=color.rgb(100, 100, 100),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(road2)
    
    # Segment 3: Resort section
    road3 = Entity(
        model='cube',
        scale=(10, 0.5, 50),
        position=Vec3(100, 2.25, 80),
        color=color.rgb(100, 100, 100),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(road3)
    
    # Segment 4: Cliff section
    road4 = Entity(
        model='cube',
        scale=(10, 0.5, 40),
        position=Vec3(80, 5.25, 30),
        rotation_y=-45,
        color=color.rgb(100, 100, 100),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(road4)
    
    # Segment 5: Lighthouse road
    road5 = Entity(
        model='cube',
        scale=(8, 0.5, 30),
        position=Vec3(50, 10.25, 25),
        rotation_y=90,
        color=color.rgb(100, 100, 100),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(road5)
    
    # Segment 6: Beach jump ramp
    ramp = Entity(
        model='cube',
        scale=(10, 1, 30),
        position=Vec3(80, 3, 30),
        rotation_x=-15,
        color=color.rgb(120, 120, 120),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(ramp)
    
    # Segment 7: Pier
    pier = Entity(
        model='cube',
        scale=(8, 0.5, 40),
        position=Vec3(20, 1.25, 0),
        color=color.rgb(139, 90, 43),
        texture='wood',
        collider='box'
    )
    road_segments.append(pier)
    
    # Segment 8: Coastal highway
    road8 = Entity(
        model='cube',
        scale=(14, 0.5, 80),
        position=Vec3(0, 0.25, -40),
        color=color.rgb(100, 100, 100),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(road8)
    
    # Segment 9: Final sweeper
    road9 = Entity(
        model='cube',
        scale=(16, 0.5, 50),
        position=Vec3(-60, 0.25, -60),
        rotation_y=20,
        color=color.rgb(100, 100, 100),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(road9)
    
    # Segment 10: Finish straight
    road10 = Entity(
        model='cube',
        scale=(15, 0.5, 60),
        position=Vec3(-80, 0.25, 0),
        rotation_y=90,
        color=color.rgb(100, 100, 100),
        texture='asphalt',
        collider='box'
    )
    road_segments.append(road10)
    
    # ============= LANDMARKS =============
    
    # Lighthouse
    lighthouse_base = Entity(
        model='cylinder',
        scale=(8, 15, 8),
        position=Vec3(30, 7.5, 30),
        color=color.white,
        texture='brick'
    )
    lighthouse_top = Entity(
        model='cylinder',
        scale=(4, 5, 4),
        position=Vec3(30, 18, 30),
        color=color.yellow
    )
    lighthouse_light = PointLight(
        position=Vec3(30, 20, 30),
        color=color.yellow,
        intensity=2
    )
    
    # Beach resort building
    resort = Entity(
        model='cube',
        scale=(30, 10, 20),
        position=Vec3(120, 5, 70),
        color=color.rgb(255, 248, 220),
        texture='stucco'
    )
    
    # Palm trees (simple)
    palm_positions = [
        Vec3(40, 0.5, 30),
        Vec3(60, 0.5, 80),
        Vec3(90, 0.5, 100),
        Vec3(-30, 0.5, 20),
        Vec3(-70, 0.5, -70),
    ]
    
    palms = []
    for pos in palm_positions:
        trunk = Entity(
            model='cylinder',
            scale=(1, 8, 1),
            position=pos,
            color=color.rgb(139, 90, 43)
        )
        leaves = Entity(
            model='sphere',
            scale=(6, 3, 6),
            position=pos + Vec3(0, 5, 0),
            color=color.rgb(34, 139, 34)
        )
        palms.append((trunk, leaves))
    
    # ============= START GRID =============
    
    # Starting positions for 8 karts
    grid_positions = []
    for i in range(8):
        row = i // 2
        col = i % 2
        x_offset = (col - 0.5) * 4
        z_offset = -row * 5
        grid_positions.append(Vec3(x_offset, 0.5, z_offset))
    
    # Start line marking
    start_line = Entity(
        model='plane',
        scale=(15, 2),
        position=Vec3(0, 0.01, -5),
        rotation_x=90,
        color=color.white
    )
    
    # Finish line marking (checkered pattern simulated)
    finish_line = Entity(
        model='plane',
        scale=(15, 2),
        position=Vec3(0, 0.01, 5),
        rotation_x=90,
        color=color.rgb(0, 0, 0)
    )
    
    # ============= BOUNDARIES & BARRIERS =============
    
    # Guardrails along cliff edges
    cliff_rail = Entity(
        model='cube',
        scale=(1, 1, 30),
        position=Vec3(115, 5, 20),
        color=color.rgb(200, 200, 200)
    )
    
    # Beach barriers
    beach_barrier = Entity(
        model='cube',
        scale=(100, 1, 1),
        position=Vec3(50, 0.5, 140),
        color=color.rgb(200, 150, 100)
    )
    
    # ============= DECORATIVE PROPS =============
    
    # Umbrellas on beach
    umbrella_positions = [
        Vec3(30, 0.5, 40),
        Vec3(50, 0.5, 60),
        Vec3(70, 0.5, 50),
    ]
    
    umbrellas = []
    for pos in umbrella_positions:
        pole = Entity(
            model='cylinder',
            scale=(0.3, 4, 0.3),
            position=pos,
            color=color.rgb(139, 90, 43)
        )
        canopy = Entity(
            model='cone',
            scale=(4, 1, 4),
            position=pos + Vec3(0, 2.5, 0),
            color=color.rgb(255, 100, 100)
        )
        umbrellas.append((pole, canopy))
    
    # ============= LIGHTING =============
    
    # Sun (directional light simulating sunset)
    sun = DirectionalLight(
        position=Vec3(-100, 50, -100),
        look_at=Vec3(0, 0, 0),
        color=color.rgb(255, 180, 100),
        intensity=1.5
    )
    
    # Ambient light
    ambient = AmbientLight(color=color.rgb(255, 200, 150))
    
    # Sky color (sunset)
    scene.sky.color = color.rgb(255, 140, 90)
    scene.sky.top_color = color.rgb(255, 100, 50)
    scene.sky.bottom_color = color.rgb(255, 200, 150)
    
    # ============= AUDIO ZONES =============
    # (Placeholder for audio system integration)
    
    print("Sunset Coast world built successfully!")
    print(f"  - Track length: {track_system.design.track_length}m")
    print(f"  - Checkpoints: {len(track_system.design.checkpoints)}")
    print(f"  - Power-up zones: {len(track_system.design.powerup_zones)}")
    print(f"  - Shortcuts: {len(track_system.design.shortcuts)}")
    print(f"  - Target lap time: {track_system.design.target_lap_time}s")


if __name__ == '__main__':
    app = Ursina()
    
    # Create track
    track_design = create_sunset_coast_track()
    track_system = TrackSystem(track_design)
    
    # Build world
    build_sunset_coast_world(track_system)
    
    # Add camera
    EditorCamera()
    
    print("\n=== SUNSET COAST TRACK PREVIEW ===")
    print(f"Track: {track_design.name}")
    print(f"Difficulty: {track_design.difficulty}")
    print(f"Laps: {track_design.total_laps}")
    print(f"Checkpoints: {len(track_design.checkpoints)}")
    print(f"Racing waypoints: {len(track_design.racing_line)}")
    
    app.run()
