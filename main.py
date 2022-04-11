# made by HyungJin Bang

from pynput import mouse


def on_click(x, y, button, pressed):
    if button.left and pressed:
        print('Pressed at {0}'.format((x, y)))


if __name__ == '__main__':
    mouse_click_counter = 0
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    if mouse_click_counter > 1:
        listener.stop()

