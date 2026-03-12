# 🎮 The Werewolf Game Explained Like You're 5 Years Old

Hello! Let me explain this game to you in the SIMPLEST way possible. Let's go! 

---

## 🎭 What Is This Game? (The Story)

Imagine you're playing with a group of friends. Some of them are **good guys** 👨‍🌾 and some of them are **bad guys** 🐺.

The **bad guys** are hiding! Nobody knows who they are. 

The **good guys** need to figure out who the bad guys are and say "You're bad! You're out!"

The **bad guys** are trying to secretly get rid of the good guys at night.

**That's the whole game!**

---

## 👥 The Players (Who's Playing?)

There are **8 people** in this game:

### 🌾 The Good Team (5 people)
- **4 Villagers** - They're just regular people. They don't have any special powers.
- **1 Doctor** - This person is special! At night, they can protect ONE person from getting hurt.
- **1 Detective** - This person is special! At night, they can check if someone is good or bad.

### 🐺 The Bad Team (2 people)
- **2 Werewolves** - These are the bad guys! At night, they secretly pick a good person to get rid of.

---

## 🌞🌙 How Does a Game Day Work?

The game goes back and forth between **DAY** and **NIGHT**.

### ☀️ WHAT HAPPENS DURING THE DAY:

```
1. Everyone wakes up
2. Everyone talks (the computer people talk automatically!)
3. Everyone points fingers 👉
   "Player 3 looks suspicious!"
   "No, Player 5 is the bad guy!"
4. Everyone votes (raises their hand)
5. The person with the MOST votes is out! 
   "Player 3 is voted out!"
6. Everyone finds out if Player 3 was good or bad
```

### 🌙 WHAT HAPPENS AT NIGHT:

```
1. Everyone goes to sleep 😴
2. The Werewolves wake up (shhhhh, secret!)
3. They pick someone good to get rid of
4. The Doctor wakes up (if still alive) 
5. The Doctor picks someone to protect
6. The Detective wakes up (if still alive)
7. The Detective picks someone to check (good or bad?)
8. Everyone sleeps
```

Then the sun comes up, and it's DAY again! 🔁

---

## 🤖 What Are These AI Players?

**AI** = Artificial Intelligence = A robot that thinks and makes decisions (kinda like a video game character)

These AI players are like **puppet people** 🎭. The computer controls them!

### How Do the Robot Players Think?

Imagine you're the AI player named "Player 2". Here's what you think:

```
🤔 "Hmm, let me think about each person..."

Player 1: Makes sense, talks nicely
→ I like Player 1 ✅ (Trust = 0.9 - almost full trust!)

Player 3: Talks weird, voted wrong yesterday
→ Suspicious... (Trust = 0.3 - not much trust)

Player 5: Killed my friend yesterday (werewolf!)
→ DEFINITELY BAD! (Suspicion = 0.95 - super suspicious!)

Now I'll vote for Player 5 because they're the most suspicious!
```

---

## 🎮 How To Play (The Buttons)

When the game is running on your screen:

| Button | What Does It Do? |
|--------|-----------------|
| **Press SPACE** | Move to the next moment (skip the talking, go to voting!) |
| **Press F5** | Same as SPACE |
| **Press F6** | Let the robot people play by themselves 🤖 (Auto-play!) |
| **Press F2** | Start a brand new game |
| **Click a player's name** | Pick them! See how suspicious everyone thinks they are |

---

## 📺 What's On Your Screen?

When you play, you see THREE sections:

```
┌──────────────────────────────────────────┐
│                                          │
│  LEFT SIDE        MIDDLE          RIGHT SIDE
│  (Player list)  (Game board)    (Game log + meter)
│                                          │
│  Shows who's    Shows the players  Shows what's
│  still playing  and what they're   happening +
│                 doing (talking,     Shows how
│                 voting, dying)      suspicious
│                                    each player is
│
└──────────────────────────────────────────┘
```

---

## 🏠 The Files (The Building Blocks)

This game is made of **7 different Python files**. Think of them like LEGO blocks 🧱.

Each block does ONE job. Together, they make the whole game!

### Block 1️⃣: **main.py** (The Start Button)

```
🎬 Imagine: A big red button that says "START GAME"

This file does ONE thing:
- PRESS THE START BUTTON!
- The computer wakes up
- The game opens
- Everything begins!

That's it! Super simple!
```

**How simple?** So simple it's only 32 lines! (Smaller than this explanation!)

---

### Block 2️⃣: **config.py** (The Rules Book)

```
📖 Imagine: A book with ALL the game's settings

This file stores:
- What colors should be used? (dark colors, bright colors)
- How big should the window be? (1440 × 900 pixels)
- How fast should things move? (33 times per second)
- What colors are werewolves? (RED!)
```

**Why separate?** If you want to change a color, you don't have to hunt through the whole game - it's all RIGHT HERE!

---

### Block 3️⃣: **models.py** (The Character Sheet)

```
🎭 Imagine: A character form for video game characters

Like when you create a character in Minecraft:
- Name: Steve
- Health: 20
- Inventory: Pickaxe, Dirt
- Level: 5

This file creates templates:
- Player (who they are, what role they have)
- Role (Villager? Werewolf? Doctor? Detective?)
- Phase (Is it Day or Night?)
```

**Think of it as:** A form you fill out to describe what a player looks like.

---

### Block 4️⃣: **utils.py** (The Toolbox)

```
🛠️ Imagine: A toolbox with useful little helpers

Tools inside:
- clamp() - Keeps numbers from getting too big or small
  Example: You want a number between 0-100, not 200!
  
- lerp() - Makes smooth movements
  Example: Move from position A to position B smoothly, not jumpy
  
- ease_out_cubic() - Makes animation curves smooth
  Example: Make things slow down at the end (like a car stopping)
  
- ease_out_back() - Makes things bouncy
  Example: Make things bounce like a ball!
```

**Why separate?** These helpers are used by LOTS of other files, so we put them all in one place.

---

### Block 5️⃣: **engine.py** (The Brain)

```
🧠 Imagine: The Brain of the game

This is where ALL the smart stuff happens:
- The GameEngine is like a REFEREE 👨‍⚖️
  - Keeps score
  - Decides who's still playing
  - Says when someone is voted out
  - Checks if the game is over
  
- The AI Players are like PUPPET PEOPLE 🎭
  - Werewolf players (they kill at night)
  - Doctor player (protects someone)
  - Detective player (checks who's good/bad)
  - Villager players (just regular people)
  
  Each one THINKS and DECIDES what to do!
```

**Biggest file!** 728 lines because all the smart thinking happens here.

---

### Block 6️⃣: **animations.py** (The Special Effects)

```
✨ Imagine: A special effects studio for movies

When something happens, it gets ANIMATED:
- Speech Bubble appears and shakes ➡️ "Player 5 is suspicious!"
- Arrow flies from one player to another ➡️ "I vote for him!"
- Player fades away ➡️ "Player 3 is gone!"
- Detective's scan ring expands ➡️ "Zzzzzzzup!" (investigation)
- Banner drops down ➡️ "VILLAGERS WIN!"

All these animations are here!
```

**Why separate?** All the visual effects are together, so if you want to change how something looks, you know where to go.

---

### Block 7️⃣: **ui.py** (The Screen)

```
🖥️ Imagine: A TV screen showing the game

This file:
- Draws everything on the screen
  - Players as circles
  - Dialogue bubbles with words
  - Vote arrows between players
  - Game log showing what happened
  
- Listens to what YOU do
  - Pressed Space? I heard it!
  - Clicked a player? Got it!
  - Pressed F2? New game coming!
  
- Runs the loop that shows the game 30 times per second
  - Blink blink blink (30 times!) = Smooth animation
```

**Biggest display file!** 1061 lines because drawing all these things is complex.

---

## 🔗 How The Files Talk To Each Other

Imagine the files are people passing messages:

```
main.py says:
"Hey ui.py, wake up and start the game!"
    ↓
ui.py says:
"Okay! Let me read config.py to see what colors to use.
 Let me read engine.py to see what's happening.
 Let me read animations.py to show cool effects.
 Let me read models.py to understand the players.
 Let me read utils.py for helper tools."
    ↓
Everything works!
    ↓
You see the game on screen!
```

---

## 🎮 What Happens When You Press Space?

You press SPACE ➡️ What happens next?

```
1. You press SPACE key on keyboard ⌨️

2. ui.py hears it
   "The user pressed Space!"

3. ui.py asks engine.py
   "Hey, what happens next?
    Is it Day or Night?
    What should I show?"

4. engine.py thinks REALLY HARD
   "It's Day time! Let me make dialogue for each player.
    Player 1 says: 'Player 3 looks suspicious!'
    Player 2 votes for: Player 1
    Player 5 votes for: Player 3
    (etc.)"

5. engine.py tells ui.py all this information

6. ui.py tells animations.py
   "Okay, make a speech bubble for Player 1!
    Make an arrow from Player 2 to Player 1!
    Make an arrow from Player 5 to Player 3!"

7. animations.py creates the animations
   "I'll make these appear and disappear smoothly!"

8. ui.py draws everything on screen 30 times per second

9. You see:
   💬 Speech bubbles appearing
   ➡️ Vote arrows flying
   🎬 Smooth animations

10. Game log updates:
    "Player 1 said: Player 3 is suspicious!
     Player 2 voted for Player 1
     Player 5 voted for Player 3"
```

**All of this happens in like 1-2 seconds!** ⚡

---

## 🤖 How Does AI Think? (Super Simple Version)

Let's say YOU are an AI Werewolf. Here's how you decide who to kill:

```
At night, you think:

"Okay, who should I kill? Let me think about each good player:

Player 1 (Villager): 
  └─ Hasn't said anything weird
  └─ Seems chill
  └─ Trust level = 0.7 (medium trust)
  └─ But wait... could be bad for me to kill them

Player 2 (Villager):
  └─ Talked A LOT
  └─ Accused my werewolf friend
  └─ Trust level = 0.2 (low trust - I don't like them)
  └─ This is who I should kill! 👿

Player 3 (Doctor):
  └─ I know they're the doctor
  └─ But I don't know who they'll protect
  └─ RISKY!

Player 4 (Detective):
  └─ Haven't done much
  └─ But VERY DANGEROUS if I kill wrong person
  └─ RISKY!

DECISION: Kill Player 2! (Most suspicious, safest choice)"
```

**Simple rule the AI uses:** Pick the person who looks most like a threat!

---

## 🎪 Let Me Explain With A Story

### 📖 The Tale of the Werewolf Village

Imagine a small village with 8 people:

```
🌾 GOOD PEOPLE:
- Alice (Farmer) - Just a regular person
- Bob (Farmer) - Just a regular person  
- Charlie (Farmer) - Just a regular person
- Diana (Farmer) - Just a regular person
- Emma (Doctor) 👩‍⚕️ - Can protect someone at night
- Frank (Detective) 🔍 - Can check if someone is good/bad

🐺 WEREWOLVES:
- George 🐺
- Henry 🐺
```

### DAY 1 ☀️

```
Everyone wakes up.

Emma says: "Frank seems quiet. Maybe he's a werewolf?"
  └─ Everyone updates their suspicion of Frank

Frank says: "George voted weird yesterday. I don't trust him!"
  └─ Everyone updates their suspicion of George

Alice says: "George and Henry hang out together. That's weird!"
  └─ Everyone's suspicion of George goes UP

VOTING:
All raise hands: "Not George! Let's vote him out!"
  👋👋👋👋👋👋👋
George gets the most votes!

George is voted out!

Announcement: "George is voted out! 
              ...George was a WEREWOLF! 🐺"

Good guys cheer! 🎉
```

### NIGHT 1 🌙

```
Everyone sleeps. 😴

Henry wakes up secretly! 🐺
"Okay, I need to kill someone good or I lose.
 Let me kill... Frank! He's the detective and too dangerous!"

Frank wakes up secretly! 🔍
"Let me investigate... I'll check Emma.
 Is she good or bad?"
(Frank checks Emma - she's good)

Emma wakes up secretly! 👩‍⚕️
"I'm scared! Let me protect...
 I'll protect Frank because Henry might try to kill him!"

Result:
- Henry tries to kill Frank ❌ (but Emma protected him!)
- Frank is safe! ✅
```

### DAY 2 ☀️

```
Next morning, Frank announces:
"Emma is definitely good! I checked her!"

Everyone knows Emma is the doctor now. 

The good guys are winning! Henry is scared.

They vote out Henry. 🐺

Announcement: "All werewolves are gone!"

GOOD GUYS WIN! 🎉🎉🎉
```

---

## 🎨 What Do You See On Screen?

### At Start:
```
You see 8 players as circles on a game board
Each one has their picture (avatar) 🎭
A list of all players on the left
A game log on the right showing what's happening
```

### During Day:
```
Speech bubbles pop up! 💬
Players talk and accuse each other
"Player 5 is suspicious!"

Vote arrows appear! ➡️
Players voting - arrows show who votes for who

Text updates in log:
"Player 1 says: Player 3 seems evil!
 Player 2 votes for Player 1
 Player 5 votes for Player 3
 ...etc"
```

### During Voting Result:
```
Count the votes!
"Player 3 gets 4 votes - ELIMINATED!"

Player 3 fades away ❌
Their name gets crossed out in the list

Log shows: "Player 3 is voted out!
             Player 3 was a WEREWOLF! 🐺"
```

### During Night:
```
Screen gets darker for night time 🌙
Werewolves show as different color

Log shows:
"Night falls...
 Werewolves choose to kill...
 Doctor chooses to protect...
 Detective investigates...
 Morning comes..."

Show results:
"Player 7 was killed! 💀
 Player 2 was protected and survived! ✅
 Detective found Player 4 is GOOD! 🔍"
```

---

## 🎓 Easy version of How Computer Thinks

The computer players use a "TRUST AND SUSPICION METER":

### 💚 Trust (How much you like/believe someone)
```
0.0 ═══════════════════════════════ 1.0
Hate them                          Love them
"They're lying"                    "They're honest"
```

### 💔 Suspicion (How much you think they're evil)
```
0.0 ═══════════════════════════════ 1.0
They seem good                     They seem evil
"Probably a villager"              "Definitely a werewolf!"
```

When Player A accuses Player B:
```
AI Player X hears it and thinks:

"Hmm, did I trust Player A?
 0.8 trust = I believe them!
 So I'll increase suspicion of Player B!
 
 But if I only trust Player A at 0.2:
 0.2 trust = They're probably lying!
 So I'll DECREASE suspicion of Player B!"
```

---

## 🎬 Magic of Animation (How Things Move Smoothly)

When a speech bubble appears, here's what happens:

```
SECOND 0.0:  Bubble is at 0% done
              □ (tiny dot)

SECOND 0.3:  Bubble is at 15% done
              ◇ (getting bigger)

SECOND 0.6:  Bubble is at 30% done
              ◆ (bigger still)

SECOND 0.9:  Bubble is at 45% done
              ◊ (almost full size)

SECOND 1.2:  Bubble is at 60% done
              ⬡ (full size!)

SECOND 1.5:  Bubble is at 75% done
              ⬡ (fading away)

SECOND 1.8:  Bubble is at 90% done
              ◊ (almost gone)

SECOND 2.1:  Bubble is at 100% done
              · (completely gone)
```

The computer does this 30 times EVERY SECOND! 

That's why it looks smooth, not jumpy. 🎬✨

---

## 💾 Putting It All Together

### When You Start The Game:

```
Step 1: You run: python main.py
        └─ main.py wakes up! 🌅

Step 2: main.py says "Hey ui.py, start!"
        └─ ui.py wakes up! 👀

Step 3: ui.py reads the rulebook (config.py)
        └─ "Colors are dark blue, window is big, speed is fast"

Step 4: ui.py reads the character sheet (models.py)
        └─ "Players are circles, roles are Villager/Werewolf/etc"

Step 5: ui.py talks to engine.py
        └─ "Create 8 new players with random roles!"

Step 6: engine.py creates players randomly
        └─ "2 Werewolves, 1 Doctor, 1 Detective, 4 Villagers"

Step 7: ui.py loads pictures from the assets folder
        └─ Avatar pictures of each player

Step 8: ui.py draws everything on screen
        └─ Window opens! You see the game! 🎮

Step 9: ui.py runs its loop 30 times per second
        └─ Draw, update, check input, repeat...

Step 10: You press SPACE!
         └─ Every file works together
         └─ Things happen on screen
         └─ Game continues! 🔁
```

---

## 🏆 How The Game Ends

The game follows one of THREE endings:

### Ending 1: 🎉 GOOD GUYS WIN!
```
All Werewolves are voted out!
Good players are happy!
Game shows: "VILLAGERS WIN!"
```

### Ending 2: 😱 BAD GUYS WIN!
```
Werewolves equal or outnumber good players!
Werewolves are happy!
Game shows: "WEREWOLVES WIN!"
```

### Ending 3: ⚖️ PERFECT BALANCE!
```
Both teams... wait, there's no third ending!
It's always one of the two above.
```

---

## 🎯 Quick Quiz (Test What You Learned!)

### Question 1: What does main.py do?
Answer: Starts the game! 🎬

### Question 2: What does config.py do?
Answer: Stores all the settings and colors! 📋

### Question 3: How many Werewolves are there?
Answer: 2! 🐺🐺

### Question 4: What can the Doctor do?
Answer: Protect someone at night! 👩‍⚕️

### Question 5: What happens if you press F2?
Answer: New game starts! 🆕

### Question 6: Which file has the AI thinking?
Answer: engine.py! 🧠

### Question 7: How many times per second does the screen update?
Answer: 30 times! (33 milliseconds between each) ⚡

---

## 🌟 Cool Things To Know

### The Game is Completely Automatic!
```
You just press SPACE and watch!
The computer runs EVERYTHING:
- All 8 players make their own decisions
- All players talk
- All votes happen
- All night actions happen
- Game checks if someone won

You're just watching a movie! 🎬
(You can also press F6 and don't even have to click!)
```

### The Game Learns!
```
AI players REMEMBER what happened:
"Player 5 voted wrong last time - they're suspicious!"
"Player 2 is the Doctor - I figured it out!"
"I trust Player 1 because they're always right!"

AI gets SMARTER as the game goes! 🧠
```

### Every Game is Different!
```
Random roles!
Random guesses!
Random votes!

Play 100 times and get 100 different results! 🎲
```

---

## 🤔 If You're Still Confused...

**Remember:**
1. This is a game of hiding and guessing 👻
2. Good guys try to find bad guys ✅
3. Bad guys try to kill good guys 🐺
4. Bad guys hide who they are 🎭
5. Computer controls all players 🤖
6. YOU just watch and press Space 👀
7. Computers then do all the thinking ⚡

**That's it!** You now understand it! 🎉

---

## 🎮 Try This Right Now!

1. **Run the game:**
   ```
   python main.py
   ```

2. **Press SPACE** to start the first day

3. **Watch what happens!** See:
   - Players talk 💬
   - Arrows show votes ➡️
   - Someone gets voted out ❌
   - Game continues 🔁

4. **Press F6** to let it play automatically!
   Watch the whole game without doing anything!

5. **Press F2** to start fresh new game!

---

## 📚 File Names Explained Funny Way

```
main.py        = The "Go" button 🔴
config.py      = The "Rules" book 📖
models.py      = The "Character Sheet" 🎭
utils.py       = The "Toolbox" 🛠️
engine.py      = The "Brain" 🧠
animations.py  = The "Special Effects" ✨
ui.py          = The "Screen" 🖥️
```

---

## 🎊 You Did It!

You now understand:
✅ How the game works
✅ What each file does
✅ How AI thinks
✅ How animations work
✅ How to play
✅ How the system works together

**You're now a Werewolf Game Expert!** 🏆

Go play the game and have fun! 🎮✨

---

*The End!* 🎬

**Made for: Complete Beginners and Small Children** 👶  
**Updated: 2026**  
**Complexity Level: ⭐ VERY EASY**
