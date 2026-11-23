"""CLI for assessment system."""
import argparse
import json

from .models import Quiz
from .runner import run_quiz, save_progress


def main(argv=None):
    parser = argparse.ArgumentParser(description="Assessment System")
    parser.add_argument("--quiz", required=True, help="Quiz JSON file")
    parser.add_argument("--learner", required=True, help="Learner name")
    parser.add_argument("--answers", required=True, help="JSON file of answers")
    parser.add_argument("--progress", default="progress.json", help="Progress file")
    args = parser.parse_args(argv)

    quiz = Quiz.from_file(args.quiz)
    with open(args.answers) as f:
        answers = json.load(f)
    result = run_quiz(quiz, args.learner, answers)
    save_progress(result, args.progress)
    print(f"{result.learner}: {result.correct}/{result.total} ({result.score_pct}%)")


if __name__ == "__main__":
    main()
