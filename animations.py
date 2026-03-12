"""
Animation classes for game visual effects.
"""

import math
import tkinter as tk
from typing import TYPE_CHECKING, Optional

from config import COLORS
from models import Phase, Role
from utils import clamp, ease_out_back, ease_out_cubic, lerp

if TYPE_CHECKING:
    from ui import GameUI


class Animation:
    """Base class for all animations."""

    def __init__(self, duration: float):
        self.duration = max(duration, 0.001)
        self.elapsed = 0.0
        self.started = False
        self.finished = False

    def start(self, ui: "GameUI") -> None:
        """Called when animation starts."""
        self.started = True

    def step(self, ui: "GameUI", dt: float) -> None:
        """Update animation by dt seconds."""
        if self.finished:
            return
        if not self.started:
            self.start(ui)
        self.elapsed += dt
        progress = clamp(self.elapsed / self.duration)
        self.update(ui, progress)
        if self.elapsed >= self.duration:
            self.finish(ui)

    def update(self, ui: "GameUI", progress: float) -> None:
        """Update animation for current progress (0.0 to 1.0)."""
        raise NotImplementedError

    def finish(self, ui: "GameUI") -> None:
        """Called when animation completes."""
        self.finished = True


class AnimationManager:
    """Manages active animations."""

    def __init__(self):
        self.animations: list[Animation] = []

    def add(self, animation: Animation) -> None:
        """Add animation to queue."""
        self.animations.append(animation)

    def update(self, ui: "GameUI", dt: float) -> None:
        """Update all active animations."""
        for animation in self.animations[:]:
            animation.step(ui, dt)
            if animation.finished:
                self.animations.remove(animation)

    def active(self) -> bool:
        """Check if any animations are playing."""
        return bool(self.animations)


class SpeechBubbleAnimation(Animation):
    """Speech bubble animation for dialogue."""

    def __init__(self, player_id: int, text: str, tone: str):
        super().__init__(1.9)
        self.player_id = player_id
        self.text = text
        self.tone = tone
        self.text_id = None
        self.bubble_id = None
        self.tail_id = None

    SPEECH_COLORS = {
        "info": COLORS["surface2"],
        "accuse": "#3b3348",
        "defend": "#43372f",
        "reveal": "#23384c",
    }

    def start(self, ui: "GameUI") -> None:
        super().start(ui)
        scene = ui.scene
        fill = self.SPEECH_COLORS.get(self.tone, COLORS["surface2"])
        self.bubble_id = scene.create_oval(
            0, 0, 0, 0, fill=fill, outline=COLORS["text"], width=2
        )
        self.tail_id = scene.create_polygon(
            0, 0, 0, 0, 0, 0, fill=fill, outline=COLORS["text"], width=2
        )
        self.text_id = scene.create_text(
            0,
            0,
            text=self.text,
            width=180,
            justify=tk.CENTER,
            fill=COLORS["text"],
            font=("Segoe UI", 2, "bold"),
        )

    def update(self, ui: "GameUI", progress: float) -> None:
        scene = ui.scene
        px, py = ui.player_position(self.player_id)
        scale = (
            ease_out_back(progress / 0.35) if progress < 0.35 else 1.0
        )
        font_size = max(8, int(11 * scale))
        y_offset = 88 + 10 * math.sin(progress * math.pi)
        scene.coords(self.text_id, px, py - y_offset)
        scene.itemconfigure(self.text_id, font=("Segoe UI", font_size, "bold"))
        bbox = scene.bbox(self.text_id)
        if not bbox:
            return
        pad = 12 * scale
        x1, y1, x2, y2 = bbox
        scene.coords(
            self.bubble_id,
            x1 - pad,
            y1 - pad,
            x2 + pad,
            y2 + pad,
        )
        scene.coords(
            self.tail_id,
            px - 10 * scale,
            y2 + pad - 2,
            px + 12 * scale,
            y2 + pad - 2,
            px,
            y2 + pad + 18 * scale,
        )

    def finish(self, ui: "GameUI") -> None:
        for item_id in (self.bubble_id, self.tail_id, self.text_id):
            if item_id:
                ui.scene.delete(item_id)
        super().finish(ui)


class VoteArrowAnimation(Animation):
    """Vote arrow animation."""

    def __init__(self, voter_id: int, target_id: int):
        super().__init__(0.55)
        self.voter_id = voter_id
        self.target_id = target_id
        self.line_id = None
        self.pulse_id = None

    def start(self, ui: "GameUI") -> None:
        super().start(ui)
        self.line_id = ui.scene.create_line(
            0,
            0,
            0,
            0,
            fill=COLORS["cyan"],
            width=3,
            arrow=tk.LAST,
            arrowshape=(10, 12, 6),
            smooth=True,
        )
        self.pulse_id = ui.scene.create_oval(
            0, 0, 0, 0, outline=COLORS["yellow"], width=2
        )

    def update(self, ui: "GameUI", progress: float) -> None:
        sx, sy = ui.player_position(self.voter_id)
        tx, ty = ui.player_position(self.target_id)
        progress = ease_out_cubic(progress)
        cx = lerp(sx, tx, progress)
        cy = lerp(sy, ty, progress)
        ui.scene.coords(
            self.line_id,
            sx,
            sy,
            (sx + cx) / 2,
            sy - 26,
            cx,
            cy,
        )
        radius = 18 * progress
        ui.scene.coords(
            self.pulse_id,
            tx - radius,
            ty - radius,
            tx + radius,
            ty + radius,
        )

    def finish(self, ui: "GameUI") -> None:
        ui.scene.delete(self.line_id)
        ui.scene.delete(self.pulse_id)
        super().finish(ui)


class MovingIconAnimation(Animation):
    """Moving icon animation (for werewolf or item movement)."""

    def __init__(
        self,
        source_id: int,
        target_id: int,
        image: Optional[tk.PhotoImage],
    ):
        super().__init__(0.8)
        self.source_id = source_id
        self.target_id = target_id
        self.image = image
        self.image_id = None

    def start(self, ui: "GameUI") -> None:
        super().start(ui)
        if self.image is None:
            self.image_id = ui.scene.create_text(
                0,
                0,
                text="W",
                fill=COLORS["red"],
                font=("Segoe UI", 18, "bold"),
            )
        else:
            self.image_id = ui.scene.create_image(0, 0, image=self.image)

    def update(self, ui: "GameUI", progress: float) -> None:
        sx, sy = ui.player_position(self.source_id)
        tx, ty = ui.player_position(self.target_id)
        arc = math.sin(progress * math.pi) * 40
        x = lerp(sx, tx, ease_out_cubic(progress))
        y = lerp(sy, ty, ease_out_cubic(progress)) - arc
        ui.scene.coords(self.image_id, x, y)

    def finish(self, ui: "GameUI") -> None:
        ui.scene.delete(self.image_id)
        super().finish(ui)


class ShieldFlashAnimation(Animation):
    """Shield flash animation (doctor protection)."""

    def __init__(self, target_id: int):
        super().__init__(0.7)
        self.target_id = target_id
        self.ring_id = None
        self.label_id = None

    def start(self, ui: "GameUI") -> None:
        super().start(ui)
        self.ring_id = ui.scene.create_oval(
            0, 0, 0, 0, outline=COLORS["green"], width=4
        )
        self.label_id = ui.scene.create_text(
            0,
            0,
            text="SHIELD",
            fill=COLORS["green"],
            font=("Consolas", 10, "bold"),
        )

    def update(self, ui: "GameUI", progress: float) -> None:
        x, y = ui.player_position(self.target_id)
        radius = 28 + 34 * progress
        ui.scene.coords(
            self.ring_id,
            x - radius,
            y - radius,
            x + radius,
            y + radius,
        )
        ui.scene.coords(self.label_id, x, y - radius - 16)
        ui.scene.itemconfigure(
            self.ring_id, width=max(1, int(5 - progress * 4))
        )

    def finish(self, ui: "GameUI") -> None:
        ui.scene.delete(self.ring_id)
        ui.scene.delete(self.label_id)
        super().finish(ui)


class ScanRingAnimation(Animation):
    """Scan ring animation (detective investigation)."""

    def __init__(self, target_id: int):
        super().__init__(0.8)
        self.target_id = target_id
        self.ring_id = None

    def start(self, ui: "GameUI") -> None:
        super().start(ui)
        self.ring_id = ui.scene.create_oval(
            0, 0, 0, 0, outline=COLORS["blue"], width=3
        )

    def update(self, ui: "GameUI", progress: float) -> None:
        x, y = ui.player_position(self.target_id)
        radius = 12 + 46 * ease_out_cubic(progress)
        ui.scene.coords(
            self.ring_id,
            x - radius,
            y - radius,
            x + radius,
            y + radius,
        )
        ui.scene.itemconfigure(
            self.ring_id, width=max(1, int(4 - progress * 3))
        )

    def finish(self, ui: "GameUI") -> None:
        ui.scene.delete(self.ring_id)
        super().finish(ui)


class DeathAnimation(Animation):
    """Death animation for eliminated players."""

    def __init__(self, player_id: int):
        super().__init__(1.15)
        self.player_id = player_id

    def update(self, ui: "GameUI", progress: float) -> None:
        ui.death_progress[self.player_id] = progress

    def finish(self, ui: "GameUI") -> None:
        ui.death_progress[self.player_id] = 1.0
        super().finish(ui)


class RevealPulseAnimation(Animation):
    """Reveal pulse animation for role reveal."""

    def __init__(self, player_id: int, role: Role):
        super().__init__(1.0)
        self.player_id = player_id
        self.role = role
        self.ring_id = None
        self.text_id = None

    def start(self, ui: "GameUI") -> None:
        super().start(ui)
        from config import ROLE_COLORS

        color = ROLE_COLORS[self.role.value]
        self.ring_id = ui.scene.create_oval(
            0, 0, 0, 0, outline=color, width=4
        )
        self.text_id = ui.scene.create_text(
            0,
            0,
            text=self.role.value.upper(),
            fill=color,
            font=("Segoe UI", 11, "bold"),
        )

    def update(self, ui: "GameUI", progress: float) -> None:
        x, y = ui.player_position(self.player_id)
        radius = 28 + 52 * ease_out_cubic(progress)
        ui.scene.coords(
            self.ring_id,
            x - radius,
            y - radius,
            x + radius,
            y + radius,
        )
        ui.scene.coords(
            self.text_id,
            x,
            y - 90 - 12 * progress,
        )

    def finish(self, ui: "GameUI") -> None:
        ui.scene.delete(self.ring_id)
        ui.scene.delete(self.text_id)
        super().finish(ui)


class BackgroundTransitionAnimation(Animation):
    """Background phase transition animation."""

    def __init__(self, target_phase: Phase, day_number: int):
        super().__init__(1.0)
        self.target_phase = target_phase
        self.day_number = day_number
        self.overlay_id = None
        self.swapped = False

    def start(self, ui: "GameUI") -> None:
        super().start(ui)
        width, height = ui._scene_dimensions()
        self.overlay_id = ui.scene.create_rectangle(
            0, 0, width, height, fill=COLORS["black"], outline=""
        )

    @staticmethod
    def _stipple_for_level(level: float) -> str:
        if level < 0.10:
            return "gray12"
        if level < 0.25:
            return "gray25"
        if level < 0.50:
            return "gray50"
        if level < 0.75:
            return "gray75"
        return ""

    def update(self, ui: "GameUI", progress: float) -> None:
        opacity = (
            progress * 2 if progress < 0.5 else (1.0 - progress) * 2
        )
        ui.scene.itemconfigure(
            self.overlay_id,
            stipple=self._stipple_for_level(clamp(opacity)),
        )
        if not self.swapped and progress >= 0.5:
            ui.set_display_phase(self.target_phase, self.day_number)
            self.swapped = True

    def finish(self, ui: "GameUI") -> None:
        ui.scene.delete(self.overlay_id)
        super().finish(ui)


class WinnerBannerAnimation(Animation):
    """Winner banner animation."""

    def __init__(self, winner: str):
        super().__init__(2.0)
        self.winner = winner
        self.text_id = None
        self.bg_id = None

    def start(self, ui: "GameUI") -> None:
        super().start(ui)
        width, height = ui._scene_dimensions()
        center_y = height * 0.46
        self.bg_id = ui.scene.create_rectangle(
            100,
            center_y - 60,
            width - 100,
            center_y + 60,
            fill=COLORS["panel"],
            outline=COLORS["yellow"],
            width=3,
        )
        self.text_id = ui.scene.create_text(
            width / 2,
            center_y,
            text=f"{self.winner.upper()} WIN",
            fill=COLORS["yellow"],
            font=("Segoe UI", 10, "bold"),
        )

    def update(self, ui: "GameUI", progress: float) -> None:
        width, height = ui._scene_dimensions()
        center_y = height * 0.46
        scale = 16 + int(
            18
            * ease_out_back(
                min(progress, 0.55) / 0.55 if progress < 0.55 else 1.0
            )
        )
        ui.scene.coords(
            self.text_id,
            width / 2,
            center_y - 6 * math.sin(progress * math.pi),
        )
        ui.scene.itemconfigure(
            self.text_id,
            font=("Segoe UI", scale, "bold"),
        )

    def finish(self, ui: "GameUI") -> None:
        super().finish(ui)
