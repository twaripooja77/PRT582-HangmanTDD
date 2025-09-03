from __future__ import annotations
from dataclasses import dataclass
import random
from pathlib import Path
from typing import List, Set


DATA_DIR = Path(__file__).parent / "data"


def _load_lines(file_name: str) -> List[str]:
    path = DATA_DIR / file_name
    with path.open(encoding="utf-8") as f:
        lines = [x.strip() for x in f if x.strip() and not x.startswith("#")]
    return lines


@dataclass
class WordProvider:
 
    words: List[str] | None = None
    phrases: List[str] | None = None
    dictionary: Set[str] | None = None

    def __post_init__(self) -> None:
        if self.words is None:
            self.words = _load_lines("words_en.txt")
        if self.phrases is None:
            self.phrases = _load_lines("phrases_en.txt")
        if self.dictionary is None:
            d: Set[str] = set(w.lower() for w in self.words)
            for p in self.phrases:
                for token in tokenize(p):
                    if token.isalpha():
                        d.add(token.lower())
            self.dictionary = d

    def random_word(self) -> str:
        return random.choice(self.words)

    def random_phrase(self) -> str:
        return random.choice(self.phrases)

    def is_valid_word(self, word: str) -> bool:
        return word.lower() in self.dictionary

    def is_valid_phrase(self, phrase: str) -> bool:
        tokens = tokenize(phrase)
        return all((t.lower() in self.dictionary) if t.isalpha() else True for t in tokens)


def tokenize(text: str) -> List[str]:
   
    out: List[str] = []
    buf = []
    for ch in text:
        if ch.isalpha():
            buf.append(ch)
        else:
            if buf:
                out.append("".join(buf))
                buf = []
            out.append(ch)
    if buf:
        out.append("".join(buf))
    return out
