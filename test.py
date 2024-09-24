from src.llvim.emulator import VimEmulator

def main():
    with open('test.txt') as f:
        document_text = f.read()
    emulator = VimEmulator(document_text, window_height=5)

    emulator.execute_command('yy')
    print(emulator.get_clipboard_content())


if __name__ == '__main__':
    main()