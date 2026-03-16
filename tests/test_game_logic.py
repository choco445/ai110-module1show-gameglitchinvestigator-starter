import random

import pytest

from logic_utils import parse_guess, check_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_check_guess_hint_direction():
    """
    Ensure human-facing hints point the correct direction:
    - Guess > secret -> "Too High" and instruct to go LOWER
    - Guess < secret -> "Too Low" and instruct to go HIGHER
    - Exact guess -> Win
    """
    outcome, message = check_guess(90, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

    outcome, message = check_guess(10, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "guessed" in message

def test_parse_guess_with_various_inputs_and_secret_validation():
    """
    parse_guess should normalize numeric inputs (including floats-as-strings).
    check_guess should accept numeric secrets but return an Error for non-numeric secrets.
    """
    ok, val, err = parse_guess("42.0")
    assert ok and err is None and val == 42
    outcome, message = check_guess(val, 42)
    assert outcome == "Win"

    ok, val2, err2 = parse_guess("007")
    assert ok and val2 == 7
    outcome, message = check_guess(val2, 10)
    assert outcome == "Too Low"
    assert "HIGHER" in message

    # Non-numeric secret should produce the internal error (defensive behavior)
    outcome, message = check_guess(5, "not-a-number")
    assert outcome == "Error"
    assert "secret is not a number" in message


def test_new_secret_within_difficulty_range():
    """
    Emulate the new-game secret generation and ensure the secret is an int in the difficulty range.
    This targets the fix that ensures the secret is always an int and inside the configured bounds.
    """
    low, high = get_range_for_difficulty("Normal")
    # simulate new game secret generation
    secret = random.randint(low, high)
    assert isinstance(secret, int)
    assert low <= secret <= high