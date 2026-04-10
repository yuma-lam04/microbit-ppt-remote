import serial
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController

PORT = "COM3"
BAUD = 115200

kb = KeyboardController()
mouse = MouseController()

pointer_mode = False


def press_key(key):
    kb.press(key)
    kb.release(key)


def handle(cmd: str):
    global pointer_mode
    cmd = cmd.strip()
    if not cmd:
        return

    # ポインター移動コマンド(例: MOVE:12,-8)
    if cmd.startswith("MOVE:"):
        if not pointer_mode:
            return
        try:
            payload = cmd[5:]
            dx_str, dy_str = payload.split(",")
            dx = int(dx_str)
            dy = int(dy_str)
            mouse.move(dx, dy)
        except (ValueError, IndexError):
            print("Invalid MOVE payload:", cmd)
        return

    # その他のコマンドは大文字化して判定
    cmd = cmd.upper()

    if cmd == "NEXT":
        press_key(Key.right)
    elif cmd == "PREV":
        press_key(Key.left)
    elif cmd == "BLACK":
        kb.type('b')
    elif cmd == "WHITE":
        kb.type('w')
    elif cmd == "POINTER_ON":
        pointer_mode = True
        # PowerPointのレーザーポインターモードを起動
        with kb.pressed(Key.ctrl):
            kb.type('l')
        print("Pointer mode: ON")
    elif cmd == "POINTER_OFF":
        pointer_mode = False
        # PowerPointの通常ポインターに戻す
        with kb.pressed(Key.ctrl):
            kb.type('a')
        print("Pointer mode: OFF")
    else:
        print("Unknown command:", cmd)


def main():
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print("Listening:", PORT)
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            # MOVEコマンドはログが多すぎるので表示しない
            if not line.startswith("MOVE:"):
                print("RX:", line)
            handle(line)


if __name__ == "__main__":
    main()