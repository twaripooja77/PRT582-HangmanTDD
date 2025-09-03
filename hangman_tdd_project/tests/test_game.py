import unittest
from hangman.game import HangmanGame, MaskingPolicy
from hangman.words import WordProvider


class HangmanTests(unittest.TestCase):
    def setUp(self):
        self.provider = WordProvider()

    def test_masking_letters_only(self):
        game = HangmanGame(answer="banana", lives=6, provider=self.provider)
        self.assertEqual(game.masked(), "______")
        game.guess("a")
        self.assertEqual(game.masked(), "_a_a_a")
        game.guess("b")
        self.assertEqual(game.masked(), "ba_a_a")
        game.guess("n")
        self.assertEqual(game.masked(), "banana")
        self.assertEqual(game.status, "won")  # all revealed

    def test_wrong_guess_deducts_life(self):
        game = HangmanGame(answer="apple", lives=2, provider=self.provider)
        self.assertEqual(game.remaining_lives(), 2)
        game.guess("z")
        self.assertEqual(game.remaining_lives(), 1)
        game.guess("x")
        self.assertEqual(game.status, "lost")

    def test_timeout_penalty(self):
        game = HangmanGame(answer="apple", lives=2, provider=self.provider)
        game.timeout_penalty()
        self.assertEqual(game.remaining_lives(), 1)
        game.timeout_penalty()
        self.assertEqual(game.status, "lost")


    def test_phrase_masking_and_validation(self):
        game = HangmanGame(answer="data science", lives=6, provider=self.provider)
        # spaces remain visible by default
        self.assertEqual(game.masked(), "____ _______")
        game.guess("e")
        self.assertEqual(game.masked().count("e"), 2)  # 'science' has two e's
        self.assertEqual(game.status, "in_progress")

    def test_masking_policy_all_chars(self):
        game = HangmanGame(answer="unit testing", lives=6, provider=self.provider, masking=MaskingPolicy.ALL_CHARS)
        self.assertEqual(game.masked(), "____ _______")  # space visible, others masked
        # guess all unique letters to win
        for ch in set("unitesting"):
            game.guess(ch)
        self.assertEqual(game.status, "won")


    def test_dictionary_validation(self):
        with self.assertRaises(ValueError):
            HangmanGame(answer="zzzz", lives=6, provider=self.provider)
        with self.assertRaises(ValueError):
            HangmanGame(answer="foo bar baz", lives=6, provider=self.provider)

    def test_random_generators_are_valid(self):
        # Smoke tests using provider's curated lists
        w = self.provider.random_word()
        HangmanGame(answer=w, provider=self.provider)
        p = self.provider.random_phrase()
        HangmanGame(answer=p, provider=self.provider)


if __name__ == "__main__":
    unittest.main()
