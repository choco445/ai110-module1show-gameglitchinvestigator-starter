def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode

class GuessResult(tuple):
    """
    Small tuple-like result that keeps backwards compatibility:
    - Unpacks as (outcome, message)
    - Compares equal to just the outcome string for older tests.
    """
    def __new__(cls, outcome, message):
        return tuple.__new__(cls, (outcome, message))

    def __eq__(self, other):
        if isinstance(other, str):
            return tuple.__getitem__(self, 0) == other
        return tuple.__eq__(self, other)


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if isinstance(raw, str) and "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low", "Invalid", "Error"
    """
    # Normalize input types
    try:
        guess_val = int(guess)
    except (ValueError, TypeError):
        return GuessResult("Invalid", "Please enter a valid number.")

    try:
        secret_val = int(secret)
    except (ValueError, TypeError):
        # FIXME: Logic breaks here
        # secret must always be an int. If secret is a string, comparisons become lexicographic
        # and hint directions can be incorrect. Ensure the app sets secret as an int in session state.
        return GuessResult("Error", "Internal error: secret is not a number.")

    # Correct numeric comparison and human-facing hints.
    # If the guess is greater than the secret, the user should be told to go LOWER.
    if guess_val > secret_val:
        return GuessResult("Too High", "📉 Go LOWER!")
    elif guess_val < secret_val:
        return GuessResult("Too Low", "📈 Go HIGHER!")
    else:
        return GuessResult("Win", "🎉 You guessed it!")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
