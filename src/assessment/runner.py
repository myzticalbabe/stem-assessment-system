"""Quiz runner with scoring and progress tracking."""
import json
import os
from datetime import datetime

from .models import Quiz, QuizResult


def run_quiz(quiz: Quiz, learner: str, responses: List[Any]) -> QuizResult:
    answers = []
    correct = 0
    for q, resp in zip(quiz.questions, responses):
        ok = q.check(resp)
        if ok:
            correct += 1
        answers.append({"question_id": q.id, "response": resp, "correct": ok})
    return QuizResult(
        quiz_title=quiz.title,
        learner=learner,
        total=len(quiz.questions),
        correct=correct,
        answers=answers,
    )


def save_progress(result: QuizResult, path: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    record = {
        "quiz": result.quiz_title,
        "learner": result.learner,
        "score_pct": result.score_pct,
        "correct": result.correct,
        "total": result.total,
        "timestamp": datetime.now().isoformat(),
        "answers": result.answers,
    }
    # Append to existing progress file
    existing = []
    if os.path.exists(path):
        with open(path) as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    if not isinstance(existing, list):
        existing = [existing]
    existing.append(record)
    with open(path, "w") as f:
        json.dump(existing, f, indent=2)


def load_progress(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path) as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]
