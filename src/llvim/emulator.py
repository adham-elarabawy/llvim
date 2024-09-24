from typing import Annotated

import pynvim

Char = Annotated[str, "Single character"]


class VimEmulator:
    def __init__(
        self, document_text: str, window_height: int, visual_mode_register: Char = "z"
    ):
        assert len(visual_mode_register) == 1
        self.nvim = pynvim.attach("child", argv=["nvim", "--embed", "--headless"])
        self.nvim.command(f"set lines={window_height}")
        self.nvim.current.buffer[:] = document_text.splitlines()
        self.visual_mode_register = visual_mode_register
        self.nvim.call("setreg", visual_mode_register, "")
        self.alive = True
        self.window_height = window_height
        self._clear_registers()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _clear_registers(self):
        registers = list("abcdefghijklmnopqrstuvwxyz0123456789")
        for reg in registers:
            self.nvim.call("setreg", reg, "")

    def execute_command(self, command):
        if command.startswith("/") or command.startswith("?"):
            self.nvim.command(command)
        else:
            self.nvim.command(f"normal! {command}")
        return self.get_window_content()

    def _clean(self, text: str) -> str:
        return text.strip()

    def get_window_content(self):
        cursor_line = self.nvim.current.window.cursor[0]
        start_line = max(1, cursor_line - self.window_height // 2)
        end_line = start_line + self.window_height - 1
        visible_lines = self.nvim.current.buffer[start_line - 1 : end_line]
        return self._clean("\n".join(visible_lines))

    def get_visual_selection(self):
        current_pos = self.nvim.current.window.cursor
        self.nvim.command("normal! gv")
        self.nvim.command(f'normal! "{self.visual_mode_register}y')
        content = self._clean(text=self.nvim.eval(f"@{self.visual_mode_register}"))
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
