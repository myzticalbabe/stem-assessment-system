"""Question and quiz models."""
import json
from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class Question:
    id: str
    type: str  # "mcq" or "numeric"
    prompt: str
    options: List[str] = field(default_factory=list)
    answer: Any = None
    tolerance: float = 0.0

    def check(self, response: Any) -> bool:
        if self.type == "mcq":
            return str(response).strip().lower() == str(self.answer).strip().lower()
        if self.type == "numeric":
            try:
                return abs(float(response) - float(self.answer)) <= self.tolerance
            except (ValueError, TypeError):
                return False
        return False


@dataclass
class Quiz:
    title: str
    questions: List[Question]

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        qs = [Question(**q) for q in data["questions"]]
        return cls(title=data.get("title", "Quiz"), questions=qs)

    @classmethod
    def from_file(cls, path: str) -> "Quiz":
        with open(path) as f:
            return cls.from_dict(json.load(f))


@dataclass
class QuizResult:
    quiz_title: str
    learner: str
    total: int
    correct: int
    answers: List[dict]

    @property
    def score_pct(self) -> float:
        if self.total == 0:
            return 0.0
        return round(self.correct / self.total * 100, 2)
