def on_received_string(receivedString):
    serial.write_line(receivedString)
radio.on_received_string(on_received_string)

radio.set_group(42)
# 送信機と同じグループ番号
serial.redirect_to_usb()
# 起動確認用
basic.show_icon(IconNames.YES)