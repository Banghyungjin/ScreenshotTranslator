# made by HyungJin Bang

from pynput import mouse
import configparser
import time
import AppKit
import os


def config_generator():
    # 설정파일 만들기
    config_parser = configparser.ConfigParser()
    now = time.localtime()

    # 설정파일 오브젝트 만들기
    config_parser['system'] = {}
    config_parser['system']['title'] = 'ScreenshotTranslator'
    config_parser['system']['author'] = 'HyungJin Bang'
    config_parser['system']['version'] = '0.0.1'
    config_parser['system']['update'] = "%04d/%02d/%02d %02d:%02d:%02d" % \
                                        (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    config_parser['directory'] = {}
    config_parser['directory']['directory'] = 'screenshots'

    config_parser['shortcuts'] = {}
    config_parser['shortcuts']['take_shot'] = 'Ctrl + Alt'
    config_parser['screensize'] = {}
    config_parser['screensize']['axisX1'] = '0'
    config_parser['screensize']['axisY1'] = '0'
    config_parser['screensize']['axisX2'] = str(AppKit.NSScreen.mainScreen().frame().size.width)
    config_parser['screensize']['axisY2'] = str(AppKit.NSScreen.mainScreen().frame().size.height)
    config_parser['mouse_counter'] = {}
    config_parser['mouse_counter']['value'] = '0'

    # 설정파일 저장
    with open('config.ini', 'w', encoding='utf-8') as configfile:  # 스크린샷 저장 폴더가 없을 경우 만듬
        config_parser.write(configfile)
    configfile.close()
    path = config_parser['directory']['directory']
    if not os.path.isdir(path):
        os.mkdir(path)


def on_click(x, y, button, pressed):  # 마우스 클릭 읽어오기
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')
    if button.left and pressed:
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            if config_parser['mouse_counter']['value'] == '0':
                config_parser.set('screensize', 'axisX1', str(x))
                config_parser.set('screensize', 'axisY1', str(y))
                config_parser.set('mouse_counter', 'value', '1')
            elif config_parser['mouse_counter']['value'] == '1':
                config_parser.set('screensize', 'axisX2', str(x))
                config_parser.set('screensize', 'axisY2', str(y))
                config_parser.set('mouse_counter', 'value', '0')

            config_parser.write(configfile)
        configfile.close()


if __name__ == '__main__':
    config_generator()

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
