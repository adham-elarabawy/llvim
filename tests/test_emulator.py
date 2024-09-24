import pytest
from src.llvim.emulator import VimEmulator

@pytest.fixture
def sample_text():
    return """Line 1: This is a test file.
Line 2: It contains multiple lines of text.
Line 3: We can use this to test Vim commands.
Line 4: Each line has some unique content.
Line 5: This is useful for testing yank and delete operations.
Line 6: The file has a total of 8 lines.
Line 7: This is the penultimate line.
Line 8: This is the last line of the file."""

@pytest.fixture
def create_emulator(sample_text):
    def _create_emulator() -> VimEmulator:
        return VimEmulator(sample_text)
    return _create_emulator

def test_initial_content(create_emulator, sample_text):
    with create_emulator() as emulator:
        assert emulator.get_window_content() == sample_text

def test_cursor_movement(create_emulator):
    with create_emulator() as emulator:
        emulator.execute_command('j')
        assert emulator.get_cursor_position() == (2, 0)
        
        emulator.execute_command('5G')
        assert emulator.get_cursor_position() == (5, 0)

def test_visual_selection_character_wise(create_emulator):
    with create_emulator() as emulator:
        emulator.execute_command('v2j')
        selection = emulator.get_visual_selection()
        expected = """Line 1: This is a test file.
Line 2: It contains multiple lines of text.
L"""
        assert selection == expected

def test_visual_selection_line_wise(create_emulator):
    with create_emulator() as emulator:
        emulator.execute_command('V2j')
        selection = emulator.get_visual_selection()
        expected = """Line 1: This is a test file.
Line 2: It contains multiple lines of text.
Line 3: We can use this to test Vim commands."""
        assert selection == expected

def test_complex_command(create_emulator):
    with create_emulator() as emulator:
        emulator.execute_command('3Gvjj')
        selection = emulator.get_visual_selection()
        expected = """Line 3: We can use this to test Vim commands.
Line 4: Each line has some unique content.
L"""
        assert selection == expected

def test_delete_line(create_emulator):
    with create_emulator() as emulator:
        original_content = emulator.get_window_content().splitlines()
        emulator.execute_command('dd')
        new_content = emulator.get_window_content().splitlines()
        assert len(new_content) == len(original_content) - 1
        assert new_content[0] == original_content[1]


def test_initial_state(create_emulator):
    with create_emulator() as emulator:
        assert emulator.get_visual_selection() == ""
        assert emulator.get_clipboard_content() == ""

def test_visual_selection(create_emulator):
    with create_emulator() as emulator:
        emulator.execute_command('v2j')
        selection = emulator.get_visual_selection()
        expected = """Line 1: This is a test file.
Line 2: It contains multiple lines of text.
L"""
        assert selection == expected

        # Check that the selection persists
        assert emulator.get_visual_selection() == expected

        # Clear selection and check it's gone
        emulator.execute_command('\x1b')  # Escape key
        assert emulator.get_visual_selection() == ""

def test_yank_and_paste(create_emulator):
    with create_emulator() as emulator:
        emulator.execute_command('yy')
        assert emulator.get_clipboard_content() == "Line 1: This is a test file."

        emulator.execute_command('p')
        content = emulator.get_window_content().splitlines()
        assert content[0] == content[1] == "Line 1: This is a test file."