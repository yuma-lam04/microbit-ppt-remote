def on_button_pressed_a():
    send("NEXT")
input.on_button_pressed(Button.A, on_button_pressed_a)

# ms
def send(cmd: str):
    global now, last
    now = control.millis()
    if now - last < cool:
        return
    last = now
    serial.write_line(cmd)
    basic.show_string(cmd)
    basic.pause(120)
    basic.clear_screen()

def on_button_pressed_ab():
    send("BLACK")
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    send("PREV")
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_logo_pressed():
    send("WHITE")
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

last = 0
now = 0
cool = 0
# ms
cool = 350
serial.redirect_to_usb()