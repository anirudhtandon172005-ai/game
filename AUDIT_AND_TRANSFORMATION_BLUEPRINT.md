# KART RUSH - COMPLETE FORENSIC AUDIT & TRANSFORMATION BLUEPRINT

## EXECUTIVE SUMMARY

**Project Status:** Foundation Complete → Race Implementation Phase

**Current State:** The project has solid architectural foundations with UI menus, save system, settings, game manager, scene manager, kart entity, and track system infrastructure. However, **the core racing experience is not yet playable** - the race scene, actual track geometry, AI opponents, camera system, HUD, and power-up systems are missing.

**Critical Gap:** Player cannot currently start and complete a race. The main.py still contains a test scene rather than launching the full game menu system.

**Priority:** Implement the complete race loop (P0), then add AI (P1), then polish (P2-P4).

---

## 1. CURRENT PROJECT TECHNOLOGY

| Component | Technology | Version | Status |
|-----------|------------|---------|--------|
| Language | Python | 3.12.10 | ✓ Installed |
| Game Engine | Ursina | 8.3.0 | ✓ Installed |
| Audio Backend | ALSA/PulseAudio | - | ⚠ Not configured (headless) |
| Build System | pip | - | ✓ Working |
| Version Control | Git | - | ✓ Initialized |

**Environment Limitations:**
- Headless server environment (no X11/display)
- No audio hardware configured
- Cannot run graphical tests directly

**Recommendation:** All runtime testing must be performed on a local machine with display. Code structure can be validated here.

---

## 2. CURRENT PROJECT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    MAIN.PPY                              │
│              (Entry Point - Test Scene)                  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────────┐    ┌──────────────────┐
│   GAME MANAGER   │    │  SCENE MANAGER   │
│  - Game States   │    │  - Transitions   │
│  - Mode Select   │    │  - Lifecycle     │
│  - Kart/Track    │    │  - Entity Reg    │
│  - Championship  │    │                  │
└──────────────────┘    └──────────────────┘
         │                       │
         │                       │
    ┌────┴────┐            ┌─────┴─────┐
    │         │            │           │
    ▼         ▼            ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
│ SETTINGS│ │ SAVE   │ │ MENU   │ │ KART     │
│ SYSTEM  │ │ SYSTEM │ │ SCENES │ │ SELECTION│
└────────┘ └────────┘ └────────┘ └──────────┘
                              │
                              ▼
                      ┌───────────────┐
                      │ TRACK SYSTEM  │
                      │ - Checkpoints │
                      │ - Racing Line │
                      │ - Shortcuts   │
                      │ - Hazards     │
                      └───────────────┘
```

**Architecture Health:** MODULAR AND SOUND. Clear separation of concerns. Systems are well-organized for expansion.

---

## 3. SYSTEM INVENTORY & GAP ANALYSIS

### Table A: System Audit

| System | Exists | Functional | Quality | Priority | Action |
|--------|--------|------------|---------|----------|--------|
| **CORE** |
| Game Manager | ✓ | ✓ | Good | P1 | Connect to main.py |
| Scene Manager | ✓ | ✓ | Good | P1 | Add race scene loading |
| Settings System | ✓ | ✓ | Good | P2 | Add graphics quality presets |
| Save System | ✓ | ✓ | Good | P2 | Add corruption recovery |
| **PLAYER** |
| Kart Entity | ✓ | Partial | Basic | P0 | Add proper physics, drift, boost |
| Kart Controller | ✗ | ✗ | Missing | P0 | IMPLEMENT |
| Drift System | △ | △ | Stub | P1 | Complete implementation |
| Boost System | △ | △ | Stub | P1 | Complete implementation |
| **RACING** |
| Race Scene | ✗ | ✗ | Missing | P0 | IMPLEMENT |
| Track Geometry | ✗ | ✗ | Missing | P0 | IMPLEMENT |
| Checkpoint System | ✓ | △ | Data only | P0 | Add visual/trigger entities |
| Lap Counter | △ | ✗ | In kart | P0 | Move to race manager |
| Position System | ✗ | ✗ | Missing | P0 | IMPLEMENT |
| Finish Detection | ✗ | ✗ | Missing | P0 | IMPLEMENT |
| **AI** |
| AI Controller | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Racing Line Usage | ✓ | ✗ | Data only | P1 | Connect to AI |
| AI Difficulty | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Overtaking Logic | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Recovery System | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| **POWER-UPS** |
| Item System | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Power-up Boxes | ✓ | △ | Data zones | P1 | Add pickup logic |
| Boost Item | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Shield Item | ✗ | ✗ | Missing | P2 | IMPLEMENT |
| Offensive Items | ✗ | ✗ | Missing | P2 | IMPLEMENT |
| **CAMERA** |
| Follow Camera | ✗ | ✗ | Missing | P0 | IMPLEMENT |
| Collision Avoidance | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Dynamic FOV | ✗ | ✗ | Missing | P2 | IMPLEMENT |
| **UI/HUD** |
| Main Menu | ✓ | ✓ | Good | P1 | Connect to game flow |
| Kart Selection | ✓ | ✓ | Good | P2 | Add 3D preview |
| Track Selection | ✓ | ✓ | Good | P2 | Add minimap preview |
| Race HUD | ✗ | ✗ | Missing | P0 | IMPLEMENT |
| Minimap | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Pause Menu | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Results Screen | ✓ | ✓ | Good | P2 | Add more stats |
| Countdown | ✗ | ✗ | Missing | P0 | IMPLEMENT |
| **AUDIO** |
| Engine Sounds | ✗ | ✗ | Missing | P2 | IMPLEMENT |
| Music System | ✗ | ✗ | Missing | P2 | IMPLEMENT |
| SFX System | ✗ | ✗ | Missing | P2 | IMPLEMENT |
| **VFX** |
| Particle System | ✗ | ✗ | Missing | P3 | IMPLEMENT |
| Skid Marks | ✗ | ✗ | Missing | P3 | IMPLEMENT |
| Boost Effects | ✗ | ✗ | Missing | P2 | IMPLEMENT |
| **TRACKS** |
| Sunset Coast | ✓ | △ | Design only | P0 | BUILD GEOMETRY |
| Neon City | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Jungle Ruins | ✗ | ✗ | Missing | P1 | IMPLEMENT |
| Volcano Run | ✗ | ✗ | Missing | P1 | IMPLEMENT |

Legend: ✓ = Complete, △ = Partial, ✗ = Missing

---

## 4. RESEARCH SYNTHESIS: KART RACING GAME DESIGN PATTERNS

### Vehicle Physics Research Findings

**Arcade Kart Handling Principles:**
1. **Exaggerated steering** - More responsive than realistic
2. **Speed-dependent steering** - Less turn at high speed
3. **Drift as core mechanic** - Maintain momentum through corners
4. **Boost as reward** - Earned through skill (drift, jumps)
5. **Forgiving collisions** - Bounce, don't crash hard

**Recommended Physics Model:**
```python
# Hybrid arcade physics (not pure raycast vehicle)
- Direct velocity control with acceleration curves
- Arcade steering with speed falloff
- Drift state with reduced lateral grip
- Jump parabola with air control
- Simple collision impulse response
```

**Why not raycast vehicle?** Ursina's built-in physics (Panda3D) lacks robust vehicle physics. Custom arcade controller provides better gameplay tuning.

### Track Design Research Findings

**Successful Kart Track Patterns:**
1. **Clear sightlines** - Player sees 2-3 turns ahead
2. **Rhythm variation** - Fast/slow/fast creates engagement
3. **Overtaking zones** - Wide sections after hairpins
4. **Risk/reward shortcuts** - Visible but challenging
5. **Landmarks** - Unique visual anchors every 15-20 seconds

**Recommended Track Structure:**
```
Start (wide) → Hairpin (brake test) → Straight (overtake) 
→ Sweeper (drift) → Technical section → Jump → Shortcut branch
→ Final straight → Finish
```

### AI Design Research Findings

**Racing AI Architecture:**
1. **Waypoint following** - Primary navigation
2. **Speed profiles** - Per-waypoint target speeds
3. **Steering behaviors** - Seek, arrive, avoid
4. **State machine** - Normal, overtaking, recovering, using item
5. **Imperfection injection** - Occasional mistakes based on difficulty

**Difficulty Scaling:**
- Easy: Slower speed, late braking, no shortcuts
- Normal: Moderate speed, basic racing line
- Hard: Optimal speed, uses shortcuts, defends position
- Expert: Near-perfect line, aggressive overtaking

### Camera Design Research Findings

**Third-Person Follow Camera:**
- Distance: 8-12 units behind kart
- Height: 4-6 units above ground
- Look-ahead: 10-15 units in front of kart
- Damping: Smooth follow (lerp 0.1-0.2)
- FOV: 70-90° (wider during boost)

**Collision Handling:**
- Raycast from camera to player
- Move camera forward on hit
- Never clip through walls

---

## 5. KART DESIGN AUDIT

### Current State
- Single cube model with 4 sphere wheels
- No driver
- No distinct silhouettes
- No animation

### Required Improvements

**Visual Design Requirements:**
1. **Distinct silhouettes** for each kart type
2. **Proportions**: Length ~2x width, low center of mass
3. **Wheel placement**: Outside body, visible rotation
4. **Driver placeholder**: Simple capsule or stylized character
5. **Color coding**: Match kart selection

**Model Hierarchy:**
```
Kart Root
├── Chassis (main body)
├── Driver (simple mesh)
├── FrontLeftWheel
├── FrontRightWheel  
├── RearLeftWheel
├── RearRightWheel
├── Exhaust VFX Socket
├── Boost VFX Socket
└── Camera Target (empty)
```

**Animation Requirements:**
- Wheel rotation (procedural, based on speed)
- Wheel steering (front wheels only)
- Body lean (procedural, based on turning)
- Suspension compression (on landing)

---

## 6. VEHICLE PHYSICS AUDIT

### Current Implementation Issues

**Problems Identified:**
1. Movement uses direct position manipulation (`self.position += self.velocity`)
2. No gravity applied
3. No ground detection
4. Steering rotates entire kart without wheel animation
5. Drift is timer-based without physics meaning
6. No collision response with walls/other karts
7. No jump mechanics

### Recommended Physics Parameters

```python
PHYSICS_CONFIG = {
    # Core movement
    'max_speed': 25.0,          # Units per second
    'acceleration': 15.0,       # Units/s²
    'brake_force': 30.0,        # Units/s²
    'reverse_speed': 8.0,       # Max reverse speed
    
    # Steering
    'steering_strength': 3.0,   # Rotation speed
    'high_speed_reduction': 0.5, # Steering reduction at max speed
    
    # Grip & Drift
    'lateral_grip': 0.95,       # Normal traction
    'drift_grip': 0.3,          # Reduced grip when drifting
    'drift_initiation_angle': 0.3,  # Radians to trigger drift
    'drift_recovery_rate': 0.5, # How fast drift decays
    
    # Boost
    'boost_multiplier': 1.5,    # Speed multiplier
    'boost_duration': 3.0,      # Seconds
    'drift_boost_threshold': 2.0, # Seconds to earn boost
    
    # Jump & Air
    'gravity': 30.0,            # Downward acceleration
    'jump_force': 12.0,         # Initial jump velocity
    'air_control': 0.3,         # Reduced steering in air
    
    # Collision
    'bounce_factor': 0.5,       # Velocity retention after collision
    'knockback_force': 10.0,    # Impulse from kart collision
}
```

---

## 7. TRACK DESIGN AUDIT

### Sunset Coast Analysis

**Design Document Quality:** EXCELLENT
- 14 checkpoints properly spaced
- 27 racing waypoints with speed profiles
- 2 shortcuts (major pier, minor beach)
- Clear elevation changes (0-10m)
- Good landmark distribution

**Missing Components:**
1. Actual road mesh/geometry
2. Terrain (beach, ocean, cliffs)
3. Barriers and boundaries
4. Visual checkpoint markers
5. Start grid positions
6. Finish line banner/arch
7. Environmental props (palms, umbrellas, lighthouse model)
8. Lighting setup (sunset colors)
9. Water plane
10. Collision meshes

### Other Tracks Status

| Track | Design | Geometry | Environment | AI Data | Status |
|-------|--------|----------|-------------|---------|--------|
| Sunset Coast | ✓ Complete | ✗ | ✗ | ✓ | Needs build |
| Neon City | ✗ | ✗ | ✗ | ✗ | Not started |
| Jungle Ruins | ✗ | ✗ | ✗ | ✗ | Not started |
| Volcano Run | ✗ | ✗ | ✗ | ✗ | Not started |

---

## 8. MISSING SYSTEMS (DETAILED)

### P0: CRITICAL - GAME CANNOT FUNCTION WITHOUT

#### 8.1 Race Scene (`src/scenes/race_scene.py`)
**Purpose:** Main gameplay scene coordinating all race elements.

**Required Components:**
```python
class RaceScene:
    - Track loading and initialization
    - Player kart instantiation
    - AI kart spawning
    - Start grid positioning
    - Countdown sequence (3, 2, 1, GO!)
    - Race state management (countdown, racing, finished)
    - Checkpoint triggering
    - Lap counting
    - Position calculation
    - Finish detection
    - Results transition
    - Pause handling
```

#### 8.2 Track Geometry Builder
**Purpose:** Convert track design data into actual 3D world.

**Required Functions:**
```python
def build_track_geometry(track_design):
    - Generate road mesh from checkpoints
    - Create terrain base
    - Place barriers/walls
    - Add water planes (Sunset Coast)
    - Position start grid markers
    - Create finish line arch/banner
    - Set up collision volumes
```

#### 8.3 Camera Controller
**Purpose:** Smooth third-person follow camera.

**Required Features:**
```python
class FollowCamera:
    - Target tracking (kart position)
    - Offset management (distance, height, angle)
    - Smooth damping (lerp)
    - Look-ahead calculation
    - Collision avoidance (raycast)
    - FOV modulation (boost = wider)
    - Shake effects (collision, landing)
```

#### 8.4 Race HUD (`src/ui/hud.py`)
**Purpose:** Display critical race information.

**Required Elements:**
```python
class RaceHUD:
    - Position indicator (e.g., "3/8")
    - Lap counter ("Lap 2/3")
    - Race timer (MM:SS.ms)
    - Current lap time
    - Best lap time
    - Speedometer (optional)
    - Item/power-up display
    - Boost meter
    - Minimap (P1)
```

#### 8.5 Countdown System
**Purpose:** Fair race start sequence.

**Implementation:**
```python
def countdown_sequence():
    - Display "3" (1 second)
    - Display "2" (1 second)
    - Display "1" (1 second)
    - Display "GO!" (0.5 seconds)
    - Enable player input
    - Start race timer
```

#### 8.6 Position System
**Purpose:** Accurate racer ranking.

**Algorithm:**
```python
def calculate_positions(racers):
    # Sort by: lap > checkpoint > distance to next checkpoint
    for each racer:
        key = (current_lap, current_checkpoint, -distance_to_next)
    sort all racers by key
    assign positions 1, 2, 3...
```

**DO NOT** use simple distance-to-finish or global position.

#### 8.7 Respawn System
**Purpose:** Recover karts that fall off track or get stuck.

**Logic:**
```python
def check_respawn(kart):
    - Detect if kart is below track (fall)
    - Detect if kart is stuck (no movement)
    - Detect if kart is upside down
    - Find nearest respawn point
    - Teleport kart
    - Reset velocity
    - Apply brief invulnerability
```

---

### P1: CORE GAMEPLAY

#### 8.8 AI Controller
**Purpose:** Computer-controlled opponents.

**Architecture:**
```python
class AIKartController:
    - Follow racing line waypoints
    - Adjust speed based on waypoint profile
    - Brake at designated points
    - Initiate drift in drift zones
    - Seek power-ups
    - Avoid obstacles (simple steering)
    - Overtake when opportunity arises
    - Defend position when leading
    - Recover from collisions
    - Use items strategically
```

**Difficulty Profiles:**
```python
AI_PROFILES = {
    'easy': {
        'speed_modifier': 0.7,
        'brake_distance': 1.5,  # Brake earlier
        'overtake_aggression': 0.2,
        'mistake_chance': 0.1,
    },
    'normal': {
        'speed_modifier': 0.85,
        'brake_distance': 1.2,
        'overtake_aggression': 0.5,
        'mistake_chance': 0.05,
    },
    'hard': {
        'speed_modifier': 0.95,
        'brake_distance': 1.0,
        'overtake_aggression': 0.8,
        'mistake_chance': 0.02,
    },
    'expert': {
        'speed_modifier': 1.0,
        'brake_distance': 0.9,  # Later braking
        'overtake_aggression': 1.0,
        'mistake_chance': 0.01,
    },
}
```

#### 8.9 Power-Up System
**Purpose:** Item pickup and usage mechanics.

**Items to Implement:**
```python
ITEMS = {
    'boost': {
        'rarity': 'common',
        'effect': 'Instant speed boost',
        'duration': 3.0,
    },
    'shield': {
        'rarity': 'uncommon',
        'effect': 'Block one hit',
        'duration': 10.0,
    },
    'oil': {
        'rarity': 'common',
        'effect': 'Drop slippery hazard',
        'instant': True,
    },
    'rocket': {
        'rarity': 'rare',
        'effect': 'Fire projectile at leader',
        'targeting': 'auto',
    },
    'lightning': {
        'rarity': 'epic',
        'effect': 'Slow all other racers',
        'duration': 3.0,
    },
    'turbo': {
        'rarity': 'uncommon',
        'effect': 'Continuous acceleration boost',
        'duration': 5.0,
    },
    'magnet': {
        'rarity': 'rare',
        'effect': 'Attract nearby power-ups',
        'duration': 8.0,
    },
}
```

**Item Distribution Logic:**
```python
def get_item_for_position(position, total_racers):
    # Comeback mechanics: worse positions get better items
    if position <= 2:
        return random_choice(['boost', 'oil'], weights=[0.7, 0.3])
    elif position <= 4:
        return random_choice(['boost', 'shield', 'turbo'])
    else:
        return random_choice(['rocket', 'lightning', 'magnet', 'shield'],
                            weights=[0.3, 0.2, 0.2, 0.3])
```

#### 8.10 Minimap
**Purpose:** Navigation aid showing track layout and racer positions.

**Implementation:**
```python
class Minimap:
    - Render track outline from waypoints
    - Draw player marker (arrow showing direction)
    - Draw AI markers (dots)
    - Show checkpoints (subtle indicators)
    - Update positions every frame
    - Rotate to match player direction OR fixed north-up
```

#### 8.11 Pause System
**Purpose:** Allow player to pause race.

**Requirements:**
```python
def pause_race():
    - Stop all kart movement (freeze physics)
    - Stop AI updates
    - Stop timers
    - Display pause menu
    - Options: Resume, Restart, Quit to Menu
    
def unpause_race():
    - Resume all systems
    - Hide pause menu
```

---

### P2: USER EXPERIENCE

#### 8.12 Audio System
**Sound Categories:**
```python
AUDIO_SOURCES = {
    'music': [
        'menu_theme.wav',
        'race_theme.wav',
        'results_theme.wav',
    ],
    'sfx_kart': [
        'engine_idle.wav',
        'engine_accelerate.wav',
        'engine_brake.wav',
        'drift_start.wav',
        'drift_loop.wav',
        'boost_activate.wav',
        'landing.wav',
        'collision.wav',
    ],
    'sfx_items': [
        'item_pickup.wav',
        'boost_use.wav',
        'shield_activate.wav',
        'rocket_fire.wav',
        'rocket_explode.wav',
        'lightning_strike.wav',
        'oil_drop.wav',
    ],
    'sfx_race': [
        'countdown_beep.wav',
        'countdown_go.wav',
        'checkpoint_pass.wav',
        'lap_complete.wav',
        'finish_race.wav',
        'podium_fanfare.wav',
    ],
    'ambient': [
        'ocean_waves.wav',  # Sunset Coast
        'city_hum.wav',     # Neon City
        'jungle_crowd.wav', # Jungle Ruins
        'volcano_rumble.wav', # Volcano Run
    ],
}
```

**Audio Implementation Notes:**
- Engine pitch varies with speed
- Doppler effect for passing karts
- Volume attenuation with distance
- Music crossfade between states

#### 8.13 VFX System
**Particle Effects Needed:**
```python
VFX_LIBRARY = {
    'exhaust': {
        'emitter': 'kart rear',
        'particle': 'smoke puff',
        'rate': 'continuous',
    },
    'boost': {
        'emitter': 'kart rear',
        'particle': 'flame jet',
        'rate': 'during boost',
    },
    'drift_smoke': {
        'emitter': 'rear tires',
        'particle': 'tire smoke',
        'rate': 'during drift',
    },
    'skid_sparks': {
        'emitter': 'kart bottom',
        'particle': 'sparks',
        'rate': 'on contact',
    },
    'landing_dust': {
        'emitter': 'ground below',
        'particle': 'dust cloud',
        'rate': 'on landing',
    },
    'explosion': {
        'emitter': 'impact point',
        'particle': 'fireball + debris',
        'rate': 'one-shot',
    },
    'shield': {
        'emitter': 'kart surround',
        'particle': 'energy bubble',
        'rate': 'continuous while active',
    },
    'speed_lines': {
        'emitter': 'camera edges',
        'particle': 'streak lines',
        'rate': 'during boost',
    },
}
```

#### 8.14 Settings Expansion
**Add Graphics Presets:**
```python
GRAPHICS_PRESETS = {
    'low': {
        'shadows': False,
        'particles': False,
        'anti_aliasing': False,
        'draw_distance': 50,
    },
    'medium': {
        'shadows': True,
        'particles': True,
        'anti_aliasing': False,
        'draw_distance': 100,
    },
    'high': {
        'shadows': True,
        'particles': True,
        'anti_aliasing': True,
        'draw_distance': 200,
    },
    'ultra': {
        'shadows': True,
        'particles': True,
        'anti_aliasing': True,
        'draw_distance': 500,
    },
}
```

---

### P3: CONTENT

#### 8.15 Additional Tracks

**Neon City Design Specification:**
```
Theme: Futuristic night race
Lighting: Dark with neon signs, streetlights
Road: Wet asphalt with reflections
Key Features:
- Underground tunnel section
- Sky bridge (elevated)
- Moving train hazard (telegraphed)
- Alley shortcut (narrow, technical)
- Tight downtown hairpin
- Long highway straight
Landmarks: Neon tower, suspension bridge, holographic billboard
Hazards: Train crossing, wet road (reduced grip)
```

**Jungle Ruins Design Specification:**
```
Theme: Ancient temple complex
Lighting: Filtered sunlight, misty
Road: Stone path through jungle
Key Features:
- Waterfall bridge
- Temple gate (dynamic opening/closing)
- Cave section (dark, headlights needed)
- Mud slowdown zones
- Ancient ramp jump
- Narrow forest paths
Landmarks: Giant stone statue, waterfall, temple entrance
Hazards: Mud pits, falling rocks (telegraphed), narrow bridges
```

**Volcano Run Design Specification:**
```
Theme: Active volcanic circuit
Lighting: Dark with lava glow
Road: Industrial/metallic near volcano
Key Features:
- Lava crossings (visual hazard)
- Mine tunnel
- Volcanic ridge (high elevation)
- Collapsing bridge sections (timed)
- Lava jump (over molten rock)
- Steep descent finale
Landmarks: Volcano cone, lava waterfall, destroyed facility
Hazards: Lava bursts (telegraphed), falling rocks, unstable bridges
```

#### 8.16 Kart Fleet Expansion

**Recommended 8-Kart Roster:**
```python
KART_ROSTER = {
    'kart_default': {
        'name': 'Standard',
        'stats': {'speed': 7, 'handling': 7, 'accel': 7, 'weight': 5},
        'unlock': 'default',
    },
    'kart_speed': {
        'name': 'Speed Racer',
        'stats': {'speed': 10, 'handling': 4, 'accel': 6, 'weight': 4},
        'unlock': 'win_sunset_coast',
    },
    'kart_heavy': {
        'name': 'Heavy Hitter',
        'stats': {'speed': 6, 'handling': 5, 'accel': 4, 'weight': 10},
        'unlock': 'win_championship',
    },
    'kart_balanced': {
        'name': 'Balanced Pro',
        'stats': {'speed': 7, 'handling': 8, 'accel': 7, 'weight': 6},
        'unlock': 'complete_time_trials',
    },
    'kart_drift': {
        'name': 'Drift King',
        'stats': {'speed': 6, 'handling': 9, 'accel': 8, 'weight': 5},
        'unlock': 'perform_50_drift_boosts',
    },
    'kart_accel': {
        'name': 'Rocket Starter',
        'stats': {'speed': 8, 'handling': 6, 'accel': 10, 'weight': 5},
        'unlock': 'win_10_races',
    },
    'kart_light': {
        'name': 'Feather',
        'stats': {'speed': 9, 'handling': 8, 'accel': 8, 'weight': 3},
        'unlock': 'find_all_shortcuts',
    },
    'kart_legendary': {
        'name': 'Champion',
        'stats': {'speed': 9, 'handling': 9, 'accel': 9, 'weight': 7},
        'unlock': 'win_all_championships',
    },
}
```

---

## 9. TARGET ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                        MAIN.PY                               │
│              (Launch GameManager + SceneManager)             │
└──────────────────────────┬───────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
┌──────────────────┐              ┌──────────────────┐
│   GAME MANAGER   │              │  SCENE MANAGER   │
│  - State Machine │◄────────────►│  - Transitions   │
│  - Session Data  │              │  - Scene Lifecycle│
│  - Progression   │              │  - Entity Registry│
└────────┬─────────┘              └─────────┬────────┘
         │                                  │
    ┌────┴────┬────────────┐          ┌─────┴─────────┐
    │         │            │          │               │
    ▼         ▼            ▼          ▼               ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌─────────────────┐
│SETTINGS│ │ SAVE   │ │ MENU   │ │ KART   │ │    RACE SCENE   │
│        │ │SYSTEM  │ │SCENES  │ │ SELECT │ │  (NEW - P0)     │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┬────────┘
                                                     │
                    ┌────────────────────────────────┼────────┐
                    │                                │        │
                    ▼                                ▼        ▼
           ┌────────────────┐              ┌──────────────┐ ┌──────────┐
           │  TRACK SYSTEM  │              │KART CONTROLLER│ │   CAMERA │
           │ - Geometry     │              │ - Player     │ │ CONTROLLER│
           │ - Checkpoints  │              │ - AI (P1)    │ │  (P0)    │
           │ - Racing Line  │              │ - Physics    │ └──────────┘
           │ - Hazards      │              └──────┬───────┘
           │ - PowerUps     │                     │
           └────────────────┘              ┌───────┴────────┐
                                           │                │
                                           ▼                ▼
                                    ┌───────────┐   ┌──────────────┐
                                    │ RACE HUD  │   │ POSITION/LAP │
                                    │   (P0)    │   │   SYSTEM     │
                                    └───────────┘   └──────────────┘
```

---

## 10. DEPENDENCY GRAPH

```
Race Scene (P0)
    ├── Track Geometry (P0)
    │   ├── Track Design Data ✓
    │   ├── Road Mesh Generation
    │   ├── Terrain
    │   ├── Barriers
    │   └── Collision Volumes
    │
    ├── Kart Controller (P0)
    │   ├── Input Handling
    │   ├── Physics Update
    │   ├── Drift Logic
    │   └── Boost Logic
    │
    ├── Camera Controller (P0)
    │   ├── Follow Logic
    │   └── Collision Avoidance
    │
    ├── Race HUD (P0)
    │   ├── Position Display
    │   ├── Lap Display
    │   └── Timer Display
    │
    ├── Countdown System (P0)
    │
    ├── Lap/Checkpoint System (P0)
    │   └── Track Checkpoint Data ✓
    │
    ├── Position System (P0)
    │
    └── Respawn System (P0)
        └── Respawn Point Data ✓

AI Opponents (P1)
    ├── AI Controller
    │   ├── Waypoint Following
    │   ├── Speed Profiles
    │   └── Difficulty Modifiers
    │
    └── Racing Line Data ✓

Power-Ups (P1)
    ├── Item System
    ├── Pickup Detection
    ├── Item Effects
    └── Power-Up Zone Data ✓

Minimap (P1)
    └── Track Waypoint Data ✓

Audio (P2)
    ├── Sound Effect Library
    ├── Music System
    └── Audio Zones

VFX (P2)
    ├── Particle System
    └── Effect Definitions

Additional Tracks (P3)
    ├── Neon City
    ├── Jungle Ruins
    └── Volcano Run
```

---

## 11. IMPLEMENTATION ROADMAP

### PHASE 1: PLAYABLE RACE LOOP (P0 - CRITICAL)
**Goal:** Player can select kart, select track, and complete a race

**Tasks:**
1. Fix main.py to launch game menu system
2. Create RaceScene class
3. Implement track geometry builder for Sunset Coast
4. Create player kart controller with proper physics
5. Implement follow camera
6. Create race HUD
7. Implement countdown sequence
8. Implement lap counting and checkpoint system
9. Implement position calculation
10. Implement finish detection and results transition
11. Implement respawn system

**Definition of Done:** Player can drive from start to finish, complete 3 laps, see results screen

---

### PHASE 2: AI OPPONENTS (P1 - CORE GAMEPLAY)
**Goal:** Race against 7 AI opponents

**Tasks:**
1. Create AIKartController class
2. Implement waypoint following
3. Implement speed profile adherence
4. Implement braking at designated points
5. Implement basic overtaking behavior
6. Implement collision recovery
7. Create difficulty profiles (Easy, Normal, Hard, Expert)
8. Integrate AI into RaceScene
9. Balance AI speeds for competitive racing

**Definition of Done:** 8-kart race completes with believable AI behavior, overtaking occurs, finishing order varies

---

### PHASE 3: DRIFT & BOOST (P1 - CORE GAMEPLAY)
**Goal:** Reward-based drift and boost mechanics

**Tasks:**
1. Refine drift physics (initiation, maintenance, exit)
2. Implement drift boost charging
3. Implement drift boost activation
4. Add starting boost (press accelerate at GO!)
5. Create drift VFX (tire smoke)
6. Create boost VFX (flame jet)
7. Balance drift duration vs boost reward
8. Tune boost speed multiplier

**Definition of Done:** Player can drift through corners, earn boost, activate boost for speed increase

---

### PHASE 4: POWER-UPS (P1 - CORE GAMEPLAY)
**Goal:** Strategic item system

**Tasks:**
1. Create PowerUpManager
2. Implement power-up box spawning
3. Implement pickup detection
4. Create item inventory UI
5. Implement Boost item
6. Implement Shield item
7. Implement Oil item
8. Implement Rocket item
9. Implement Lightning item
10. Implement comeback distribution logic
11. Create item VFX
12. Create item SFX

**Definition of Done:** Player can pick up items, use items, see effects on self and others

---

### PHASE 5: MINIMAP & PAUSE (P1 - UX)
**Goal:** Navigation and control features

**Tasks:**
1. Create Minimap UI component
2. Render track outline
3. Display racer positions
4. Implement pause functionality
5. Create pause menu
6. Implement restart race
7. Implement quit to menu

**Definition of Done:** Player can navigate using minimap, pause and resume race

---

### PHASE 6: ADDITIONAL TRACKS (P3 - CONTENT)
**Goal:** Four unique tracks

**Tasks:**
1. Build Neon City geometry
2. Build Jungle Ruins geometry
3. Build Volcano Run geometry
4. Create AI racing lines for each
5. Place hazards unique to each track
6. Implement dynamic events (train, temple gate, lava burst)
7. Balance track difficulties

**Definition of Done:** All 4 tracks playable with unique characteristics

---

### PHASE 7: AUDIO & VFX (P2 - POLISH)
**Goal:** Immersive presentation

**Tasks:**
1. Source/create sound effects library
2. Implement engine sound (pitch varies with RPM)
3. Implement music system
4. Implement ambient zone audio
5. Create particle system
6. Implement exhaust, drift, boost, explosion VFX
7. Implement skid marks
8. Add screen shake on collision/landing

**Definition of Done:** Game has appropriate audio feedback and visual effects

---

### PHASE 8: PROGRESSION & UNLOCKS (P2 - UX)
**Goal:** Reward player progression

**Tasks:**
1. Expand unlock conditions
2. Implement kart unlocking
3. Implement track unlocking
4. Add championship point rewards
5. Add best time rewards
6. Create unlock notifications
7. Update kart selection to show locked/unlocked

**Definition of Done:** Player has clear progression goals and receives unlocks

---

### PHASE 9: OPTIMIZATION (P4 - PERFORMANCE)
**Goal:** Stable 60 FPS

**Tasks:**
1. Profile frame time
2. Implement object pooling for particles
3. Reduce draw calls (batching)
4. Implement LOD for distant objects
5. Optimize collision detection
6. Reduce AI update frequency for distant karts
7. Implement frustum culling awareness

**Definition of Done:** Game maintains 60 FPS with 8 karts and full VFX

---

### PHASE 10: QA & POLISH (P4 - FINAL)
**Goal:** Bug-free, polished experience

**Tasks:**
1. Execute 50+ QA passes (as specified in master prompt)
2. Fix all P0/P1 bugs
3. Balance gameplay (speeds, AI difficulty, item distribution)
4. Polish UI animations
5. Add accessibility options
6. Final playtesting
7. Regression testing

**Definition of Done:** All QA passes pass, game feels polished and fair

---

## 12. RISK ANALYSIS

### Table D: Risk Assessment

| Risk | Probability | Impact | Severity | Mitigation |
|------|-------------|--------|----------|------------|
| Ursina physics limitations | High | High | Critical | Use custom arcade controller instead of built-in vehicle physics |
| Headless development environment | Certain | Medium | High | Develop code structure here, test on local machine with display |
| Asset creation complexity | Medium | High | Medium | Use procedural generation and simple geometric shapes initially |
| AI pathfinding complexity | Medium | Medium | Medium | Use waypoint following (already designed) instead of complex navmesh |
| Performance on low-end hardware | Low | Medium | Low | Implement graphics settings, LOD, particle limits |
| Scope creep | High | Medium | Medium | Strictly prioritize P0/P1 first, defer P3/P4 |
| Audio asset licensing | Medium | Low | Low | Use royalty-free sources or procedural audio |
| Multi-track content volume | Medium | Medium | Medium | Reuse systems, vary parameters and layouts |

---

## 13. RED TEAM FINDINGS

### Critical Vulnerabilities

**1. No Actual Playable Race**
- Current project cannot start a race
- main.py runs a test scene, not the menu system
- **Fix:** Immediately implement RaceScene and connect main.py to GameManager

**2. Track Designs Are Data-Only**
- Sunset Coast exists as Python data structures
- No actual 3D geometry, terrain, or visuals
- **Fix:** Build track geometry generator

**3. Kart Has No Real Physics**
- Movement is direct position manipulation
- No gravity, ground detection, or collision response
- **Fix:** Implement proper arcade physics controller

**4. No Camera System**
- Test scene uses static camera look_at
- No follow behavior, no collision avoidance
- **Fix:** Implement FollowCamera class

**5. No Win Condition**
- Kart can drive forever with no goal
- No lap counting, no finish detection
- **Fix:** Implement complete race state machine

**6. AI Does Not Exist**
- Racing alone is not a "racing game"
- **Fix:** Implement AI controller after basic race works

### Potential Player Complaints

**"Controls feel floaty"**
- Cause: No friction/drag modeling
- Fix: Add proper lateral grip and drag coefficients

**"AI cheats with perfect racing"**
- Cause: AI follows exact line without variation
- Fix: Add noise to AI steering and occasional mistakes

**"Can't tell where the track goes"**
- Cause: Poor visual guidance
- Fix: Add barriers, road markings, landmarks

**"Fell off and couldn't recover"**
- Cause: No respawn system
- Fix: Implement automatic respawn detection

**"Got stuck behind AI forever"**
- Cause: No rubber-banding or comeback mechanics
- Fix: Add item-based comeback system, AI speed limits

---

## 14. SCOPE RECOMMENDATIONS

### MUST HAVE (MVP - Minimum Viable Product)
- Playable race loop (start → drive → finish → results)
- 1 complete track (Sunset Coast)
- Player kart with drift and boost
- 7 AI opponents
- Basic power-ups (boost, shield, oil)
- Position/lap/timer HUD
- Minimap
- Pause/restart

### SHOULD HAVE (Complete Experience)
- 4 tracks with unique themes
- Full power-up roster (7 items)
- Championship mode
- Time trial mode
- 8 unlockable karts
- Audio (SFX + music)
- VFX (particles, skids)
- Save/load progression

### NICE TO HAVE (Polish)
- Animated drivers
- Kart customization (colors, decals)
- Photo mode
- Ghost karts (time trial)
- Replay system
- Online leaderboards

### DO NOT IMPLEMENT YET
- Multiplayer networking
- Complex kart customization
- Story mode
- Character-specific abilities
- Weather dynamics
- Day/night cycles per track

---

## 15. ASSET REQUIREMENTS

### Table B: Asset Audit

| Asset Type | Exists | Quality | Reusable | Missing | Priority |
|------------|--------|---------|----------|---------|----------|
| **3D Models** |
| Kart models | △ | Basic | Partial | 7 more karts | P1 |
| Driver models | ✗ | - | - | All | P3 |
| Track pieces | ✗ | - | - | Road segments | P0 |
| Barriers | ✗ | - | - | Guardrails, walls | P0 |
| Props (trees, buildings) | ✗ | - | - | All | P2 |
| Landmarks (lighthouse, etc) | ✗ | - | - | All | P2 |
| **Textures** |
| Road surface | ✗ | - | - | Asphalt, painted | P0 |
| Terrain (sand, grass) | ✗ | - | - | All | P1 |
| Barrier textures | ✗ | - | - | Metal, concrete | P0 |
| Prop textures | ✗ | - | - | All | P2 |
| UI textures | △ | Basic | Yes | Minimap icons | P1 |
| **Audio** |
| Engine sounds | ✗ | - | - | All | P2 |
| SFX library | ✗ | - | - | All | P2 |
| Music tracks | ✗ | - | - | All | P2 |
| Ambient loops | ✗ | - | - | All | P2 |
| **VFX** |
| Particle textures | ✗ | - | - | Smoke, fire, sparks | P2 |
| Skid mark texture | ✗ | - | - | Black tire mark | P3 |

### Asset Creation Strategy

**Phase 1 (P0):** Use procedural geometry
- Generate road from spline extrusion
- Use colored boxes for barriers
- Procedural terrain from heightmap

**Phase 2 (P1):** Simple primitives
- Karts: Combination of boxes, cylinders, spheres
- Drivers: Capsule with sphere head
- Props: Box trees, cylinder buildings

**Phase 3 (P2):** Improved visuals
- Better UV mapping
- Distinctive materials
- Emissive textures for Neon City

**Asset Sources:**
- Procedural generation (roads, terrain)
- Geometric primitives (buildings, props)
- OpenGameArt.org (free assets)
- Kenney.nl (CC0 game assets)
- Self-created simple models

---

## 16. REQUIRED OUTPUT TABLES

### Table E: Development Task Breakdown

| ID | Task | Dependency | Effort | Risk | Priority | Definition of Done | Test |
|----|------|------------|--------|------|----------|-------------------|------|
| T01 | Fix main.py entry point | None | Low | Low | P0 | Launches main menu | Menu appears |
| T02 | Create RaceScene class | T01 | Medium | Low | P0 | Scene loads track | Track visible |
| T03 | Build track geometry | T02 | High | Medium | P0 | Drivable road exists | Kart stays on road |
| T04 | Implement kart physics | None | Medium | Medium | P0 | Responsive controls | Kart accelerates, steers, brakes |
| T05 | Create follow camera | T04 | Medium | Low | P0 | Smooth camera follow | No clipping through walls |
| T06 | Create race HUD | T02 | Low | Low | P0 | Shows position, lap, time | Values update correctly |
| T07 | Implement countdown | T02 | Low | Low | P0 | 3-2-1-GO sequence | Input enabled at GO |
| T08 | Implement lap system | T03 | Medium | Low | P0 | Counts laps correctly | 3 laps = finish |
| T09 | Implement position system | T08 | Medium | Medium | P0 | Correct rankings | Overtaking updates position |
| T10 | Implement finish detection | T08 | Low | Low | P0 | Triggers results | Results screen shows |
| T11 | Implement respawn | T03 | Medium | Low | P0 | Recovers stuck karts | Kart respawns on track |
| T12 | Create AI controller | T03, T04 | High | Medium | P1 | AI completes race | AI finishes without getting stuck |
| T13 | Implement AI difficulty | T12 | Medium | Low | P1 | Different speeds | Easy slower than Expert |
| T14 | Refine drift mechanics | T04 | Medium | Medium | P1 | Drift earns boost | Drift boost activates |
| T15 | Implement power-up system | T02 | High | Medium | P1 | Items usable | Items affect race |
| T16 | Create minimap | T03 | Medium | Low | P1 | Shows track + racers | Markers move correctly |
| T17 | Implement pause | T02 | Low | Low | P1 | Game freezes | Resume works |
| T18 | Build Neon City | T02 | High | Low | P3 | Drivable track | Unique from Sunset Coast |
| T19 | Build Jungle Ruins | T02 | High | Low | P3 | Drivable track | Unique theme |
| T20 | Build Volcano Run | T02 | High | Low | P3 | Drivable track | Hazard mechanics work |
| T21 | Add audio system | T02 | Medium | Low | P2 | Sounds play | Engine pitch varies |
| T22 | Add VFX system | T02 | Medium | Low | P2 | Particles emit | Boost/drift VFX visible |
| T23 | Expand kart roster | T04 | Low | Low | P3 | 8 karts available | Each has unique stats |
| T24 | Implement unlocks | Save System | Low | Low | P2 | Karts/tracks unlock | Locked content inaccessible |
| T25 | Optimization pass | All P0/P1 | Medium | Low | P4 | 60 FPS stable | Profiler shows <16ms/frame |

---

## 17. TRANSFORMATION MATRIX

### CURRENT STATE → TARGET STATE

| Subsystem | Current | Target | Gap | Solution | Dependencies | Test |
|-----------|---------|--------|-----|----------|--------------|------|
| **Entry Point** | Test scene | Full game menu | No menu launch | Connect main.py to GameManager | None | Menu renders |
| **Race Scene** | Missing | Complete race environment | No gameplay | Implement RaceScene class | Track data | Race starts |
| **Track Geometry** | Data only | 3D drivable world | No visuals/collision | Build procedural track generator | Checkpoint data | Kart drives on road |
| **Player Control** | Basic movement | Arcade physics | Floaty, unrealistic | Implement physics controller | Input system | Responsive handling |
| **Camera** | Static look_at | Dynamic follow | No gameplay camera | Create FollowCamera | Kart entity | Smooth tracking |
| **AI** | Missing | 7 opponents | Single player only | Implement AI controller | Racing line data | AI completes race |
| **Power-Ups** | Data zones | Functional items | No pickups/effects | Create PowerUpManager | Item definitions | Items change race outcome |
| **HUD** | Missing | Full race info | No feedback | Implement RaceHUD | Race state | Info displays correctly |
| **Audio** | Missing | Full soundscape | Silent game | Add audio system | Sound assets | Audio enhances gameplay |
| **VFX** | Missing | Particle effects | Sterile visuals | Create VFX system | Particle textures | Effects enhance feedback |

---

## 18. FINAL AGENTIC LOOP INSTRUCTIONS

After this audit, execute the following loop:

```
SELECT_HIGHEST_PRIORITY_GAP (P0 first)
    ↓
IMPLEMENT solution
    ↓
BUILD (verify no syntax errors)
    ↓
RUN (on local machine with display)
    ↓
TEST (does it meet Definition of Done?)
    ↓
OBSERVE (note any issues)
    ↓
COMPARE to audit specification
    ↓
FIX any problems
    ↓
RETEST
    ↓
MARK_GAP_COMPLETE
    ↓
SELECT_NEXT_GAP
```

Continue until all P0 gaps resolved, then P1, then P2, etc.

**DO NOT** skip to P3/P4 content before P0/P1 core gameplay works.

**DO NOT** declare completion after code compiles—must verify runtime behavior.

**DO NOT** assume systems work—test each one independently and integrated.

---

## 19. COMPLETION CHECKLIST

The game is COMPLETE only when ALL of these pass:

### Core Gameplay
- [ ] Launch → Main Menu works
- [ ] Kart Selection works
- [ ] Track Selection works
- [ ] Race starts with countdown
- [ ] Player can control kart (accelerate, brake, steer, drift, boost)
- [ ] Kart physics feel responsive and fair
- [ ] Camera follows smoothly without clipping
- [ ] HUD displays correct position, lap, time
- [ ] Checkpoints register correctly
- [ ] Laps count accurately (3 laps = finish)
- [ ] Position updates on overtaking
- [ ] Finish triggers results screen
- [ ] Results show correct data
- [ ] Retry race works
- [ ] Return to menu works

### AI & Competition
- [ ] 7 AI karts start in grid
- [ ] AI complete the race
- [ ] AI overtake player and each other
- [ ] AI use racing line appropriately
- [ ] AI recover from collisions
- [ ] Difficulty levels produce different performance
- [ ] Finishing order varies between races

### Mechanics
- [ ] Drifting initiates when turning sharply
- [ ] Drift boost charges during drift
- [ ] Drift boost activates on release
- [ ] Starting boost possible with timing
- [ ] Power-up boxes spawn
- [ ] Player can pick up items
- [ ] Items have intended effects
- [ ] Item distribution favors comeback

### Content
- [ ] Sunset Coast fully playable
- [ ] Neon City fully playable
- [ ] Jungle Ruins fully playable
- [ ] Volcano Run fully playable
- [ ] Each track feels visually distinct
- [ ] Each track has appropriate difficulty
- [ ] Shortcuts exist and are viable
- [ ] Hazards affect gameplay

### UX
- [ ] Minimap shows track and racers
- [ ] Pause freezes game state
- [ ] Resume continues correctly
- [ ] Restart resets all state
- [ ] Settings affect game behavior
- [ ] Save/load preserves progress
- [ ] Unlocks persist across sessions

### Presentation
- [ ] Engine audio plays
- [ ] SFX trigger appropriately
- [ ] Music plays in menus/races
- [ ] Drift VFX visible
- [ ] Boost VFX visible
- [ ] Collision VFX/sparks
- [ ] Skid marks appear

### Quality
- [ ] No crashes in normal play
- [ ] No soft-locks (stuck states)
- [ ] No unfair deaths/falls
- [ ] Consistent 60 FPS (or stable target)
- [ ] No memory leaks (long session test)
- [ ] Controls responsive
- [ ] UI readable

### Testing
- [ ] 50+ QA passes executed
- [ ] All P0 bugs fixed
- [ ] All P1 bugs fixed
- [ ] Regression suite passes
- [ ] Full user journey tested 5+ times

---

## 20. FINAL VERIFICATION INSTRUCTION

Before declaring ANY task complete:

1. **BUILD** the project (check for syntax errors)
2. **RUN** on a machine with display
3. **OBSERVE** the actual behavior
4. **TEST** against the Definition of Done
5. **DOCUMENT** any discrepancies
6. **FIX** issues found
7. **RETEST** until passing

**DO NOT** claim success based on code inspection alone.

**DO NOT** assume "it should work"—verify it DOES work.

**DO NOT** move to next task until current task verified.

---

## CONCLUSION

This audit identifies **11 critical missing systems** preventing the game from being playable. The architecture is sound, but implementation must focus on:

**IMMEDIATE (P0):** Race Scene, Track Geometry, Kart Physics, Camera, HUD, Countdown, Lap/Position systems

**NEXT (P1):** AI Opponents, Drift/Boost refinement, Power-Ups, Minimap, Pause

**LATER (P2-P4):** Audio, VFX, Additional Tracks, Progression, Optimization, Polish

The project can become a complete, playable kart racer within focused development sprints following this blueprint.

**Estimated Effort:**
- P0 tasks: 3-5 days of focused development
- P1 tasks: 3-5 days
- P2 tasks: 2-3 days
- P3 tasks: 4-6 days
- P4 tasks: 2-3 days

**Total: ~14-22 days for complete, polished game**

Begin with T01: Fix main.py entry point.
