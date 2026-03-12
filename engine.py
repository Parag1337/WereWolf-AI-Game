"""
Game engine and AI player logic for Werewolf/Mafia.
"""

import random
from collections import Counter, defaultdict
from typing import Dict, List, Optional

from models import Dialogue, Phase, Player, Role, ScriptEvent
from utils import clamp


class AIPlayer:
    """Base class for AI-controlled players."""

    accuse_lines = [
        "Player {target} is acting suspicious.",
        "The way Player {target} voted feels wrong.",
        "I do not trust Player {target} right now.",
        "Player {target} keeps slipping past scrutiny.",
    ]
    defend_lines = [
        "I swear I'm a villager!",
        "That accusation is weak and you know it.",
        "I am not the threat here.",
        "You are pushing the wrong target.",
    ]
    info_lines = [
        "We need cleaner reads before we panic.",
        "Look at who is steering the table.",
        "Trust the patterns, not the volume.",
        "We should pressure the most inconsistent player.",
    ]

    def __init__(self, player: Player, player_ids: List[int]):
        self.player = player
        self.suspicion = {pid: 0.18 for pid in player_ids if pid != player.id}
        self.trust = {pid: 0.5 for pid in player_ids if pid != player.id}
        self.known_roles: Dict[int, Role] = {}
        self.heat = 0

    def is_alive(self) -> bool:
        return self.player.is_alive

    def _living_candidates(
        self, engine: "GameEngine", exclude: Optional[set] = None
    ) -> List[int]:
        exclude = exclude or set()
        return [
            pid
            for pid in engine.living_ids()
            if pid != self.player.id and pid not in exclude
        ]

    def _most_suspicious(
        self, engine: "GameEngine", exclude: Optional[set] = None
    ) -> Optional[int]:
        choices = self._living_candidates(engine, exclude)
        if not choices:
            return None
        return max(
            choices,
            key=lambda pid: self.suspicion.get(pid, 0.18) + random.uniform(-0.02, 0.02),
        )

    def observe_dialogue(self, dialogue: Dialogue, engine: "GameEngine") -> None:
        """Update suspicion based on dialogue observed."""
        if not self.player.is_alive or dialogue.speaker_id == self.player.id:
            return
        speaker_id = dialogue.speaker_id
        target_id = dialogue.target_id
        if dialogue.kind in ("accuse", "reveal") and target_id in self.suspicion:
            self.suspicion[target_id] = clamp(
                self.suspicion[target_id]
                + 0.08 * self.trust.get(speaker_id, 0.5)
            )
        if dialogue.kind == "defend" and speaker_id in self.suspicion:
            self.suspicion[speaker_id] = clamp(self.suspicion[speaker_id] + 0.03)
        if target_id == self.player.id and dialogue.kind in ("accuse", "reveal"):
            self.heat += 1

    def observe_votes(
        self,
        votes: Dict[int, int],
        eliminated_id: Optional[int],
        engine: "GameEngine",
    ) -> None:
        """Update suspicion based on voting patterns."""
        if eliminated_id is None or not self.player.is_alive:
            self.heat = 0
            return

        eliminated_role = engine.players[eliminated_id].role
        for voter_id, target_id in votes.items():
            if voter_id == self.player.id or voter_id not in self.suspicion:
                continue
            if target_id != eliminated_id:
                if eliminated_role == Role.WEREWOLF:
                    self.suspicion[voter_id] = clamp(self.suspicion[voter_id] + 0.04)
                continue
            if eliminated_role == Role.WEREWOLF:
                self.suspicion[voter_id] = clamp(self.suspicion[voter_id] - 0.15)
                self.trust[voter_id] = clamp(self.trust[voter_id] + 0.12)
            else:
                self.suspicion[voter_id] = clamp(self.suspicion[voter_id] + 0.08)
                self.trust[voter_id] = clamp(self.trust[voter_id] - 0.08)
        self.heat = 0

    def observe_reveal(self, player_id: int, role: Role) -> None:
        """Update known roles when a player is revealed."""
        self.known_roles[player_id] = role
        if player_id in self.suspicion:
            self.suspicion[player_id] = 1.0 if role == Role.WEREWOLF else 0.0

    def on_new_day(self, engine: "GameEngine") -> None:
        """Called at the start of a new day."""
        for pid in self._living_candidates(engine):
            if pid not in self.known_roles:
                self.suspicion[pid] = clamp(
                    self.suspicion[pid] + random.uniform(-0.03, 0.04)
                )

    def make_day_dialogue(self, engine: "GameEngine") -> Dialogue:
        """Generate dialogue for the day phase."""
        if self.heat > 0 and random.random() < 0.65:
            return Dialogue(self.player.id, random.choice(self.defend_lines), "defend", self.player.id)

        target_id = self._most_suspicious(engine)
        if target_id is not None and self.suspicion.get(target_id, 0.0) > 0.44:
            return Dialogue(
                self.player.id,
                random.choice(self.accuse_lines).format(target=target_id),
                "accuse",
                target_id,
            )

        if target_id is not None and random.random() < 0.45:
            return Dialogue(
                self.player.id,
                f"We should vote Player {target_id}.",
                "accuse",
                target_id,
            )

        return Dialogue(self.player.id, random.choice(self.info_lines), "info", None)

    def vote(self, engine: "GameEngine") -> int:
        """Decide which player to vote for."""
        target_id = self._most_suspicious(engine)
        candidates = self._living_candidates(engine)
        if target_id is not None:
            return target_id
        return random.choice(candidates) if candidates else self.player.id

    def night_action(self, engine: "GameEngine") -> Optional[int]:
        """Return target player ID for night action (if applicable)."""
        return None


class Villager(AIPlayer):
    """Villager AI (no special actions)."""
    pass


class Werewolf(AIPlayer):
    """Werewolf AI with pack knowledge and fake claiming."""

    def __init__(self, player: Player, player_ids: List[int], pack_ids: List[int]):
        super().__init__(player, player_ids)
        self.pack_ids = set(pack_ids)
        self.fake_claimed = False
        for pack_id in self.pack_ids:
            if pack_id != self.player.id:
                self.suspicion[pack_id] = 0.0
                self.trust[pack_id] = 1.0
                self.known_roles[pack_id] = Role.WEREWOLF

    def _wolf_targets(self, engine: "GameEngine") -> List[int]:
        return [pid for pid in engine.living_ids() if pid not in self.pack_ids]

    def make_day_dialogue(self, engine: "GameEngine") -> Dialogue:
        targets = self._wolf_targets(engine)
        if not targets:
            return Dialogue(self.player.id, "We are close. Stay sharp.", "info", None)

        if self.heat > 0 and not self.fake_claimed and random.random() < 0.22:
            self.fake_claimed = True
            self.player.claim = Role.DETECTIVE
            target_id = random.choice(targets)
            return Dialogue(
                self.player.id,
                f"I am the Detective. Player {target_id} is mafia.",
                "reveal",
                target_id,
            )

        target_id = engine.pick_werewolf_vote_target()
        if target_id is None:
            target_id = random.choice(targets)

        if self.heat > 0 and random.random() < 0.55:
            return Dialogue(self.player.id, random.choice(self.defend_lines), "defend", self.player.id)

        lines = [
            "Player {target} is steering the room too hard.",
            "Why is nobody pressuring Player {target}?",
            "Player {target} feels rehearsed to me.",
            "We should vote Player {target} before this slips away.",
        ]
        return Dialogue(
            self.player.id,
            random.choice(lines).format(target=target_id),
            "accuse",
            target_id,
        )

    def vote(self, engine: "GameEngine") -> int:
        target_id = engine.pick_werewolf_vote_target()
        if target_id is not None:
            return target_id
        targets = self._wolf_targets(engine)
        return random.choice(targets) if targets else self.player.id

    def night_action(self, engine: "GameEngine") -> Optional[int]:
        targets = self._wolf_targets(engine)
        if not targets:
            return None

        claimed_detectives = [
            pid for pid in targets if engine.players[pid].claim == Role.DETECTIVE
        ]
        if claimed_detectives:
            return random.choice(claimed_detectives)

        power_roles = [
            pid
            for pid in targets
            if engine.players[pid].role in (Role.DOCTOR, Role.DETECTIVE)
        ]
        if power_roles and random.random() < 0.6:
            return random.choice(power_roles)

        return min(targets, key=lambda pid: engine.average_suspicion(pid))


class Doctor(AIPlayer):
    """Doctor AI with protective abilities."""

    def __init__(self, player: Player, player_ids: List[int]):
        super().__init__(player, player_ids)
        self.last_saved: Optional[int] = None

    def make_day_dialogue(self, engine: "GameEngine") -> Dialogue:
        target_id = self._most_suspicious(engine)
        if target_id is not None and self.suspicion.get(target_id, 0.0) > 0.48:
            return Dialogue(
                self.player.id,
                f"Player {target_id} is making me nervous.",
                "accuse",
                target_id,
            )
        return Dialogue(
            self.player.id, "Protect the people who are helping the village.", "info", None
        )

    def night_action(self, engine: "GameEngine") -> Optional[int]:
        living = engine.living_ids()
        candidates = [pid for pid in living if pid != self.last_saved]
        if not candidates:
            candidates = living

        revealed_detectives = [
            pid
            for pid in candidates
            if engine.players[pid].claim == Role.DETECTIVE
        ]
        if revealed_detectives:
            target_id = min(
                revealed_detectives,
                key=lambda pid: self.suspicion.get(pid, 0.18),
            )
        else:
            target_id = min(candidates, key=lambda pid: self.suspicion.get(pid, 0.18))

        self.last_saved = target_id
        return target_id


class Detective(AIPlayer):
    """Detective AI with investigation abilities."""

    def __init__(self, player: Player, player_ids: List[int]):
        super().__init__(player, player_ids)
        self.investigated: Dict[int, bool] = {}
        self.revealed = False

    def register_investigation(self, target_id: int, is_werewolf: bool) -> None:
        """Register an investigation result."""
        self.investigated[target_id] = is_werewolf
        self.suspicion[target_id] = 0.95 if is_werewolf else 0.02
        self.known_roles[target_id] = (
            Role.WEREWOLF if is_werewolf else Role.VILLAGER
        )

    def make_day_dialogue(self, engine: "GameEngine") -> Dialogue:
        live_wolves = [
            pid
            for pid, is_wolf in self.investigated.items()
            if is_wolf and engine.players[pid].is_alive
        ]
        if (
            live_wolves
            and (
                self.revealed
                or engine.day_number >= 2
                or random.random() < 0.45
            )
        ):
            self.player.claim = Role.DETECTIVE
            self.revealed = True
            target_id = live_wolves[0]
            return Dialogue(
                self.player.id,
                f"I checked Player {target_id}. They are mafia.",
                "reveal",
                target_id,
            )

        cleared = [
            pid
            for pid, is_wolf in self.investigated.items()
            if not is_wolf and engine.players[pid].is_alive
        ]
        if cleared and self.revealed and random.random() < 0.35:
            target_id = cleared[0]
            return Dialogue(
                self.player.id,
                f"Player {target_id} came back clean.",
                "info",
                target_id,
            )

        return super().make_day_dialogue(engine)

    def vote(self, engine: "GameEngine") -> int:
        live_wolves = [
            pid
            for pid, is_wolf in self.investigated.items()
            if is_wolf and engine.players[pid].is_alive
        ]
        if live_wolves:
            return live_wolves[0]
        return super().vote(engine)

    def night_action(self, engine: "GameEngine") -> Optional[int]:
        pool = [
            pid
            for pid in engine.living_ids()
            if pid != self.player.id and pid not in self.investigated
        ]
        if not pool:
            return None
        return max(pool, key=lambda pid: self.suspicion.get(pid, 0.18))


class GameEngine:
    """Main game engine for Werewolf/Mafia simulation."""

    def __init__(self, num_players: int = 8):
        self.num_players = max(6, min(12, num_players))
        self.day_number = 1
        self.phase = Phase.DAY
        self.winner: Optional[str] = None
        self.players: Dict[int, Player] = {}
        self.ai: Dict[int, AIPlayer] = {}
        self.logs: List[tuple] = []
        self.last_votes: Dict[int, int] = {}
        self.cached_werewolf_target: Optional[int] = None
        self._build_roster()

    def _build_roster(self) -> None:
        """Initialize players with random roles."""
        werewolf_count = max(1, self.num_players // 4)
        roles = [Role.WEREWOLF] * werewolf_count + [
            Role.DOCTOR,
            Role.DETECTIVE,
        ]
        roles += [Role.VILLAGER] * (self.num_players - len(roles))
        random.shuffle(roles)

        player_ids = list(range(1, self.num_players + 1))
        for pid, role in zip(player_ids, roles):
            self.players[pid] = Player(pid, f"Player {pid}", role)

        pack_ids = [
            pid
            for pid, player in self.players.items()
            if player.role == Role.WEREWOLF
        ]
        for pid, player in self.players.items():
            if player.role == Role.WEREWOLF:
                self.ai[pid] = Werewolf(player, player_ids, pack_ids)
            elif player.role == Role.DOCTOR:
                self.ai[pid] = Doctor(player, player_ids)
            elif player.role == Role.DETECTIVE:
                self.ai[pid] = Detective(player, player_ids)
            else:
                self.ai[pid] = Villager(player, player_ids)

    def living_players(self) -> List[Player]:
        """Return list of alive players."""
        return [player for player in self.players.values() if player.is_alive]

    def living_ids(self) -> List[int]:
        """Return list of alive player IDs."""
        return [player.id for player in self.living_players()]

    def average_suspicion(self, target_id: int) -> float:
        """Calculate average suspicion toward a target across all players."""
        values = [
            brain.suspicion.get(target_id, 0.18)
            for pid, brain in self.ai.items()
            if self.players[pid].is_alive and pid != target_id
        ]
        return sum(values) / len(values) if values else 0.18

    def visible_role(self, player_id: int) -> str:
        """Return the role visible to display (claim if game is ongoing, actual if revealed)."""
        player = self.players[player_id]
        if player.is_alive and self.winner is None:
            return player.claim.value if player.claim else "Hidden"
        return player.role.value

    def counts(self) -> Counter:
        """Count players by role among living players."""
        return Counter(player.role for player in self.living_players())

    def check_winner(self) -> Optional[str]:
        """Check if game has a winner."""
        counts = self.counts()
        wolves = counts[Role.WEREWOLF]
        good = len(self.living_players()) - wolves
        if wolves <= 0:
            return "Village"
        if wolves >= good:
            return "Werewolves"
        return None

    def pick_werewolf_vote_target(self) -> Optional[int]:
        """Pick the target werewolves should vote for."""
        if (
            self.cached_werewolf_target
            and self.players[self.cached_werewolf_target].is_alive
        ):
            return self.cached_werewolf_target

        candidates = [
            pid
            for pid in self.living_ids()
            if self.players[pid].role != Role.WEREWOLF
        ]
        if not candidates:
            return None

        target_id = min(candidates, key=self.average_suspicion)
        self.cached_werewolf_target = target_id
        return target_id

    def advance_phase(self) -> List[ScriptEvent]:
        """Advance to next phase and return script events."""
        if self.winner:
            return []
        return self._run_day() if self.phase == Phase.DAY else self._run_night()

    def _run_day(self) -> List[ScriptEvent]:
        """Execute the day phase."""
        self.cached_werewolf_target = None
        for brain in self.ai.values():
            if brain.is_alive():
                brain.on_new_day(self)

        script: List[ScriptEvent] = []
        cursor = 0.0
        accused_targets: Dict[int, List[int]] = defaultdict(list)
        alive_ids = self.living_ids()
        speakers = alive_ids[:]
        random.shuffle(speakers)
        speakers = speakers[: min(5, len(speakers))]

        for speaker_id in speakers:
            dialogue = self.ai[speaker_id].make_day_dialogue(self)
            if dialogue.target_id and dialogue.kind in ("accuse", "reveal"):
                accused_targets[dialogue.target_id].append(speaker_id)
            for brain in self.ai.values():
                brain.observe_dialogue(dialogue, self)
            script.append(
                ScriptEvent(cursor, "speech", {"dialogue": dialogue})
            )
            cursor += 0.75

        for target_id, _accusers in list(accused_targets.items())[:2]:
            if not self.players[target_id].is_alive:
                continue
            if random.random() < 0.9:
                defense = Dialogue(
                    target_id,
                    random.choice(self.ai[target_id].defend_lines),
                    "defend",
                    target_id,
                )
                for brain in self.ai.values():
                    brain.observe_dialogue(defense, self)
                script.append(
                    ScriptEvent(cursor, "speech", {"dialogue": defense})
                )
                cursor += 0.65

        votes: Dict[int, int] = {}
        for voter_id in alive_ids:
            votes[voter_id] = self.ai[voter_id].vote(self)
        self.last_votes = votes

        for voter_id, target_id in votes.items():
            script.append(
                ScriptEvent(
                    cursor,
                    "vote",
                    {"voter": voter_id, "target": target_id},
                )
            )
            cursor += 0.10

        counts = Counter(votes.values())
        tally = " | ".join(
            f"P{pid}:{count}" for pid, count in counts.most_common()
        )
        script.append(
            ScriptEvent(cursor, "log", {"text": f"Vote tally: {tally}", "tag": "system"})
        )
        cursor += 0.20

        top_votes = max(counts.values()) if counts else 0
        tied = [pid for pid, count in counts.items() if count == top_votes]
        eliminated_id = random.choice(tied) if tied else None

        if eliminated_id is not None:
            self.players[eliminated_id].is_alive = False
            role = self.players[eliminated_id].role
            script.append(
                ScriptEvent(
                    cursor,
                    "death",
                    {"player": eliminated_id, "reason": "vote"},
                )
            )
            script.append(
                ScriptEvent(
                    cursor + 0.20,
                    "reveal",
                    {"player": eliminated_id, "role": role},
                )
            )
            cursor += 1.05

        for brain in self.ai.values():
            brain.observe_votes(votes, eliminated_id, self)
            if eliminated_id is not None:
                brain.observe_reveal(
                    eliminated_id, self.players[eliminated_id].role
                )

        self.winner = self.check_winner()
        if self.winner:
            script.append(ScriptEvent(cursor, "winner", {"winner": self.winner}))
            return script

        self.phase = Phase.NIGHT
        script.append(
            ScriptEvent(
                cursor,
                "phase_transition",
                {"phase": Phase.NIGHT, "day": self.day_number},
            )
        )
        return script

    def _run_night(self) -> List[ScriptEvent]:
        """Execute the night phase."""
        script: List[ScriptEvent] = []
        cursor = 0.0

        wolf_ids = [
            pid
            for pid in self.living_ids()
            if self.players[pid].role == Role.WEREWOLF
        ]
        doctor_id = next(
            (
                pid
                for pid in self.living_ids()
                if self.players[pid].role == Role.DOCTOR
            ),
            None,
        )
        detective_id = next(
            (
                pid
                for pid in self.living_ids()
                if self.players[pid].role == Role.DETECTIVE
            ),
            None,
        )

        kill_target = None
        save_target = None
        scan_target = None

        if wolf_ids:
            wolf_choices = [
                self.ai[pid].night_action(self) for pid in wolf_ids
            ]
            wolf_choices = [pid for pid in wolf_choices if pid is not None]
            if wolf_choices:
                kill_target = Counter(wolf_choices).most_common(1)[0][0]
                script.append(
                    ScriptEvent(
                        cursor,
                        "kill_move",
                        {"source": random.choice(wolf_ids), "target": kill_target},
                    )
                )
                cursor += 0.75

        if doctor_id is not None:
            save_target = self.ai[doctor_id].night_action(self)
            if save_target is not None:
                script.append(
                    ScriptEvent(
                        cursor,
                        "shield",
                        {
                            "target": save_target,
                            "saved": save_target == kill_target,
                        },
                    )
                )
                cursor += 0.60

        if detective_id is not None:
            scan_target = self.ai[detective_id].night_action(self)
            if scan_target is not None:
                is_wolf = (
                    self.players[scan_target].role == Role.WEREWOLF
                )
                detective = self.ai[detective_id]
                if isinstance(detective, Detective):
                    detective.register_investigation(scan_target, is_wolf)
                script.append(
                    ScriptEvent(
                        cursor,
                        "scan",
                        {"target": scan_target, "is_werewolf": is_wolf},
                    )
                )
                cursor += 0.60

        if (
            kill_target is not None
            and kill_target != save_target
            and self.players[kill_target].is_alive
        ):
            self.players[kill_target].is_alive = False
            role = self.players[kill_target].role
            script.append(
                ScriptEvent(
                    cursor,
                    "death",
                    {"player": kill_target, "reason": "night"},
                )
            )
            script.append(
                ScriptEvent(
                    cursor + 0.20,
                    "reveal",
                    {"player": kill_target, "role": role},
                )
            )
            cursor += 1.0

            for brain in self.ai.values():
                brain.observe_reveal(kill_target, role)
        elif kill_target is not None and save_target == kill_target:
            script.append(
                ScriptEvent(
                    cursor,
                    "log",
                    {
                        "text": f"Doctor saved Player {kill_target} during the night.",
                        "tag": "save",
                    },
                )
            )
            cursor += 0.20
        else:
            script.append(
                ScriptEvent(
                    cursor,
                    "log",
                    {"text": "The night passes without a kill.", "tag": "system"},
                )
            )
            cursor += 0.20

        self.winner = self.check_winner()
        if self.winner:
            script.append(ScriptEvent(cursor, "winner", {"winner": self.winner}))
            return script

        self.phase = Phase.DAY
        self.day_number += 1
        script.append(
            ScriptEvent(
                cursor,
                "phase_transition",
                {"phase": Phase.DAY, "day": self.day_number},
            )
        )
        return script
