"""
Game UI and rendering for the Werewolf game.
"""

import math
import time
import tkinter as tk
from collections import defaultdict
from tkinter import ttk
from typing import Dict, Optional, Tuple

from animations import (
    AnimationManager,
    BackgroundTransitionAnimation,
    DeathAnimation,
    MovingIconAnimation,
    RevealPulseAnimation,
    ScanRingAnimation,
    ShieldFlashAnimation,
    SpeechBubbleAnimation,
    VoteArrowAnimation,
    WinnerBannerAnimation,
)
from config import (
    ANIMATION_FRAME_RATE,
    AUTO_PLAY_DELAY,
    COLORS,
    GAME_WINDOW_MIN_SIZE,
    GAME_WINDOW_SIZE,
    LOG_TAGS,
    ROLE_COLORS,
    SIDEBAR_LEFT_WIDTH,
    SIDEBAR_RIGHT_WIDTH,
)
from engine import GameEngine
from models import Dialogue, Phase, ScriptEvent
from utils import clamp, resolve_asset_path


class GameUI:
    """Main UI for the game."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Animated Werewolf / Mafia Simulation")
        self.root.geometry(GAME_WINDOW_SIZE)
        self.root.minsize(*GAME_WINDOW_MIN_SIZE)
        self.root.configure(bg=COLORS["bg"])

        self.engine = GameEngine(8)
        self.animations = AnimationManager()
        self.script: list[ScriptEvent] = []
        self.script_index = 0
        self.script_elapsed = 0.0
        self.is_busy = False
        self.auto_play = False
        self.auto_delay = AUTO_PLAY_DELAY
        self.next_auto_time = 0.0
        self.frame_time = time.perf_counter()
        self.display_phase = self.engine.phase
        self.display_day = self.engine.day_number
        self.focus_player_id = 1
        self.scene_size = (1000, 720)

        self.images: Dict[str, tk.PhotoImage] = {}
        self.scene_image_cache: Dict[Tuple[str, int, int], tk.PhotoImage] = {}
        self.player_rows: Dict[int, Dict[str, tk.Widget]] = {}
        self.player_nodes: Dict[int, Dict[str, int]] = {}
        self.player_positions: Dict[int, Tuple[float, float]] = {}
        self.death_progress: Dict[int, float] = defaultdict(float)

        self.phase_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self._load_images()
        self._build_layout()
        self._build_scene()
        self._build_player_list()
        self.set_display_phase(self.display_phase, self.display_day)
        self._refresh_player_list()
        self._refresh_suspicion_meter()
        self.log(
            "Animated game ready. Press Next Phase to start the scene.", "system"
        )

        self.root.bind("<F5>", lambda _e: self.next_phase())
        self.root.bind("<F6>", lambda _e: self.toggle_auto())
        self.root.bind("<F2>", lambda _e: self.new_game())
        self.root.bind("<space>", lambda _e: self.next_phase())

        self._loop()

    def _load_images(self) -> None:
        """Load all game images."""
        import config

        for key in config.ASSET_VARIANTS:
            path = resolve_asset_path(key)
            if path is None:
                continue
            self.images[f"{key}_raw"] = tk.PhotoImage(file=path)

        if "villager_raw" in self.images:
            self.images["villager_small"] = self._resize_photo(
                self.images["villager_raw"], 48, 48
            )
        if "werewolf_raw" in self.images:
            self.images["werewolf_small"] = self._resize_photo(
                self.images["werewolf_raw"], 48, 48
            )
        if "bonefire_raw" in self.images:
            self.images["bonefire_scene"] = self._resize_photo(
                self.images["bonefire_raw"], 80, 80
            )

    @staticmethod
    def _resize_photo(
        image: tk.PhotoImage, target_w: int, target_h: int
    ) -> tk.PhotoImage:
        """Resize a PhotoImage using zoom and subsample."""
        target_w = max(1, int(target_w))
        target_h = max(1, int(target_h))
        precision = 12
        x_zoom = max(1, int(round(target_w / image.width() * precision)))
        y_zoom = max(1, int(round(target_h / image.height() * precision)))
        return image.zoom(x_zoom, y_zoom).subsample(precision, precision)

    def _scene_image(
        self, key: str, width: int, height: int
    ) -> Optional[tk.PhotoImage]:
        """Get or create a cached scaled image for the scene."""
        raw = self.images.get(f"{key}_raw")
        if raw is None:
            return None
        cache_key = (key, max(1, int(width)), max(1, int(height)))
        if cache_key not in self.scene_image_cache:
            self.scene_image_cache[cache_key] = self._resize_photo(
                raw, cache_key[1], cache_key[2]
            )
        return self.scene_image_cache[cache_key]

    def _scene_dimensions(self) -> Tuple[int, int]:
        """Get current canvas dimensions."""
        width = max(1, self.scene.winfo_width())
        height = max(1, self.scene.winfo_height())
        return width, height

    def _on_scene_resize(self, event) -> None:
        """Handle canvas resize events."""
        width = max(1, int(event.width))
        height = max(1, int(event.height))
        if (width, height) == self.scene_size:
            return
        self.scene_size = (width, height)
        self.scene_image_cache.clear()
        self.scene.coords(
            self.overlay_gradient, 0, 0, width, height
        )
        self.set_display_phase(self.display_phase, self.display_day)

    def _build_layout(self) -> None:
        """Build the UI layout."""
        # Top bar
        top = tk.Frame(self.root, bg=COLORS["panel"], height=56)
        top.pack(fill=tk.X)
        top.pack_propagate(False)

        tk.Label(
            top,
            text="Werewolf Village",
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=("Segoe UI", 18, "bold"),
        ).pack(side=tk.LEFT, padx=18)
        tk.Label(
            top,
            textvariable=self.phase_var,
            bg=COLORS["panel"],
            fg=COLORS["yellow"],
            font=("Consolas", 14, "bold"),
        ).pack(side=tk.LEFT, padx=10)
        tk.Label(
            top,
            textvariable=self.day_var,
            bg=COLORS["panel"],
            fg=COLORS["cyan"],
            font=("Consolas", 14, "bold"),
        ).pack(side=tk.LEFT)
        tk.Label(
            top,
            textvariable=self.status_var,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(side=tk.RIGHT, padx=16)

        # Body (three columns)
        body = tk.Frame(self.root, bg=COLORS["bg"])
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Left sidebar
        left = tk.Frame(body, bg=COLORS["panel2"], width=SIDEBAR_LEFT_WIDTH)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        # Right sidebar
        right = tk.Frame(body, bg=COLORS["panel2"], width=SIDEBAR_RIGHT_WIDTH)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)

        # Center (expandable)
        center = tk.Frame(body, bg=COLORS["bg"])
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12)

        # Left sidebar content
        tk.Label(
            left,
            text="Players",
            bg=COLORS["panel2"],
            fg=COLORS["text"],
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 8))
        self.player_list_frame = tk.Frame(left, bg=COLORS["panel2"])
        self.player_list_frame.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=(0, 10)
        )

        # Right sidebar content
        tk.Label(
            right,
            text="Game Log",
            bg=COLORS["panel2"],
            fg=COLORS["text"],
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 8))
        self.log_text = tk.Text(
            right,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            relief=tk.FLAT,
            height=18,
            wrap=tk.WORD,
            padx=10,
            pady=10,
            state=tk.DISABLED,
            font=("Consolas", 11),
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        for tag, color in LOG_TAGS.items():
            self.log_text.tag_configure(tag, foreground=color)

        meter_frame = tk.Frame(right, bg=COLORS["panel2"])
        meter_frame.pack(fill=tk.X, padx=12, pady=12)
        self.meter_title = tk.Label(
            meter_frame,
            text="Suspicion Meter",
            bg=COLORS["panel2"],
            fg=COLORS["text"],
            font=("Segoe UI", 12, "bold"),
        )
        self.meter_title.pack(anchor="w")
        self.suspicion_canvas = tk.Canvas(
            meter_frame,
            width=276,
            height=250,
            bg=COLORS["surface"],
            highlightthickness=0,
        )
        self.suspicion_canvas.pack(fill=tk.X, pady=(8, 0))

        # Center scene
        self.scene = tk.Canvas(
            center, bg=COLORS["black"], highlightthickness=0
        )
        self.scene.pack(fill=tk.BOTH, expand=True)
        self.scene.bind("<Configure>", self._on_scene_resize)

        # Bottom bar
        bottom = tk.Frame(self.root, bg=COLORS["panel"], height=72)
        bottom.pack(fill=tk.X, padx=12, pady=(0, 12))
        bottom.pack_propagate(False)

        self.next_button = tk.Button(
            bottom,
            text="Next Phase  F5",
            command=self.next_phase,
            bg=COLORS["blue"],
            fg=COLORS["black"],
            relief=tk.FLAT,
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=10,
        )
        self.next_button.pack(side=tk.LEFT, padx=(14, 8), pady=12)

        self.auto_button = tk.Button(
            bottom,
            text="Auto Play  F6",
            command=self.toggle_auto,
            bg=COLORS["green"],
            fg=COLORS["black"],
            relief=tk.FLAT,
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=10,
        )
        self.auto_button.pack(side=tk.LEFT, padx=8, pady=12)

        self.new_button = tk.Button(
            bottom,
            text="New Game  F2",
            command=self.new_game,
            bg=COLORS["surface2"],
            fg=COLORS["text"],
            relief=tk.FLAT,
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=10,
        )
        self.new_button.pack(side=tk.LEFT, padx=8, pady=12)

        ttk.Label(
            bottom,
            text="Animated game loop uses root.after()",
            background=COLORS["panel"],
            foreground=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(side=tk.RIGHT, padx=16)

    def _build_scene(self) -> None:
        """Build the canvas scene."""
        self.scene.delete("all")
        scene_w, scene_h = self._scene_dimensions()
        self.scene_size = (scene_w, scene_h)
        self.background_id = self.scene.create_image(scene_w / 2, scene_h / 2)
        self.overlay_gradient = self.scene.create_rectangle(
            0, 0, scene_w, scene_h, fill="#000000", stipple="gray25", outline=""
        )

        self.ground_id = self.scene.create_oval(
            0, 0, 0, 0, fill="#2d2e24", outline=""
        )
        self.fire_glow_outer = self.scene.create_oval(
            0, 0, 0, 0, fill="#9f4a1a", outline=""
        )
        self.fire_glow_inner = self.scene.create_oval(
            0, 0, 0, 0, fill="#ffb04d", outline=""
        )
        self.fire_id = self.scene.create_polygon(
            0, 0, 0, 0, 0, 0, 0, 0, fill="#ffd36b", outline=""
        )
        self.fire_core = self.scene.create_polygon(
            0, 0, 0, 0, 0, 0, 0, 0, fill="#fff0a8", outline=""
        )
        self.bonefire_id = self.scene.create_image(0, 0)
        self.log_base = self.scene.create_rectangle(
            0, 0, 0, 0, fill="#56311d", outline=""
        )
        self.log_1 = self.scene.create_line(
            0, 0, 0, 0, fill="#704428", width=6
        )
        self.log_2 = self.scene.create_line(
            0, 0, 0, 0, fill="#704428", width=6
        )

        self.player_nodes.clear()
        self.player_positions.clear()
        for pid in self.engine.players:
            shadow = self.scene.create_oval(
                0, 0, 0, 0, fill="#101115", outline=""
            )
            ring = self.scene.create_oval(
                0, 0, 0, 0, outline=COLORS["muted"], width=2
            )
            image = self.scene.create_image(0, 0)
            tint = self.scene.create_oval(
                0,
                0,
                0,
                0,
                fill="#a6a6a6",
                stipple="gray12",
                outline="",
            )
            cross1 = self.scene.create_line(
                0, 0, 0, 0, fill=COLORS["red"], width=6
            )
            cross2 = self.scene.create_line(
                0, 0, 0, 0, fill=COLORS["red"], width=6
            )
            label = self.scene.create_text(
                0,
                0,
                text="",
                fill=COLORS["text"],
                font=("Segoe UI", 11, "bold"),
            )
            state = self.scene.create_text(
                0,
                0,
                text="",
                fill=COLORS["green"],
                font=("Consolas", 10, "bold"),
            )
            indicator = self.scene.create_oval(
                0, 0, 0, 0, fill=COLORS["green"], outline=""
            )
            self.player_nodes[pid] = {
                "shadow": shadow,
                "ring": ring,
                "image": image,
                "tint": tint,
                "cross1": cross1,
                "cross2": cross2,
                "label": label,
                "state": state,
                "indicator": indicator,
            }

    def _build_player_list(self) -> None:
        """Build the player list sidebar."""
        for child in self.player_list_frame.winfo_children():
            child.destroy()
        self.player_rows.clear()

        for player_id, player in self.engine.players.items():
            row = tk.Frame(
                self.player_list_frame, bg=COLORS["surface"], cursor="hand2"
            )
            row.pack(fill=tk.X, pady=8, padx=0)

            # Avatar (48x48)
            icon_image = self.images.get(f"{player.avatar_key}_small")
            icon_label = tk.Label(
                row,
                image=icon_image,
                bg=COLORS["surface"],
                width=48,
                height=48,
            )
            icon_label.image = icon_image
            icon_label.pack(side=tk.LEFT, padx=(8, 10), pady=0)

            # Text block (2 lines: Player Name / Role)
            text_block = tk.Frame(row, bg=COLORS["surface"])
            text_block.pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, pady=0
            )

            name_label = tk.Label(
                text_block,
                text=player.name,
                bg=COLORS["surface"],
                fg=COLORS["text"],
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                wraplength=150,
            )
            name_label.pack(fill=tk.X, anchor="w")

            detail_label = tk.Label(
                text_block,
                text="",
                bg=COLORS["surface"],
                fg=COLORS["muted"],
                anchor="w",
                font=("Consolas", 10),
                wraplength=150,
            )
            detail_label.pack(fill=tk.X, anchor="w")

            for widget in (
                row,
                icon_label,
                text_block,
                name_label,
                detail_label,
            ):
                widget.bind(
                    "<Button-1>",
                    lambda _e, pid=player_id: self.select_player(pid),
                )

            self.player_rows[player_id] = {
                "row": row,
                "name": name_label,
                "detail": detail_label,
            }

    def select_player(self, player_id: int) -> None:
        """Select a player to focus on."""
        self.focus_player_id = player_id
        self._refresh_player_list()
        self._refresh_suspicion_meter()

    def log(self, text: str, tag: str = "system") -> None:
        """Add text to the game log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def set_display_phase(
        self, phase: Phase, day_number: int
    ) -> None:
        """Set the displayed phase and update background."""
        self.display_phase = phase
        self.display_day = day_number
        self.phase_var.set(f"Phase: {phase.value}")
        self.day_var.set(f"Day: {day_number}")
        self.status_var.set(
            "Busy animating" if self.is_busy else "Ready"
        )
        scene_w, scene_h = self._scene_dimensions()
        self.scene.coords(self.background_id, scene_w / 2, scene_h / 2)
        image = self._scene_image(
            "day" if phase == Phase.DAY else "night",
            scene_w,
            scene_h,
        )
        if image is not None:
            self.scene.itemconfigure(self.background_id, image=image)
            self.scene.image = image
        else:
            fallback = "#43381f" if phase == Phase.DAY else "#14203a"
            self.scene.configure(bg=fallback)

    def new_game(self) -> None:
        """Start a new game."""
        self.engine = GameEngine(8)
        self.animations = AnimationManager()
        self.script = []
        self.script_index = 0
        self.script_elapsed = 0.0
        self.is_busy = False
        self.auto_play = False
        self.death_progress = defaultdict(float)
        self.display_phase = self.engine.phase
        self.display_day = self.engine.day_number
        self.focus_player_id = 1
        self.scene_image_cache.clear()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        self._build_scene()
        self._build_player_list()
        self.set_display_phase(self.display_phase, self.display_day)
        self._refresh_player_list()
        self._refresh_suspicion_meter()
        self.log("New animated match started.", "system")
        self._sync_buttons()

    def toggle_auto(self) -> None:
        """Toggle auto play."""
        self.auto_play = not self.auto_play
        self.next_auto_time = time.perf_counter() + self.auto_delay
        self._sync_buttons()

    def _sync_buttons(self) -> None:
        """Update button states."""
        self.auto_button.config(
            text="Stop Auto  F6" if self.auto_play else "Auto Play  F6",
            bg=COLORS["orange"] if self.auto_play else COLORS["green"],
        )
        self.next_button.config(
            state=tk.DISABLED if self.is_busy else tk.NORMAL
        )
        self.status_var.set(
            "Busy animating" if self.is_busy else "Ready"
        )

    def next_phase(self) -> None:
        """Advance to next game phase."""
        if self.is_busy or self.engine.winner:
            return
        self.script = self.engine.advance_phase()
        self.script_index = 0
        self.script_elapsed = 0.0
        self.is_busy = True
        self._sync_buttons()
        self._refresh_suspicion_meter()

    def _dispatch_event(self, event: ScriptEvent) -> None:
        """Process a game event and create animations."""
        kind = event.kind
        payload = event.payload

        if kind == "speech":
            dialogue: Dialogue = payload["dialogue"]  # type: ignore
            speaker = self.engine.players[dialogue.speaker_id].name
            self.log(
                f"{speaker}: {dialogue.text}",
                dialogue.kind if dialogue.kind in LOG_TAGS else "speech",
            )
            self.animations.add(
                SpeechBubbleAnimation(
                    dialogue.speaker_id, dialogue.text, dialogue.kind
                )
            )
        elif kind == "vote":
            voter_id = int(payload["voter"])
            target_id = int(payload["target"])
            self.log(
                f"Player {voter_id} votes for Player {target_id}.",
                "vote",
            )
            self.animations.add(VoteArrowAnimation(voter_id, target_id))
        elif kind == "kill_move":
            source_id = int(payload["source"])
            target_id = int(payload["target"])
            self.log(
                f"The werewolves stalk Player {target_id} in the dark.",
                "kill",
            )
            self.animations.add(
                MovingIconAnimation(
                    source_id,
                    target_id,
                    self.images.get("werewolf_effect"),
                )
            )
        elif kind == "shield":
            target_id = int(payload["target"])
            if payload.get("saved"):
                self.log(
                    f"A doctor shield wraps around Player {target_id}.",
                    "save",
                )
            self.animations.add(ShieldFlashAnimation(target_id))
        elif kind == "scan":
            target_id = int(payload["target"])
            result = "Werewolf" if payload.get("is_werewolf") else "Not Werewolf"
            self.log(
                f"Detective scans Player {target_id}: {result}.",
                "reveal",
            )
            self.animations.add(ScanRingAnimation(target_id))
        elif kind == "death":
            player_id = int(payload["player"])
            reason = payload.get("reason", "")
            if reason == "night":
                self.log(f"Player {player_id} falls during the night.", "kill")
            else:
                self.log(
                    f"The village eliminates Player {player_id}.",
                    "vote",
                )
            self.animations.add(DeathAnimation(player_id))
        elif kind == "reveal":
            player_id = int(payload["player"])
            role = payload["role"]  # type: ignore
            self.log(f"Player {player_id} was {role.value}.", "reveal")
            self.animations.add(RevealPulseAnimation(player_id, role))
        elif kind == "phase_transition":
            phase: Phase = payload["phase"]  # type: ignore
            day_number = int(payload["day"])
            self.animations.add(
                BackgroundTransitionAnimation(phase, day_number)
            )
        elif kind == "winner":
            winner = str(payload["winner"])
            self.log(f"{winner} win the match.", "system")
            self.animations.add(WinnerBannerAnimation(winner))
        elif kind == "log":
            self.log(
                str(payload["text"]),
                str(payload.get("tag", "system")),
            )

    def _process_script(self, dt: float) -> None:
        """Process game script events."""
        if not self.is_busy:
            return

        self.script_elapsed += dt
        while (
            self.script_index < len(self.script)
            and self.script[self.script_index].at <= self.script_elapsed
        ):
            self._dispatch_event(self.script[self.script_index])
            self.script_index += 1

        if (
            self.script_index >= len(self.script)
            and not self.animations.active()
        ):
            self.is_busy = False
            self._sync_buttons()
            self._refresh_player_list()
            self._refresh_suspicion_meter()

    def player_position(self, player_id: int) -> Tuple[float, float]:
        """Get a player's position on the scene."""
        return self.player_positions.get(player_id, (430.0, 320.0))

    def _refresh_player_list(self) -> None:
        """Update player list display."""
        for player_id, widgets in self.player_rows.items():
            player = self.engine.players[player_id]
            focused = player_id == self.focus_player_id
            bg = COLORS["surface2"] if focused else COLORS["surface"]
            widgets["row"].config(bg=bg)
            widgets["name"].config(
                bg=bg,
                fg=ROLE_COLORS.get(player.role.value, COLORS["text"]),
            )
            widgets["detail"].config(bg=bg)

            role_text = self.engine.visible_role(player_id)
            status_text = "ALIVE" if player.is_alive else "DEAD"
            status_color = COLORS["green"] if player.is_alive else COLORS["red"]
            widgets["detail"].config(
                text=f"{role_text}\n{status_text}",
                fg=status_color,
            )

    def _refresh_suspicion_meter(self) -> None:
        """Update suspicion meter display."""
        canvas = self.suspicion_canvas
        canvas.delete("all")
        focus_player = self.engine.players.get(self.focus_player_id)
        if focus_player is None:
            return

        if focus_player.is_alive:
            source_ai = self.engine.ai[self.focus_player_id]
            title = f"Perspective: {focus_player.name}"
            bars = [
                (pid, source_ai.suspicion.get(pid, 0.0))
                for pid in self.engine.players
                if pid != self.focus_player_id
            ]
        else:
            title = "Perspective: Average table pressure"
            bars = [
                (pid, self.engine.average_suspicion(pid))
                for pid in self.engine.players
                if pid != self.focus_player_id
            ]

        self.meter_title.config(text=title)
        bars.sort(key=lambda item: item[1], reverse=True)

        top = 18
        for index, (player_id, suspicion) in enumerate(bars[:8]):
            player = self.engine.players[player_id]
            y = top + index * 28
            canvas.create_text(
                16,
                y,
                anchor="w",
                text=f"P{player_id}",
                fill=ROLE_COLORS[player.role.value],
                font=("Consolas", 10, "bold"),
            )
            canvas.create_rectangle(
                72, y - 8, 250, y + 8, fill="#1a1c28", outline=""
            )
            fill = (
                COLORS["green"]
                if suspicion < 0.35
                else COLORS["yellow"]
                if suspicion < 0.60
                else COLORS["red"]
            )
            canvas.create_rectangle(
                72,
                y - 8,
                72 + 178 * clamp(suspicion),
                y + 8,
                fill=fill,
                outline="",
            )
            canvas.create_text(
                282,
                y,
                anchor="e",
                text=f"{suspicion:.0%}",
                fill=fill,
                font=("Consolas", 10, "bold"),
            )

    def _update_scene(self, dt: float) -> None:
        """Update canvas scene rendering."""
        self.animations.update(self, dt)

        scene_w, scene_h = self._scene_dimensions()
        center_x = scene_w / 2
        center_y = scene_h * 0.53
        count = len(self.engine.players)
        radius = max(120, min(scene_w, scene_h) * 0.34)
        avatar_size = int(
            clamp(min(scene_w, scene_h) / 8.5, 56, 108)
        )
        ring_radius = avatar_size / 2 + 10
        shadow_width = avatar_size * 0.55
        shadow_height = avatar_size * 0.14
        now = time.perf_counter()

        ground_rx = radius * 1.1
        ground_ry = radius * 0.92
        self.scene.coords(
            self.ground_id,
            center_x - ground_rx,
            center_y - ground_ry,
            center_x + ground_rx,
            center_y + ground_ry,
        )
        self.scene.coords(
            self.overlay_gradient, 0, 0, scene_w, scene_h
        )

        flicker = 6 * math.sin(now * 8.0)
        fire_outer = max(42, avatar_size * 0.72)
        fire_inner = fire_outer * 0.62
        fire_top = center_y - avatar_size * 0.95
        fire_bottom = center_y - avatar_size * 0.12
        self.scene.coords(
            self.fire_glow_outer,
            center_x - fire_outer - flicker,
            fire_top - flicker,
            center_x + fire_outer + flicker,
            fire_bottom + flicker,
        )
        self.scene.coords(
            self.fire_glow_inner,
            center_x - fire_inner - flicker / 2,
            fire_top + 16 - flicker / 2,
            center_x + fire_inner + flicker / 2,
            fire_bottom - 10 + flicker / 2,
        )

        # Position bonefire image at center
        bonfire_image = self.images.get("bonefire_scene")
        if bonfire_image:
            self.scene.coords(self.bonefire_id, center_x, center_y)
            self.scene.itemconfigure(
                self.bonefire_id, image=bonfire_image
            )

        self.scene.coords(
            self.fire_id,
            center_x,
            fire_top - 18,
            center_x - fire_outer * 0.45,
            fire_bottom,
            center_x,
            fire_bottom - fire_outer * 0.34,
            center_x + fire_outer * 0.4,
            fire_bottom,
        )
        self.scene.coords(
            self.fire_core,
            center_x,
            fire_top + 8,
            center_x - fire_inner * 0.36,
            fire_bottom - 12,
            center_x,
            fire_bottom - fire_inner * 0.30,
            center_x + fire_inner * 0.32,
            fire_bottom - 12,
        )
        self.scene.coords(
            self.log_base,
            center_x - fire_outer * 0.55,
            fire_bottom,
            center_x + fire_outer * 0.55,
            fire_bottom + 12,
        )
        self.scene.coords(
            self.log_1,
            center_x - fire_outer * 0.5,
            fire_bottom + 11,
            center_x + fire_outer * 0.5,
            fire_bottom,
        )
        self.scene.coords(
            self.log_2,
            center_x - fire_outer * 0.5,
            fire_bottom,
            center_x + fire_outer * 0.5,
            fire_bottom + 11,
        )
        self.scene.itemconfigure(
            self.fire_glow_outer,
            fill="#a7511d"
            if self.display_phase == Phase.NIGHT
            else "#b8611f",
        )
        self.scene.itemconfigure(self.fire_glow_inner, fill="#ffb445")

        for index, player_id in enumerate(sorted(self.engine.players)):
            angle = (-math.pi / 2) + (math.tau * index / count)
            base_x = center_x + math.cos(angle) * radius
            base_y = center_y + math.sin(angle) * radius * 0.9
            bob = (
                max(2, avatar_size * 0.04)
                * math.sin(now * 2.0 + player_id)
            )
            x = base_x
            y = base_y + bob
            self.player_positions[player_id] = (x, y)

            player = self.engine.players[player_id]
            nodes = self.player_nodes[player_id]
            avatar = self._scene_image(
                player.avatar_key, avatar_size, avatar_size
            )
            death = (
                self.death_progress[player_id]
                if not player.is_alive
                else 0.0
            )
            label_offset = avatar_size * 0.78
            state_offset = avatar_size * 1.02

            self.scene.coords(
                nodes["shadow"],
                x - shadow_width,
                y + avatar_size * 0.38,
                x + shadow_width,
                y + avatar_size * 0.38 + shadow_height,
            )
            self.scene.coords(
                nodes["ring"],
                x - ring_radius,
                y - ring_radius,
                x + ring_radius,
                y + ring_radius,
            )
            self.scene.coords(nodes["image"], x, y)
            self.scene.coords(nodes["label"], x, y + label_offset)
            self.scene.coords(nodes["state"], x, y + state_offset)
            self.scene.coords(
                nodes["indicator"],
                x - ring_radius + 10,
                y - ring_radius + 8,
                x - ring_radius + 24,
                y - ring_radius + 22,
            )
            self.scene.itemconfigure(nodes["image"], image=avatar)
            self.scene.itemconfigure(
                nodes["label"],
                text=player.name,
                fill=(
                    ROLE_COLORS[player.role.value]
                    if self.engine.winner
                    else COLORS["text"]
                ),
                font=(
                    "Segoe UI",
                    max(10, int(avatar_size * 0.18)),
                    "bold",
                ),
            )
            self.scene.itemconfigure(
                nodes["state"],
                font=(
                    "Consolas",
                    max(9, int(avatar_size * 0.15)),
                    "bold",
                ),
            )

            if player.is_alive:
                self.scene.itemconfigure(
                    nodes["state"], text="ALIVE", fill=COLORS["green"]
                )
                self.scene.itemconfigure(
                    nodes["indicator"], fill=COLORS["green"]
                )
                self.scene.itemconfigure(
                    nodes["ring"],
                    outline=(
                        COLORS["blue"]
                        if player_id == self.focus_player_id
                        else COLORS["muted"]
                    ),
                    width=3
                    if player_id == self.focus_player_id
                    else 2,
                )
                self.scene.itemconfigure(nodes["tint"], state=tk.HIDDEN)
                self.scene.itemconfigure(
                    nodes["cross1"], state=tk.HIDDEN
                )
                self.scene.itemconfigure(
                    nodes["cross2"], state=tk.HIDDEN
                )
            else:
                self.scene.itemconfigure(
                    nodes["state"], text="DEAD", fill=COLORS["red"]
                )
                self.scene.itemconfigure(
                    nodes["indicator"], fill=COLORS["red"]
                )
                self.scene.itemconfigure(
                    nodes["ring"], outline=COLORS["red"], width=2
                )
                tint_radius = avatar_size / 2
                self.scene.coords(
                    nodes["tint"],
                    x - tint_radius,
                    y - tint_radius,
                    x + tint_radius,
                    y + tint_radius,
                )
                self.scene.itemconfigure(
                    nodes["tint"],
                    state=tk.NORMAL,
                    stipple="gray50" if death > 0.5 else "gray25",
                )
                cross_size = avatar_size * (0.20 + 0.55 * death)
                self.scene.coords(
                    nodes["cross1"],
                    x - cross_size,
                    y - cross_size,
                    x + cross_size,
                    y + cross_size,
                )
                self.scene.coords(
                    nodes["cross2"],
                    x - cross_size,
                    y + cross_size,
                    x + cross_size,
                    y - cross_size,
                )
                self.scene.itemconfigure(
                    nodes["cross1"],
                    state=tk.NORMAL,
                    width=max(2, int(avatar_size * 0.08)),
                )
                self.scene.itemconfigure(
                    nodes["cross2"],
                    state=tk.NORMAL,
                    width=max(2, int(avatar_size * 0.08)),
                )

    def _loop(self) -> None:
        """Main game loop."""
        now = time.perf_counter()
        dt = min(now - self.frame_time, 0.05)
        self.frame_time = now

        self._process_script(dt)
        self._update_scene(dt)

        if (
            self.auto_play
            and not self.is_busy
            and not self.engine.winner
            and now >= self.next_auto_time
        ):
            self.next_phase()
            self.next_auto_time = now + self.auto_delay

        self.root.after(ANIMATION_FRAME_RATE, self._loop)
