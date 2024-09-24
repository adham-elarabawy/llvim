import pynvim
from typing import Annotated

Char = Annotated[str, "Single character"]

class VimEmulator:
    def __init__(self, document_text, window_height=10, visual_mode_register: Char ='z'):
        assert len(visual_mode_register) == 1
        self.nvim = pynvim.attach('child', argv=["nvim", "--embed", "--headless"])
        self.nvim.command(f'set lines={window_height}')
        self.nvim.current.buffer[:] = document_text.splitlines()
        self.visual_mode_register = visual_mode_register
        self.nvim.call('setreg', visual_mode_register, '')
        self.alive = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def execute_command(self, command):
        self.nvim.command(f'normal! {command}')
        return self.get_window_content()

    def _clean(self, text: str) -> str:
        return text.strip()

    def get_window_content(self):
        return self._clean('\n'.join(self.nvim.current.buffer[:]))

    def get_visual_selection(self):
        current_pos = self.nvim.current.window.cursor
        self.nvim.command('normal! gv')
        self.nvim.command(f'normal! "{self.visual_mode_register}y')
        content = self._clean(self.nvim.eval(f'@{self.visual_mode_register}'))
        self.nvim.current.window.cursor = current_pos

        return content

    def get_clipboard_content(self):
        return self._clean(self.nvim.eval('@"'))

    def get_cursor_position(self):
        return self.nvim.current.window.cursor

    def close(self):
        if self.alive:
            self.nvim.quit()
            self.alive = False

    def __del__(self):
        self.close()