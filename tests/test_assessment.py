import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from assessment.models import Question, Quiz, QuizResult
from assessment.runner import run_quiz, save_progress, load_progress


def test_mcq_check():
    q = Question("q1", "mcq", "prompt", options=["a", "b"], answer="a")
    assert q.check("a") is True
    assert q.check("b") is False
    assert q.check("A") is True


def test_numeric_check():
    q = Question("q2", "numeric", "prompt", answer=5, tolerance=0.1)
    assert q.check(5.0) is True
    assert q.check(5.05) is True
    assert q.check(6.0) is False


def test_run_quiz():
    quiz = Quiz(title="T", questions=[
        Question("q1", "mcq", "p", answer="a"),
        Question("q2", "numeric", "p", answer=10, tolerance=0.01),
    ])
    result = run_quiz(quiz, "Alice", ["a", 10])
    assert result.correct == 2
    assert result.score_pct == 100.0


def test_run_quiz_partial():
    quiz = Quiz(title="T", questions=[
        Question("q1", "mcq", "p", answer="a"),
        Question("q2", "mcq", "p", answer="b"),
    ])
    result = run_quiz(quiz, "Bob", ["a", "wrong"])
    assert result.correct == 1
    assert result.score_pct == 50.0


def test_save_and_load_progress():
    quiz = Quiz(title="T", questions=[Question("q1", "mcq", "p", answer="a")])
    result = run_quiz(quiz, "Alice", ["a"])
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "progress.json")
        save_progress(result, path)
        loaded = load_progress(path)
        assert len(loaded) == 1
        assert loaded[0]["learner"] == "Alice"


def test_quiz_from_file():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_quiz.json")
    quiz = Quiz.from_file(path)
    assert quiz.title == "Python Basics"
    assert len(quiz.questions) == 3


def test_quiz_from_dict():
    data = {"title": "X", "questions": [{"id": "q1", "type": "mcq", "prompt": "p", "answer": "a"}]}
    quiz = Quiz.from_dict(data)
    assert len(quiz.questions) == 1
