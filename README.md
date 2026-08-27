# KART RUSH

A 3D go-kart racing game built with Python and Ursina engine.

## Features

- **Game Modes:**
  - Quick Race
  - Championship (4-race series)
  - Time Trial

- **4 Unique Tracks:**
  - Sunset Coast (Easy)
  - Neon City (Medium)
  - Jungle Ruins (Hard)
  - Volcano Run (Expert)

- **Kart Selection:**
  - Multiple karts with different stats
  - Speed, Handling, Acceleration, Weight

- **Racing Mechanics:**
  - Drifting with boost rewards
  - Speed boosts
  - Checkpoint system
  - Lap timing
  - Position tracking

- **Power-ups:**
  - Boost
  - Shield
  - And more!

- **Full UI System:**
  - Main Menu
  - Kart Selection
  - Track Selection
  - Settings
  - Race Results
  - Championship Standings

- **Save System:**
  - Persistent unlocks
  - Best lap times
  - Race statistics

## Requirements

- Python 3.8+
- Ursina game engine

## Installation

```bash
pip install ursina
```

## Running the Game

```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| W | Accelerate |
| S | Brake/Reverse |
| A | Steer Left |
| D | Steer Right |
| Space | Drift |
| Shift | Boost |
| E | Use Item |
| ESC | Pause |

## Project Structure

```
kart-rush/
├── main.py              # Game entry point
├── src/
│   ├── core/            # Core systems
│   │   ├── game_manager.py
│   │   └── scene_manager.py
│   ├── scenes/          # UI scenes
│   │   ├── main_menu.py
│   │   ├── kart_selection.py
│   │   ├── track_selection.py
│   │   ├── results.py
│   │   ├── settings.py
│   │   ├── championship.py
│   │   └── time_trial.py
│   ├── entities/        # Game entities
│   │   └── kart.py
│   ├── systems/         # Game systems
│   ├── ui/              # UI components
│   ├── utils/           # Utilities
│   │   ├── settings.py
│   │   └── save_system.py
│   ├── tracks/          # Track definitions
│   └── assets/          # Game assets
```

## Development Status

**CURRENT PHASE: Core Implementation**

Completed:
- [x] Project structure
- [x] Settings system
- [x] Save system
- [x] Game manager
- [x] Scene manager
- [x] Main menu UI
- [x] Kart selection UI
- [x] Track selection UI
- [x] Results screen
- [x] Settings screen
- [x] Championship mode
- [x] Time trial mode
- [x] Kart entity with physics

In Progress:
- [ ] Race scene implementation
- [ ] Track creation
- [ ] AI opponents
- [ ] Power-up system
- [ ] Camera system
- [ ] HUD system
- [ ] Audio system
- [ ] VFX system

## License

MIT License
