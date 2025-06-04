import sys
import os
import types
from unittest.mock import MagicMock

# Ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Create a fake streamlit module
class SessionState(dict):
    def __getattr__(self, name):
        return self.get(name)
    def __setattr__(self, name, value):
        self[name] = value

fake_st = types.SimpleNamespace()
fake_st.session_state = SessionState()
fake_st.balloons = MagicMock()

sys.modules['streamlit'] = fake_st

import test_game_ver2 as game


def test_initialize_game_generates_number_and_resets_attempts():
    fake_st.session_state.clear()
    game.initialize_game()
    secret = fake_st.session_state.secret_number
    attempts = fake_st.session_state.attempts
    assert 1 <= secret <= 100
    assert attempts == 0


def test_check_guess_game_over_on_correct_guess():
    fake_st.session_state.clear()
    fake_st.session_state.secret_number = 10
    fake_st.session_state.guess_input = 10
    fake_st.session_state.attempts = 0
    fake_st.session_state.guesses = []
    fake_st.session_state.game_over = False
    fake_st.balloons.reset_mock()

    game.check_guess()

    assert fake_st.session_state.game_over is True
    fake_st.balloons.assert_called_once()


def test_check_guess_game_over_after_five_attempts():
    fake_st.session_state.clear()
    fake_st.session_state.secret_number = 99
    fake_st.session_state.attempts = 0
    fake_st.session_state.guesses = []
    fake_st.session_state.game_over = False
    fake_st.balloons.reset_mock()

    for _ in range(5):
        fake_st.session_state.guess_input = 1  # always wrong
        game.check_guess()

    assert fake_st.session_state.attempts == 5
    assert fake_st.session_state.game_over is True
    fake_st.balloons.assert_not_called()
