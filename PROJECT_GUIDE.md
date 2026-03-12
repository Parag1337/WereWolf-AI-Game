# 🎮 AI Werewolf Game - Complete Beginner's Guide

Welcome! This is a complete guide to understanding the **Animated Werewolf/Mafia Simulation** project. Whether you're new to coding or just new to this project, this guide will explain everything from the basics.

---

## 📋 Table of Contents

1. [Game Rules & How to Play](#game-rules--how-to-play)
2. [How to Run the Game](#how-to-run-the-game)
3. [Game Controls (All Buttons)](#game-controls-all-buttons)
4. [What Is AI in This Game?](#what-is-ai-in-this-game)
5. [Project Structure - Files Explained](#project-structure---files-explained)
6. [How the System Works (Architecture)](#how-the-system-works-architecture)
7. [Game Flow (What Happens Each Turn)](#game-flow-what-happens-each-turn)
8. [Understanding AI Behavior](#understanding-ai-behavior)

---

## 🎯 Game Rules & How to Play

### What is Werewolf/Mafia?

Werewolf (also called Mafia) is a classic party game that's now automated with AI players. Here's the basic idea:

- **Players**: 8 people playing together
- **Two Teams**: 
  - **Good Players** (Villagers, Doctor, Detective): Try to identify and vote out the Werewolves
  - **Evil Players** (Werewolves): Try to kill all the Good players

### The Game Phases

The game alternates between **DAY** and **NIGHT**:

#### 🌞 **DAY Phase**
- All living players are shown
- Players discuss and accuse each other
- Everyone votes on who to eliminate
- The player with most votes is removed from the game
- If a Werewolf is eliminated → Good team gains points
- If a Good player is eliminated → Werewolf team gains points

#### 🌙 **NIGHT Phase**
- The Werewolves secretly pick a Good player to kill
- The Doctor can protect one player (if they're alive)
- The Detective can investigate one player's role (if they're alive)
- The game shows the results next morning

### Player Roles

| Role | Team | Special Ability | Goal |
|------|------|-----------------|------|
| **Villager** | Good | None | Vote out all Werewolves |
| **Werewolf** | Evil | Can kill at night | Kill all Good players |
| **Doctor** | Good | Protect 1 player each night | Heal villagers & vote out werewolves |
| **Detective** | Good | Investigate 1 player's role | Find werewolves & vote them out |

### Win Conditions

- **Good Team Wins**: If all Werewolves are eliminated
- **Evil Team Wins**: If Werewolves equal or outnumber Good players

---

## 🚀 How to Run the Game

### Requirements
- Python 3.7 or higher
- Tkinter (usually comes with Python)

### Running the Game

```bash
# Navigate to the game folder
cd '/home/parag/Downloads/AI CP'

# Run the game
python main.py
```

A window will open showing:
- **Left Panel**: List of all players with their images
- **Center**: Game board showing players, votes, items, and animated events
- **Right Panel**: Game log of what's happening + suspicion meter for selected player

---

## 🎮 Game Controls (All Buttons)

When the game is running, you can control it with these keys:

| Button | What It Does | When to Use |
|--------|-------------|-------------|
| **Space** or **F5** | Next Phase | Move game forward (Day→Night or Night→Day) |
| **F6** | Toggle Auto Play | Let AI play automatically without clicking |
| **F2** | New Game | Restart with a fresh game |
| **Click on player name** | Select Player | View the suspicion meter for that player |

### Understanding the UI

```
┌─────────────────────────────────┐
│  LEFT SIDEBAR       CENTER       │  RIGHT SIDEBAR
│  ┌──────────┐     ┌──────────┐   │  ┌──────────┐
│  │ Player   │     │ Game     │   │  │ Game     │
│  │ List     │     │ Board    │   │  │ Log +    │
│  │          │     │ with     │   │  │ Suspicions
│  │ Show all │     │ animated │   │  │ for      │
│  │ players  │     │ events   │   │  │ selected │
│  │ & claim  │     │ & votes  │   │  │ player   │
│  └──────────┘     └──────────┘   │  └──────────┘
└─────────────────────────────────┘
```

---

## 🤖 What Is AI in This Game?

**AI** = Artificial Intelligence = Computer-controlled players that make decisions automatically.

### How AI Players Think

Instead of you controlling every player, the computer controls them. Each AI player:

1. **Listens** to what other players say
2. **Remembers** who they trust or suspect
3. **Votes** based on their suspicion level
4. **Makes decisions** at night about who to kill or protect

### AI Mechanics

- **Suspicion**: A number (0.0 to 1.0) that shows how much an AI player distrusts another
  - Low suspicion (0.2) = Trust them
  - High suspicion (0.8) = Suspect they're a Werewolf

- **Trust**: A number (0.0 to 1.0) showing how much faith they have in another player
  - Used to decide if they should believe what someone says

- **Heat**: How much "attention" an AI player is getting from accusations
  - High heat = Many people are accusing them = They're in danger of being voted out

### AI Dialogue

AI players don't just vote silently - they also speak:
- **"Player X is acting suspicious"** = They're accusing someone
- **"I swear I'm a villager!"** = They're defending themselves
- **"We need cleaner reads"** = General discussion

---

## 📁 Project Structure - Files Explained

The project is organized into 7 Python files. Think of each file as handling one job:

### 1. **main.py** (Entry Point)

**Job**: Start the game

```
🎬 What it does:
  • Creates the application window
  • Starts the game loop
  • This is THE FIRST FILE that runs
```

**Size**: 32 lines (very small!)

**Code**: 
- Imports GameUI from ui.py
- Creates a Tkinter window
- Runs the game loop

**When nothing works**: Start here to make sure Python can run the game at all.

---

### 2. **config.py** (Settings & Constants)

**Job**: Store ALL configuration values and constants in one place

```
📋 What it does:
  • Defines the color palette (what colors are used)
  • Sets window size and layout dimensions
  • Stores asset file paths and variants
  • Sets game timing (how fast animations run)
  • Defines all game-wide settings
```

**Size**: 73 lines

**Key Variables Explained**:

```python
COLORS = {
    "bg": "#171821",           # Main background (dark)
    "text": "#e7ebff",         # Text color (light)
    "red": "#ff6f7d",          # For Werewolves
    "green": "#72e0a1",        # For Doctor
    "blue": "#77b8ff",         # For Detective
    # ... 11 more colors
}

SIDEBAR_LEFT_WIDTH = 240       # Player list width (pixels)
SIDEBAR_RIGHT_WIDTH = 300      # Game log width (pixels)
ANIMATION_FRAME_RATE = 33      # Updates 30 times per second
AUTO_PLAY_DELAY = 0.9          # 0.9 second delay for auto-play
```

**Why it matters**: If you want to change colors, window size, or speed, this is where you do it.

---

### 3. **models.py** (Data Structures)

**Job**: Define the data types/classes used throughout the game

```
🏗️ What it does:
  • Creates Role enum (VILLAGER, WEREWOLF, DOCTOR, DETECTIVE)
  • Creates Phase enum (DAY, NIGHT)
  • Creates Player class (stores player info)
  • Creates Dialogue class (stores what players say)
  • Creates ScriptEvent class (stores game events)
```

**Size**: 58 lines

**Key Classes Explained**:

```python
class Player:
    id: int              # Player number (0-7)
    name: str            # Player name
    role: Role           # What role they have
    is_alive: bool       # Are they still in the game?
    claim: Optional[Role] # What role do they CLAIM to be?
    
    # Methods:
    team                 # Returns "good" or "evil"
    avatar_key           # Returns "villager" or "werewolf"
```

**Why it matters**: This defines the structure of ALL data in the game. If you want to add a new property to players, you change it here.

---

### 4. **utils.py** (Helper Functions)

**Job**: Provide useful math and utility functions

```
🛠️ What it does:
  • clamp() - Keep numbers between min and max
  • lerp() - Smooth transitions between values
  • ease_out_cubic() - Smooth animation curves
  • ease_out_back() - Bouncy animation curves
  • resolve_asset_path() - Find image files
```

**Size**: 44 lines

**Examples**:

```python
clamp(200, 0, 100)      # Returns 100 (keeps value between 0-100)
lerp(0, 100, 0.5)       # Returns 50 (halfway between 0 and 100)

# Used in animations:
# For a 1 second animation, update position:
position = lerp(start_pos, end_pos, progress)
```

**Why it matters**: These functions make animations smooth instead of jerky.

---

### 5. **engine.py** (Game Logic)

**Job**: All the AI decision-making and game rules

```
⚙️ What it does:
  • GameEngine class - Main game manager
    - Keeps track of players and game state
    - Decides what happens in each phase
    - Checks if someone won
  
  • AIPlayer classes - AI decision makers
    - Villager - Basic player
    - Werewolf - Killers at night
    - Doctor - Protectors
    - Detective - Investigators
```

**Size**: 728 lines (largest file!)

**Key Classes**:

```python
class GameEngine:
    players[]           # List of all players
    current_phase       # DAY or NIGHT?
    
    def run_day()       # Handle day phase
    def run_night()     # Handle night phase
    def check_winner()  # Is the game over?

class AIPlayer:
    suspicion{}         # How much do I suspect each player?
    trust{}             # How much do I trust each player?
    heat                # How much am I being accused?
    
    def observe_dialogue()  # Learn from what people say
    def observe_votes()     # Learn from voting patterns
    def vote_target()       # Who should I vote for?
```

**Why it matters**: This is the "brain" of the game. All AI decisions come from here.

---

### 6. **animations.py** (Visual Effects)

**Job**: All animations that show on screen

```
🎨 What it does:
  • Animation base class - Framework for animations
  • AnimationManager - Controls which animations play
  • SpeechBubbleAnimation - Dialogue bubbles appearing
  • VoteArrowAnimation - Arrow showing who voted for who
  • DeathAnimation - Player fading away
  • RevealPulseAnimation - Role reveal animation
  • And 5 more animation types...
```

**Size**: 484 lines

**How Animations Work**:

```
Animation has a duration (e.g., 1.5 seconds)
Each frame:
  ├─ Calculate progress (0.0 = start, 1.0 = finished)
  ├─ Update visual (move, fade, scale, etc.)
  └─ Continue until finished
```

**Why it matters**: Makes the game look smooth and polished instead of static.

---

### 7. **ui.py** (User Interface)

**Job**: Display the game on screen using Tkinter

```
🖥️ What it does:
  • GameUI class - Main display
    - Creates the window layout
    - Renders all graphics
    - Handles user input (clicks, keystrokes)
    - Runs the main game loop (60 FPS)
  
  • Handles:
    - Drawing players on canvas
    - Showing dialogue bubbles
    - Displaying votes
    - Updating the game log
    - Showing suspicion meter
```

**Size**: 1061 lines

**What Happens Each Frame**:

```
ui.py runs ~30 times per second:
  1. Get elapsed time (dt)
  2. Update all animations (dt seconds passed)
  3. Redraw everything on canvas
  4. Update player positions
  5. Update game log
  6. Check for user input (keyboard/mouse)
  7. Draw frame to screen
  8. Do it again!
```

**Why it matters**: This is what you SEE. Without this, the game has no graphics.

---

## 🏗️ How the System Works (Architecture)

### Import Flow (Dependency Chain)

```
main.py (Entry Point)
    ↓
ui.py (User Interface)
    ├─ Imports from: engine.py, animations.py, config.py, models.py, utils.py
    ├─→ engine.py (Game Logic)
    │       ├─ Imports from: models.py, utils.py, config.py
    │       └─ Makes all AI decisions
    │
    ├─→ animations.py (Visual Effects)
    │       ├─ Imports from: models.py, utils.py, config.py
    │       └─ Creates all visual animations
    │
    ├─→ config.py (Settings)
    │       └─ Provides all constants and colors
    │
    ├─→ models.py (Data Types)
    │       └─ Defines Player, Role, Phase, etc.
    │
    └─→ utils.py (Helper Functions)
            └─ Provides math and utility functions
```

### Data Flow (How information moves)

```
config.py ← Constants (colors, sizes)
    ↓
models.py ← Defines data structures
    ↓
utils.py ← Math helpers
    ↓
engine.py ← Reads config, models, utils → Makes game decisions
    ↓
animations.py ← Creates animations based on game events
    ↓
ui.py ← Reads ALL above → Displays game to player
```

### The Main Game Loop

```
main.py starts:
  ├─ Create window
  ├─ Create GameUI instance
  └─ Start game loop
  
GameUI initializes:
  ├─ Load images from assets folder
  ├─ Create GameEngine
  ├─ Draw the layout (left sidebar, center canvas, right sidebar)
  └─ Start animation timer
  
Every 33 milliseconds (~30 FPS):
  ├─ Update all animations
  ├─ Redraw canvas
  ├─ Update game log
  ├─ Check keyboard input
  └─ Schedule next frame
  
When player presses Space (Next Phase):
  ├─ Call engine.run_day() or engine.run_night()
  ├─ Get dialogue, events, votes from engine
  ├─ Create animations for those events
  ├─ Play animations on canvas
  └─ Update game log and player states
```

---

## 📊 Game Flow (What Happens Each Turn)

### Turn 0: Game Start

```
1. engine.py:
   ├─ Create 8 players with random roles
   │  ├─ 2 Werewolves (evil)
   │  ├─ 1 Doctor (good)
   │  ├─ 1 Detective (good)
   │  └─ 4 Villagers (good)
   └─ Initialize suspicion/trust for AI players

2. ui.py:
   ├─ Load images for each player
   ├─ Draw player circles on canvas
   ├─ Show player list in left sidebar
   └─ Show game log entry "Game started" in right sidebar
```

### Turn 1: First Day Phase

```
1. Player clicks Space → ui.py calls engine.run_day()

2. engine.py (AI Discussion):
   ├─ Each living AI player:
   │  ├─ Creates dialogue ("X seems suspicious")
   │  ├─ AI calculates whom to vote for
   │  └─ Returns Dialogue object with their speech
   └─ Creates list of ScriptEvents

3. ui.py (Animation & Display):
   ├─ For each dialogue in engine's events:
   │  ├─ Create SpeechBubbleAnimation
   │  └─ Show animation on canvas (speech bubble appears, waves, fades)
   │
   ├─ Create game log entry showing who said what
   │
   └─ For each vote:
       ├─ Create VoteArrowAnimation
       └─ Show arrow from voter to target on canvas

4. engine.py (Calculate Vote Result):
   ├─ Count votes (who voted for whom)
   ├─ Eliminate player with most votes
   ├─ Announce elimination in game log
   └─ Check if good team won (all werewolves dead)

5. ui.py (Update Display):
   ├─ Mark eliminated player as dead (cross icon)
   ├─ Create DeathAnimation
   └─ Show in log: "Player X was voted out"
```

### Turn 2: First Night Phase

```
1. Player clicks Space → ui.py calls engine.run_night()

2. engine.py (Werewolf Kill):
   ├─ Find all living werewolves
   ├─ Each werewolf:
   │  ├─ Selects a living good player to kill
   │  └─ Returns kill action
   └─ Creates ScriptEvent for the kill

3. engine.py (Doctor Protect):
   ├─ Find the doctor (if alive)
   └─ Doctor:
       ├─ Selects a player to protect
       └─ Returns protection action

4. engine.py (Detective Investigate):
   ├─ Find the detective (if alive)
   └─ Detective:
       ├─ Selects a player to investigate
       ├─ Reveals their role (only to detective)
       └─ Returns investigation result

5. engine.py (Resolve Night):
   ├─ If werewolf's target ≠ doctor's protection → Kill happens
   ├─ Announce deaths
   └─ Check if evil team won (werewolves ≥ good players)

6. ui.py (Animate & Display):
   ├─ Show kill animations
   ├─ Show protection shield animation (if saved)
   ├─ Show investigation scan animation
   └─ Update game log with results
```

### Turn 3: Day Phase 2

```
Repeat Turn 1 pattern...
```

### Game End

```
When one team wins:

1. engine.check_winner() returns winner

2. ui.py:
   ├─ Create WinnerBannerAnimation
   ├─ Display "Werewolves Win!" or "Villagers Win!"
   ├─ Show final statistics
   └─ Game state: GAME_OVER
```

---

## 🧠 Understanding AI Behavior

### AI Decision-Making Process

Each AI player makes decisions based on **4 factors**:

#### 1. **Suspicion Values** (0.0 to 1.0)

```
Suspicion increases when:
  ├─ Someone accuses them
  ├─ They vote wrong (for innocent when werewolf died)
  ├─ They defend a werewolf
  └─ They seem too quiet (not participating)

Suspicion is used to decide:
  ├─ Who to vote for (highest suspicion)
  ├─ Who might be a werewolf
  └─ Who could be a threat
```

**Example**:
```
Player A: suspicion = 0.2  (trusted, probably good)
Player B: suspicion = 0.7  (suspicious, might be werewolf)
Player C: suspicion = 0.9  (very suspicious, targeted for voting)
```

#### 2. **Trust Values** (0.0 to 1.0)

```
How much an AI player believes what another player says.

High trust (0.8):
  └─ "If they accuse someone, that person is probably bad"

Low trust (0.2):
  └─ "If they accuse someone, they're probably lying"
```

#### 3. **Heat** (attention from accusations)

```
Heat increases when:
  └─ Other players accuse you

High heat means:
  └─ You're likely to be voted out
  └─ AI might defend themselves
```

#### 4. **Known Roles**

```
AI players learn roles through:
  ├─ Detective reveals
  ├─ Player claims ("I'm the doctor!")
  └─ Role reveals when voted out
```

### Example AI Thought Process

```
🤖 Werewolf's turn to vote:

1. Check all living players
2. For each player, calculate:
   suspicion = my trust level of accuser × accuser's track record
3. Vote for player with highest suspicion
4. BUT if I'm the one with high heat:
   └─ Vote for someone else to deflect attention
```

### Dialogue System

AI players don't vote silently - they explain their reasoning:

```python
If AI is accusing:
  └─ Dialogue: "Player X is acting suspicious"
    └─ Others update suspicion of Player X

If AI is defending:
  └─ Dialogue: "I swear I'm a villager!"
    └─ Reduces accuser's trust in that AI

If AI is discussing:
  └─ Dialogue: "Look at who is steering the table"
    └─ General information that influences voting
```

---

## 🎬 Animation System

### How Animations Work

```
1. engine.py creates a ScriptEvent:
   └─ ScriptEvent(at=0.5, kind="speech", payload={...})

2. ui.py reads the event:
   └─ dispatcher converts event to Animation object

3. AnimationManager plays animation:
   ├─ Animation starts (setup)
   ├─ Each frame updates:
   │  └─ progress = elapsed_time / duration
   │  └─ update(ui, progress)
   └─ Animation finishes

4. Visuals appear on canvas:
   └─ Dialogue bubble, vote arrow, death icon, etc.
```

### Animation Types

```
SpeechBubbleAnimation (1.9 seconds)
  ├─ Bubble appears, scales up
  ├─ Text fades in
  ├─ Shows for a while
  └─ Fades away

VoteArrowAnimation (0.6 seconds)
  ├─ Arrow appears between voter and target
  ├─ Pulses and animates
  └─ Disappears

DeathAnimation (1.0 second)
  ├─ Player fades to gray
  ├─ Death cross appears
  └─ Player marked as dead

DetectiveRevealAnimation (0.8 seconds)
  ├─ Scan ring expands
  ├─ Role popup appears
  └─ Fades out
```

---

## 💡 Tips for Understanding the Code

### If you want to...

**Change game colors**:
→ Edit `config.py` - the `COLORS` dictionary

**Change window size**:
→ Edit `config.py` - `SIDEBAR_LEFT_WIDTH`, `SIDEBAR_RIGHT_WIDTH`, etc.

**Make game faster/slower**:
→ Edit `config.py` - `ANIMATION_FRAME_RATE`

**Understand a player's suspicion**:
→ Look in `engine.py` - `AIPlayer.suspicion` dictionary

**Add new dialogue**:
→ Edit `engine.py` - Add lines to `accuse_lines`, `defend_lines`, etc.

**Change how votes are calculated**:
→ Edit `engine.py` - `vote_target()` method

**Add new animations**:
→ Edit `animations.py` - Create new `Animation` subclass

**Change UI layout**:
→ Edit `ui.py` - `_build_layout()` method

**Add new player roles**:
→ Edit `models.py` - Add to `Role` enum
→ Then implement in `engine.py` as new `AIPlayer` subclass

---

## 📚 Summary: The Complete Picture

```
Think of the project like a movie production:

📋 CONFIG.PY = Script notes (colors, timing, sizes)
🏗️ MODELS.PY = Character definitions (Player, Role, etc.)
🛠️ UTILS.PY = Tools (math functions, helpers)
⚙️ ENGINE.PY = Director & Actors (decides what happens, AI choices)
🎨 ANIMATIONS.PY = Special effects (visual animations)
🖥️ UI.PY = Camera & Filming crew (displays everything)
🎬 MAIN.PY = Producer (starts the whole thing)
```

**When you run the game**:

```
main.py (producer) starts the show
    ↓
ui.py (camera crew) learns the script from config.py
    ↓
engine.py (director) makes moment-to-moment decisions
    ↓
animations.py (special effects) creates visual magic
    ↓
ui.py (camera) displays everything on screen
    ↓
Players see an animated werewolf game!
```

---

## 🚀 Next Steps

1. **Run the game**: `python main.py`
2. **Play a few rounds** to understand the game flow
3. **Read one file at a time** - start with `config.py` (smallest)
4. **Modify something small** - change a color or player count
5. **Understand the changes** - see how it affects the game
6. **Explore the code** - find the functions that interest you

---

## ❓ Quick Reference

### Key Terms

- **Phase**: DAY or NIGHT period
- **Suspicion**: How much an AI distrusts another (0.0-1.0)
- **Dialogue**: What an AI player says
- **ScriptEvent**: An event that happens in the game
- **Animation**: A visual effect that plays
- **Canvas**: The main game board area
- **Token/FPS**: How many times per second the screen updates

### File Sizes

```
main.py:        32 lines    (entry point)
config.py:      73 lines    (settings)
models.py:      58 lines    (data types)
utils.py:       44 lines    (helpers)
animations.py:  484 lines   (visual effects)
engine.py:      728 lines   (game logic & AI)
ui.py:          1061 lines  (display)
────────────────────────
Total:          2480 lines
```

### Control Keys

| Key | Action |
|-----|--------|
| **Space** or **F5** | Next Phase |
| **F6** | Auto Play |
| **F2** | New Game |
| **Click Player Name** | Select/Deselect |

---

## 🎓 Learning Resources in Code

Each file has a docstring at the top explaining what it does:

```python
"""
This is a docstring.
It explains what the file does.
"""
```

Read these first - they give a quick overview!

---

**Good luck exploring the code! Have fun! 🎮✨**

---

*Last Updated: 2026*  
*This guide matches the refactored 7-module architecture*
