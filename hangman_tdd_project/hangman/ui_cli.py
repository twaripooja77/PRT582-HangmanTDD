from __future__ import annotations

import random
from typing import Optional

from .game import HangmanGame
from .words import WordProvider
from .timer import input_with_timeout


def _choose_level() -> str:
    print("Welcome to Hangman!\n")
    print("Choose level: 1) Basic (single word)  2) Intermediate (phrase)\n")
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice in {"1", "2"}:
            return "basic" if choice == "1" else "intermediate"
        print("Please enter 1 or 2.\n")


def play(seed: Optional[int] = None) -> None:
    if seed is not None:
        random.seed(seed)

    provider = WordProvider()
    level = _choose_level()
    game = HangmanGame.new_basic(provider) if level == "basic" else HangmanGame.new_intermediate(provider)
    print("\nLives:", game.lives)
    print("Guess letters. You have 15 seconds per guess.\n")

    while game.status == "in_progress":
        print("Word:", spaced(game.masked()))
        print("Used:", " ".join(sorted(game.used_letters())) or "(none)")
        text, timed_out = input_with_timeout("Enter a letter: ", timeout=15.0)
        if timed_out:
            print("Time's up! You lose a life.\n")
            game.timeout_penalty()
            continue
        if text is None:
            continue
        text = text.strip()
        if text.lower() == "quit":  # allow quit
            print("\nGoodbye! The answer was:", game.answer)
            return
        try:
            correct = game.guess(text[0])
        except ValueError as e:
            print("Invalid input:", e, "\n")
            continue
        if correct:
            print("Great! That letter is in the answer.\n")
        else:
            print("Nope, wrong guess.\n")

    if game.status == "won":
        print("🎉 You WIN! The answer was:", game.answer)
    else:
        print("💀 Game over. The answer was:", game.answer)


def spaced(masked: str) -> str:
    return " ".join(list(masked))


if __name__ == "__main__":
    play()
