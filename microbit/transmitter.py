def on_button_pressed_a():
    send("PREV")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_gesture_shake():
    global pointer_mode
    pointer_mode = not (pointer_mode)
    if pointer_mode:
        radio.send_string("POINTER_ON")
        basic.show_leds("""
            . . # . .
            . # # # .
            # . # . #
            . . # . .
            . . # . .
            """)
    else:
        radio.send_string("POINTER_OFF")
        basic.clear_screen()
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

# 傾き値をこれで割って移動量にする
def send(cmd: str):
    global now, last_sent
    now = control.millis()
    if now - last_sent < cool:
        return
    last_sent = now
    radio.send_string(cmd)
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

def on_button_pressed_ab():
    send("BLACK")
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    send("NEXT")
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_logo_pressed():
    send("WHITE")
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

dy2 = 0
dx2 = 0
y2 = 0
x2 = 0
sample_index = 0
last_move = 0
now_ms2 = 0
pointer_mode = False
now = 0
last_sent = 0
cool = 0
y = 0
x = 0
now_ms = 0
last_dy = 0
last_dx = 0
# 状態変数
x_samples = [0, 0, 0, 0]
y_samples = [0, 0, 0, 0]
# 平均を取るサンプル数
sample_count = 4
cool = 350
# ポインター移動の送信間隔(ms)
move_interval = 25
dead_zone = 100
# この値以下の傾きは無視
scale = 40
# 初期化
last_sent = 0
now = 0
pointer_mode = False
radio.set_group(42)
radio.set_transmit_power(7)
# メインループ(ポインター移動の連続送信)

def on_forever():
    global now_ms2, last_move, sample_index, x2, y2, dx2, dy2
    dy = 0
    dx = 0
    if not (pointer_mode):
        return
    now_ms2 = control.millis()
    if now_ms2 - last_move < move_interval:
        return
    last_move = now_ms2
    # 現在の加速度値をバッファに記録
    # 現在の加速度値をバッファに記録
    # 現在の加速度値をバッファに記録
    # 現在の加速度値をバッファに記録
    x_samples[sample_index] = input.acceleration(Dimension.X)
    y_samples[sample_index] = input.acceleration(Dimension.Y)
    sample_index = (sample_index + 1) % sample_count
    # 平均を計算(sumは使えなかったため、素直に)
    x2 = x_samples[0] + x_samples[1] + x_samples[2] + Math.idiv(x_samples[3], sample_count)
    y2 = y_samples[0] + y_samples[1] + y_samples[2] + Math.idiv(y_samples[3], sample_count)
    # デッドゾーン適用
    if abs(x2) < dead_zone:
        x2 = 0
    if abs(y2) < dead_zone:
        y2 = 0
    if x2 == 0 and y2 == 0:
        return
    dx2 = Math.idiv(x2, scale)
    dy2 = Math.idiv(y2, scale)
    if dx == last_dx2 and dy == last_dy2:
        return
    last_dx2 = dx
    last_dy2 = dy
    radio.send_string("MOVE:" + ("" + str(dx2)) + "," + ("" + str(dy2)))
basic.forever(on_forever)
