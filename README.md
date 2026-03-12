# 🎮 Animated Werewolf / Mafia Simulation

A sophisticated AI-powered implementation of the classic Werewolf (Mafia) party game with animated visuals, intelligent AI players, and dynamic game mechanics.

![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Game Rules](#-game-rules)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Game Controls](#-game-controls)
- [How AI Works](#-how-ai-works)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [Game Flow](#-game-flow)
- [Roles Explained](#-roles-explained)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This project is an **automated simulation** of the Werewolf/Mafia party game where AI-controlled players compete against each other. The game features:

- ✅ **8 AI Players** with dynamic personalities and decision-making algorithms
- ✅ **Real-time Animations** and smooth visual transitions
- ✅ **Suspicion Mechanics** - AI players track trust and suspicion of each other
- ✅ **Natural Dialogue** - AI players speak about their reasoning and strategy
- ✅ **Tkinter GUI** - Interactive interface with scene rendering and player management
- ✅ **Intelligent Team Play** - Roles have special abilities and strategies
- ✅ **Game State Tracking** - Complete logging of votes, deaths, and events
- ✅ **Auto-play Mode** - Watch the AI play the entire game automatically

---

## 🎭 Game Rules

### Basic Concept

Werewolf (also called Mafia) is a deduction game where:
- **Good Team** (Villagers, Doctor, Detective) tries to identify and eliminate the Werewolves
- **Evil Team** (Werewolves) secretly eliminates Good players at night

### Game Structure

**Total Players: 8**
- Good Team: 5 (4 Villagers, 1 Doctor, 1 Detective)
- Evil Team: 2 (2 Werewolves)

### Game Phases

#### 🌞 DAY Phase
1. All living players are shown
2. AI players discuss and accuse each other
3. All players vote on who to eliminate
4. Player with most votes is removed from game
5. Role is revealed
6. Points awarded based on whether eliminated player was good or evil

#### 🌙 NIGHT Phase
1. Werewolves secretly choose a Good player to eliminate
2. Doctor (if alive) can protect one player
3. Detective (if alive) can investigate one player's role
4. Results are shown the next morning
5. Phase transitions to DAY

### Win Conditions

- **Good Team Wins:** All Werewolves are eliminated
- **Evil Team Wins:** Werewolves equal or outnumber Good players

---

## ✨ Features

### AI Intelligence System
- **Suspicion Tracking**: Each AI player maintains a suspicion score for every other player
- **Trust Dynamics**: Tracks how trustworthy other players seem based on behavior
- **Pattern Recognition**: AI analyzes voting patterns and speech behavior
- **Strategic Voting**: AI votes based on evidence and suspicion levels
- **Role-Based Strategy**: Different roles use different decision-making strategies

### Visual & Animation Features
- **Smooth Animations**: Player movements, death animations, vote indicators
- **Real-time Scene Rendering**: 1000x720 resolution game board
- **Dynamic Backgrounds**: Day/Night visual transitions
- **Player Avatar Display**: Visual representation of each player
- **Animated Events**: Vote arrows, shield flashes, reveal pulses
- **Color-Coded Roles**: Each role has a distinct color in the UI

### Game Features
- **Auto-play Mode**: Let the game play itself without interaction
- **Manual Control**: Step through each phase with keyboard controls
- **Game Logging**: Complete transcript of all actions and dialogue
- **Player Selection**: Click players to view their suspicion meters
- **Live Suspicion Meter**: Real-time visualization of how suspicious each player is
- **New Game**: Quick restart with randomized role assignment

---

## 🚀 Installation

### Requirements
- **Python 3.7 or higher**
- **Tkinter** (included with most Python installations)
- **Linux, macOS, or Windows** (tested on Fedora)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Parag1337/WereWolf-AI-Game.git
cd WereWolf-AI-Game
```

### Step 2: Create Virtual Environment (Recommended)

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or if no requirements file:
```bash
# No external dependencies needed - uses only Python standard library
# Make sure Tkinter is installed (python3-tk on Linux)
```

### Step 4: Add Game Assets (Optional)

The game looks for images in the `assets/` folder:
- `dayBackground.png` or `dayBackround.png` - Day phase background
- `nightBackground.png` or `nightBackround.png` - Night phase background
- `villager.png` - Villager avatar
- `werewolf.png` - Werewolf avatar
- `bonefire.png` - Bonfire decoration

---

## ⚡ Quick Start

### Run the Game

```bash
python main.py
```

A window will open with:
- **Left Panel**: Player list with avatars and alive/dead status
- **Center Panel**: Game board showing current phase, day number, and animations
- **Right Panel**: Game log and suspicion meter for selected player

### First Game
1. Press **Space** or **F5** to start the first phase
2. Watch the AI players discuss and vote
3. Continue pressing **Space** to advance through phases
4. Watch as the game unfolds

---

## 🎮 Game Controls

| Key/Button | Action | Use Case |
|-----------|--------|----------|
| **Space** or **F5** | Advance to next phase | Move game forward |
| **F6** | Toggle Auto-play | Let AI play automatically |
| **F2** | Start New Game | Reset with new roles |
| **Click Player Name** | Select player | View their suspicion meter |
| **Mouse Scroll** | Scroll game log | Read past messages |

### UI Elements

**Left Sidebar (Players)**
- Shows all 8 players with avatars
- Green highlight = alive
- Red/faded = dead
- Click to select and view suspicion

**Center Area (Game Board)**
- Current phase (DAY/NIGHT)
- Day counter
- Animated players and events
- Vote indicators and arrows
- Status messages

**Right Sidebar (Suspicion Meter)**
- List of all living players
- Suspicion bar for each (0-100%)
- Color-coded by role

**Bottom (Game Log)**
- System messages (phase changes, eliminations)
- Player dialogue (accusa tions, defenses, info)
- Vote results
- Role reveals

---

## 🤖 How AI Works

### Suspicion System

Each AI player maintains two metrics for every other player:

**Suspicion Score (0-1):**
- Increases when player's vote seems wrong
- Increases when voting patterns look coordinated
- Increases when statements contradict previous behavior
- Used to identify likely Werewolves

**Trust Score (0-1):**
- Starts at 0.5 (neutral)
- Increases for consistent, honest-seeming behavior
- Decreases for suspicious behavior
- Used to weight voting decisions

### AI Decision Making

When voting, each AI player:

1. **Analyzes all players** using suspicion/trust scores
2. **Filters candidates** - won't vote for obviously trusted players
3. **Ranks by suspicion** - most suspicious players voted first
4. **Generates dialogue** - explains their reasoning
5. **Casts vote** - based on calculated most-suspicious player

### Role-Specific Behavior

**Werewolf AI:**
- Tries to eliminate key Good players (Doctor, Detective first)
- Votes suspiciously to hide identity
- High suspicion of players who vote against werewolf team
- Defensive statements when accused

**Doctor AI:**
- Prioritizes protecting high-value targets
- Tracks threat patterns
- Uses voting information to deduce Werewolf locations
- Strategic about who to protect

**Detective AI:**
- Investigates most suspicious players first
- Uses confirmed roles to narrow down Werewolves
- Votes based on investigation results
- More confident in their voting after investigation

**Villager AI:**
- Uses voting and speech analysis only
- Builds suspicion through pattern matching
- Learns from revealed roles
- Adjusts strategy as game progresses

---

## 📁 Project Structure

```
WereWolf-AI-Game/
├── main.py                 # Game entry point
├── ui.py                   # Tkinter UI and rendering (400+ lines)
├── engine.py               # Game engine and AI logic (500+ lines)
├── models.py               # Data classes (Role, Player, Dialogue, etc.)
├── animations.py           # Animation system (vote, death, reveal, etc.)
├── config.py               # Configuration (colors, sizes, asset paths)
├── utils.py                # Utility functions (asset loading, math)
├── assets/                 # Game images and sprites
│   ├── dayBackground.png
│   ├── nightBackground.png
│   ├── villager.png
│   ├── werewolf.png
│   └── bonefire.png
├── .gitignore              # Git ignore file
├── README.md               # This file
├── PROJECT_GUIDE.md        # Detailed technical guide
├── SIMPLE_EXPLANATION.md   # Beginner-friendly explanation
└── .venv/                  # Virtual environment (excluded from git)
```

---

## 🏗️ Architecture

### Class Hierarchy

```
GameEngine
├── Manages overall game state
├── Controls phase transitions
├── Handles voting and eliminations
└── Orchestrates AI players

AIPlayer (Base Class)
├── Maintains suspicion/trust metrics
├── Generates dialogue
├── Makes voting decisions
└── Subclasses for specific roles:
    ├── WerewolfAI
    ├── DoctorAI
    ├── DetectiveAI
    └── VillagerAI

GameUI (Tkinter)
├── Renders game board
├── Manages animations
├── Handles keyboard input
├── Displays player list and log
└── Updates in real-time via root.after()

AnimationManager
├── Manages active animations
├── Updates animation state each frame
├── Renders animations to canvas
└── Handles:
    ├── VoteArrowAnimation
    ├── DeathAnimation
    ├── RevealPulseAnimation
    ├── ScanRingAnimation
    └── 6+ other animation types
```

### Data Flow

```
GameEngine
    ↓
Determines current phase (DAY/NIGHT)
    ↓
AIPlayer decides action (vote/protect/investigate)
    ↓
GameUI updates visuals
    ↓
AnimationManager creates animations
    ↓
Updates drawn to Tkinter Canvas
    ↓
Input handled via root.after() loop
```

---

## ⚙️ Configuration

All game settings are in `config.py`:

### Game Settings
- `GAME_WINDOW_SIZE` - Default window dimensions (1200x720)
- `GAME_WINDOW_MIN_SIZE` - Minimum allowed size (800x600)
- `ANIMATION_FRAME_RATE` - 60 FPS
- `AUTO_PLAY_DELAY` - Delay between auto-play phases (3 seconds)

### Colors (Dark Theme)
- `"bg"` - Main background (#171821)
- `"panel"` - Sidebar panels (#202231)
- `"text"` - Primary text color (#e7ebff)
- `"red"`, `"green"`, `"blue"` - Role colors

### Role Colors
- Villager: Light text
- Werewolf: Red (#ff6f7d)
- Doctor: Green (#72e0a1)
- Detective: Blue (#77b8ff)

### Asset Paths
Images are loaded from `assets/` directory with fallback names:
```python
ASSET_VARIANTS = {
    "day": ["dayBackground.png", "dayBackround.png"],
    "night": ["nightBackground.png", "nightBackround.png"],
    ...
}
```

---

## 🎬 Game Flow

### Turn Sequence

```
Start Game
    ↓
[DAY Phase]
  ├─ Players discuss (AI generate dialogue)
  ├─ Players vote (AI calculate suspicion)
  ├─ Most suspected player eliminated
  ├─ Role revealed
  ├─ Check win conditions
  └─ If game continues...
    ↓
[NIGHT Phase]
  ├─ Werewolves choose target
  ├─ Doctor protects player
  ├─ Detective investigates
  ├─ Results processed
  ├─ Check win conditions
  └─ Return to DAY Phase
```

### State Transitions

```
PLAYING
  ├─ [Space/F5] → Advance phase
  ├─ [F6] → Toggle auto-play
  ├─ [F2] → New game
  └─ [Click] → Select player

GOOD_VICTORY / EVIL_VICTORY
  ├─ [F2] → New game
  └─ [F5/Space] → Reset to game start
```

---

## 👥 Roles Explained

### 🌾 VILLAGER
- **Team:** Good
- **Ability:** None
- **Goal:** Vote out all Werewolves
- **Count:** 4 players
- **Strategy:** Analyze speech and voting patterns to identify Werewolves

### 🐺 WEREWOLF
- **Team:** Evil
- **Ability:** Choose a player to eliminate each night
- **Goal:** Kill all Good players or reach parity
- **Count:** 2 players
- **Strategy:** Coordinate kills, hide identity, sow distrust

### 💊 DOCTOR
- **Team:** Good
- **Ability:** Protect one player each night from werewolf kill
- **Goal:** Keep Good players alive and identify Werewolves
- **Count:** 1 player
- **Strategy:** Protect key targets, use voting to identify threats

### 🔍 DETECTIVE
- **Team:** Good
- **Ability:** Investigate one player's role each night
- **Goal:** Discover Werewolves through investigation
- **Count:** 1 player
- **Strategy:** Investigate suspicious players, use confirmed info to guide votes

---

## 📊 Scoring System

### Good Team Points
- Each eliminated Werewolf: +1 point
- Winning game: +10 bonus points

### Evil Team Points
- Each killed Good player: +1 point
- Winning game: +10 bonus points

Scores are tracked throughout the game session.

---

## 🛠️ Development

### Project Statistics
- **Lines of Code:** 1500+
- **Python Version:** 3.7+
- **Main Dependencies:** Tkinter (built-in), Python Standard Library
- **Architecture:** Object-oriented with AI pattern recognition

### Code Organization
- **ui.py** - GUI and rendering (Tkinter Canvas)
- **engine.py** - Game logic and AI decision-making
- **models.py** - Data structures (Enum, Dataclass)
- **animations.py** - Animation classes and effects
- **config.py** - Constants and configuration
- **utils.py** - Helper functions (asset loading, math)
- **main.py** - Entry point

### Key Algorithms
1. **Suspicion Calculation** - Weighted scoring based on player behavior
2. **Vote Aggregation** - Finds most-suspected player via Counter
3. **AI Dialogue Generation** - Template-based with player substitution
4. **Animation Interpolation** - Smooth transitions using easing functions

---

## 🐛 Known Issues

- Asset images are optional (game runs with placeholder colors if missing)
- AI dialogue is template-based (for performance)
- Canvas rendering may lag on very old systems
- Tkinter canvas can be slow with many simultaneous animations

### Troubleshooting

**"No module named 'tkinter'"**
```bash
# Linux (Debian/Ubuntu)
sudo apt-get install python3-tk

# Linux (Fedora)
sudo dnf install python3-tkinter

# macOS
brew install python-tk

# Windows - Reinstall Python with "tcl/tk and IDLE" checked
```

**Game window doesn't appear**
- Ensure X11 is running (on Linux with remote connection)
- Check if Tkinter is properly installed
- Try running in a different virtual environment

**No images showing**
- Add PNG files to `assets/` folder
- Check `config.py` for correct asset paths
- Game will still run without images (uses colored backgrounds)

---

## 📚 Additional Documentation

- **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** - Complete technical guide for developers
- **[SIMPLE_EXPLANATION.md](SIMPLE_EXPLANATION.md)** - Beginner-friendly game explanation
- **[Code Comments](engine.py)** - Inline documentation in source files

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with clear commit messages
4. **Test thoroughly** before submitting
5. **Submit a Pull Request** with description of changes

### Ideas for Contributions
- Additional animation types
- More sophisticated AI strategies
- Networking for multiplayer
- Sound effects and voice synthesis
- Custom role balancing
- Web version using Pygame
- Statistics and replay system

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 👨‍💻 Author

**Parag1337** - AI Game Developer

Repository: [https://github.com/Parag1337/WereWolf-AI-Game](https://github.com/Parag1337/WereWolf-AI-Game)

---

## 🙏 Acknowledgments

- Classic Werewolf/Mafia game design
- Tkinter community and documentation
- Python AI and game development resources

---

## 📞 Support

Have questions or found a bug? 

- **Open an Issue** on GitHub
- **Check the Guides** (PROJECT_GUIDE.md, SIMPLE_EXPLANATION.md)
- **Review the Code** - it's well-commented!

---

## 🎯 Future Roadmap

- [ ] Multiplayer support (networked games)
- [ ] Advanced AI strategies (machine learning)
- [ ] Sound effects and music
- [ ] Custom game configurations
- [ ] Replay/recording system
- [ ] Statistics dashboard
- [ ] Mobile version (Kivy)
- [ ] Web version (PyGame/WebGL)
- [ ] Voice synthesis for dialogue
- [ ] Advanced animation engine

---

**Enjoy the game! Watch the AI play and see if you can predict their moves.** 🎮✨
