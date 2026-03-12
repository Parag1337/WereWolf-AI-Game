"""
Data models and enums for the Werewolf game.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


class Role(Enum):
    """Game roles."""
    VILLAGER = "Villager"
    WEREWOLF = "Werewolf"
    DOCTOR = "Doctor"
    DETECTIVE = "Detective"


class Phase(Enum):
    """Game phases."""
    DAY = "DAY"
    NIGHT = "NIGHT"


@dataclass
class Player:
    """Represents a player in the game."""
    id: int
    name: str
    role: Role
    is_alive: bool = True
    claim: Optional[Role] = None

    @property
    def team(self) -> str:
        """Return the player's team: 'evil' for werewolf, 'good' for others."""
        return "evil" if self.role == Role.WEREWOLF else "good"

    @property
    def avatar_key(self) -> str:
        """Return the asset key for the player's avatar."""
        return "werewolf" if self.role == Role.WEREWOLF else "villager"


@dataclass
class Dialogue:
    """Represents dialogue spoken by a player."""
    speaker_id: int
    text: str
    kind: str = "info"
    target_id: Optional[int] = None


@dataclass
class ScriptEvent:
    """Represents an event in the game script."""
    at: float
    kind: str
    payload: Dict[str, object] = field(default_factory=dict)
