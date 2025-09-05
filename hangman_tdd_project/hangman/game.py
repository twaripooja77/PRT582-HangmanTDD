from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterable, Optional, Set

from .words import WordProvider, tokenize


class MaskingPolicy(Enum):
    LETTERS_ONLY = auto()  
    ALL_CHARS = auto()     

@dataclass
class HangmanGame:

    answer: str
    lives: int = 6
    masking: MaskingPolicy = MaskingPolicy.LETTERS_ONLY
    allowed_guesses: Set[str] = field(default_factory=lambda: set("abcdefghijklmnopqrstuvwxyz"))
    provider: Optional[WordProvider] = None

    guessed: Set[str] = field(default_factory=set, init=False)
    status: str = field(default="in_progress", init=False) 

    def __post_init__(self) -> None:
        self.answer = self.answer.strip()
        if not self.answer:
            raise ValueError("Answer must be non-empty")
        if self.provider is None:
            self.provider = WordProvider()
        if " " in self.answer or any(not ch.isalpha() and ch != " " and ch not in "-'!,.?" for ch in self.answer):
            if not self.provider.is_valid_phrase(self.answer):
                raise ValueError("Phrase not valid against dictionary")
        else:
            if not self.provider.is_valid_word(self.answer):
                raise ValueError("Word not valid against dictionary")

    def normalized_answer(self) -> str:
        return self.answer.lower()

    def masked(self) -> str:
        out = []
        for ch in self.answer:
            if ch.isalpha():
                out.append(ch if ch.lower() in self.guessed else "_")
            else:
                out.append(ch if self.masking == MaskingPolicy.LETTERS_ONLY else ("_" if ch != " " else " "))
        return "".join(out)

    def remaining_lives(self) -> int:
        return self.lives

    def used_letters(self) -> Set[str]:
        return set(sorted(self.guessed))

    def guess(self, letter: str) -> bool:
        if self.status != "in_progress":
            return False
        if not letter or len(letter) != 1 or not letter.isalpha():
            raise ValueError("Guess must be a single alphabetic character")
        letter = letter.lower()
        if letter in self.guessed:
            return False
        self.guessed.add(letter)
        if letter in self.normalized_answer():
            if self._all_revealed():
                self.status = "won"
            return True
        self.lives -= 1
        if self.lives <= 0:
            self.status = "lost"
        return False

    def timeout_penalty(self) -> None:
        if self.status != "in_progress":
            return
        self.lives -= 1
        if self.lives <= 0:
            self.status = "lost"

    def _all_revealed(self) -> bool:
        for ch in self.answer:
            if ch.isalpha() and ch.lower() not in self.guessed:
                return False
        return True

    @classmethod
    def new_basic(cls, provider: Optional[WordProvider] = None, lives: int = 6) -> "HangmanGame":
        p = provider or WordProvider()
        return cls(answer=p.random_word(), lives=lives, provider=p)

    @classmethod
    def new_intermediate(cls, provider: Optional[WordProvider] = None, lives: int = 6) -> "HangmanGame":
        p = provider or WordProvider()
        return cls(answer=p.random_phrase(), lives=lives, provider=p)
