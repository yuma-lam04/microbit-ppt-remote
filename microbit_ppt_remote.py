import serial
from pynput.keyboard import Controller, Key

PORT = "COM4"      
BAUD = 115200

kb = Controller()

def press_key(key):
    kb.press(key)
    kb.release(key)

def handle(cmd: str):
    cmd = cmd.strip().upper()
    if cmd == "NEXT":
        press_key(Key.right)   # PowerPoint 次へ
    elif cmd == "PREV":
        press_key(Key.left)    # 前へ
    elif cmd == "BLACK":
        kb.type('b')           # 黒画面トグル
    elif cmd == "WHITE":
        kb.type('w')           # 白画面トグル

def main():
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print("Listening:", PORT)
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            print("RX:", line)
            handle(line)

if __name__ == "__main__":
    main()
