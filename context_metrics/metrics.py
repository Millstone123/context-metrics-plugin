"""In-memory metrics collected during a pytest session."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class SessionMetrics:
    started: bool = False
    collected: int = 0
    outcomes: Dict[str, int] = field(default_factory=dict)
    phases: List[Tuple[str, float]] = field(default_factory=list)

    def start(self) -> None:
        self.started = True

    def record_collection(self, count: int) -> None:
        self.collected = max(0, int(count))

    def record_phase(self, phase: str, elapsed: float) -> None:
        self.phases.append((phase, max(0.0, float(elapsed))))

    def record_outcome(self, outcome: str) -> None:
        self.outcomes[outcome] = self.outcomes.get(outcome, 0) + 1

    def slowest(self, limit: int = 3) -> List[Tuple[str, float]]:
        return sorted(self.phases, key=lambda item: item[1], reverse=True)[:limit]

    def totals(self) -> Dict[str, int]:
        return {
            "collected": self.collected,
            "passed": self.outcomes.get("passed", 0),
            "failed": self.outcomes.get("failed", 0),
            "skipped": self.outcomes.get("skipped", 0),
        }
