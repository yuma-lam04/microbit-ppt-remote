# 状態変数
pointer_mode = False
last_sent = 0
now = 0
cool = 0
cool = 350
move_interval = 50  # ポインター移動の送信間隔(ms)
last_move = 0
dead_zone = 100     # この値以下の傾きは無視
scale = 50          # 傾き値をこれで割って移動量にする

def send(cmd: str):
    global now, last_sent
    now = control.millis()
    if now - last_sent < cool:
        return
    last_sent = now
    serial.write_line(cmd)
    basic.show_string(cmd)
    basic.pause(120)
    basic.clear_screen()
    # ポインターモード中はアイコンを再表示
    if pointer_mode:
        basic.show_leds("""
            . . # . .
            . # # # .
            # . # . #
            . . # . .
            . . # . .
        """)

def on_button_pressed_a():
    send("PREV")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    send("NEXT")
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_button_pressed_ab():
    send("BLACK")
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_logo_pressed():
    send("WHITE")
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

def on_gesture_shake():
    global pointer_mode
    pointer_mode = not pointer_mode
    if pointer_mode:
        serial.write_line("POINTER_ON")
        basic.show_leds("""
            . . # . .
            . # # # .
            # . # . #
            . . # . .
            . . # . .
        """)
    else:
        serial.write_line("POINTER_OFF")
        basic.clear_screen()
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

# 初期化
last_sent = 0
now = 0
last_move = 0
pointer_mode = False
serial.redirect_to_usb()

# メインループ(ポインター移動の連続送信)
def on_forever():
    global last_move
    if not pointer_mode:
        return
    now_ms = control.millis()
    if now_ms - last_move < move_interval:
        return
    last_move = now_ms
    x = input.acceleration(Dimension.X)
    y = input.acceleration(Dimension.Y)
    # デッドゾーン適用
    if abs(x) < dead_zone:
        x = 0
    if abs(y) < dead_zone:
        y = 0
    if x == 0 and y == 0:
        return
    dx = x // scale
    dy = y // scale
    serial.write_line("MOVE:" + str(dx) + "," + str(dy))

basic.forever(on_forever)