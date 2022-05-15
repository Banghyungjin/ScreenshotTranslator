# made by HyungJin Bang
from PyQt6.QtCore import QDateTime
from pynput import mouse
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QWidget, QGridLayout, QPushButton, QHBoxLayout, \
    QVBoxLayout, QFileDialog
import configparser
import time
import AppKit
import os
import pyautogui
import sys
import subprocess


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def config_generator():  # 설정파일 만드는 메소드
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


def open_directory():  # 저장 공간 열기
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini', encoding='utf-8')
    path = config_parser['directory']['directory']
    if not os.path.isdir(path):
        os.mkdir(path)
    # os.startfile(path)
    open_file(path)


class ScreenshotTranslator(QWidget):
    def __init__(self):
        super().__init__()
        if not os.path.isfile('config.ini'):
            config_generator()
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        self.storage_text = "현재 저장 장소 = " + config_parser['directory']['directory']
        self.storage_label = QLabel(self.storage_text, self)
        self.cover_text = "현재 촬영할 범위(픽셀) = (" + config_parser['screensize']['axisX1'] + ", " \
                          + config_parser['screensize']['axisY1'] + ") (" + config_parser['screensize']['axisX2'] \
                          + ", " + config_parser['screensize']['axisY2'] + ")"
        self.cover_label = QLabel(self.cover_text, self)
        self.datetime = QDateTime.currentDateTime()
        self.init_ui()

    def init_ui(self):
        # 버튼 생성
        reset_str_btn = QPushButton('저장 장소 초기화')
        reset_str_btn.setToolTip('저장 장소를 초기화 합니다.')
        reset_str_btn.clicked.connect(self.reset_str)  # 버튼이 클릭되면 해당 함수 실행

        save_btn = QPushButton('저장 장소 설정')
        save_btn.setToolTip('스크린샷이 저장될 위치를 선택합니다.')
        save_btn.clicked.connect(self.select_directory)  # 버튼이 클릭되면 해당 함수 실행

        open_btn = QPushButton('저장 장소 열기')
        open_btn.setToolTip('스크린샷이 저장된 위치를 엽니다.')
        open_btn.clicked.connect(open_directory)  # 버튼이 클릭되면 해당 함수 실행

        set_btn = QPushButton('촬영 범위 설정')
        set_btn.setToolTip('스크린샷 촬영 범위를 설정합니다')
        # set_btn.clicked.connect(self.get_mouse)  # 버튼이 클릭되면 해당 함수 실행

        reset_cov_btn = QPushButton('촬영 범위 초기화')
        reset_cov_btn.setToolTip('스크린샷 촬영 범위를 전체 화면 촬영으로 초기화 합니다.')
        # reset_cov_btn.clicked.connect(self.reset_cov)  # 버튼이 클릭되면 해당 함수 실행

        capture_btn = QPushButton('촬영 시작 = Q,  종료 = E')
        capture_btn.setToolTip('스크린샷 촬영을 시작합니다.')
        capture_btn.setShortcut("q")
        # capture_btn.clicked.connect(self.capture)  # 버튼이 클릭되면 해당 함수 실행
        # 박스 레이아웃 생성
        box_1 = QHBoxLayout()
        box_1.addStretch(1)
        box_1.addWidget(QLabel('오늘 날짜 : ' + self.datetime.toString('yyyy 년 MM 월 dd 일')))
        box_1.addStretch(1)

        box_2 = QHBoxLayout()
        box_2.addStretch(1)
        box_2.addWidget(QLabel(
            '현재 화면 크기(픽셀) : 가로 X 세로 : ' + str(screen.frame().size.width for screen in AppKit.NSScreen.screens())
            + ' X ' + str(screen.frame().size.height for screen in AppKit.NSScreen.screens())))  # 현재 화면 크기 출력
        box_2.addStretch(1)

        box_3 = QHBoxLayout()
        box_3.addStretch(1)
        box_3.addWidget(self.cover_label)
        box_3.addStretch(1)

        box_4 = QHBoxLayout()
        box_4.addStretch(1)
        box_4.addWidget(self.storage_label)
        box_4.addStretch(1)

        box_5 = QHBoxLayout()
        box_5.addStretch(1)
        box_5.addWidget(QLabel("사용법 = 촬영 시작 버튼을 누른 뒤 Ctrl + Alt 를 누를 때 마다 스크린샷이 저장됩니다.\n"
                               + "스크린샷을 필요한 만큼 촬영한 뒤에는 E를 눌러 촬영을 종료합니다."))
        box_5.addStretch(1)
        # 그리드 레이아웃 생성
        grid = QGridLayout()
        grid.addWidget(save_btn, 0, 0)
        grid.addWidget(open_btn, 0, 1)
        grid.addWidget(reset_str_btn, 0, 2)
        grid.addWidget(set_btn, 1, 0)
        grid.addWidget(capture_btn, 1, 1)
        grid.addWidget(reset_cov_btn, 1, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(box_1)
        vbox.addLayout(box_2)
        vbox.addLayout(box_4)
        vbox.addLayout(box_3)
        vbox.addLayout(box_5)
        vbox.addLayout(grid)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('Screenshot Translator')
        self.show()

    def select_directory(self):  # 저장 공간 설정
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', QFileDialog.getExistingDirectory(self, "select Directory"))
            config_parser.write(configfile)
        configfile.close()
        self.storage_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.storage_label.repaint()

    def reset_str(self):  # 저장 공간 리셋
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', 'screenshots')
            config_parser.write(configfile)
        configfile.close()
        self.storage_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.storage_label.repaint()


def on_click(x, y, button, pressed):  # 마우스 클릭 x, y 좌표 받아오기
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')
    if button.left and pressed:  # 마우스 왼쪽 버튼 클릭 확인
        with open('config.ini', 'w', encoding='utf-8') as configfile:  # config 파일 열고 좌표 적어 넣기
            if config_parser['mouse_counter']['value'] == '0':
                config_parser.set('screensize', 'axisX1', str(x))
                config_parser.set('screensize', 'axisY1', str(y))
                config_parser.set('mouse_counter', 'value', '1')
            elif config_parser['mouse_counter']['value'] == '1':
                config_parser.set('screensize', 'axisX2', str(x))
                config_parser.set('screensize', 'axisY2', str(y))
                config_parser.set('mouse_counter', 'value', '0')
                coord_arrange(config_parser)
                # 확인을 위해 config에 저장 해놓은 좌표 출력
                print(config_parser['screensize']['axisX1'], config_parser['screensize']['axisY1'])
                print(config_parser['screensize']['axisX2'], config_parser['screensize']['axisY2'])
                listener.stop()  # 마우스 위치 받아오기 종료
                now = time.localtime()  # 저장할 스크린샷 이름에 사용할 현재 시간
                # config directory 위치에 현재 시간을 이름으로 하는 스크린샷 저장
                pyautogui.screenshot(os.path.join(os.getcwd(),
                                                  config_parser['directory']['directory'],
                                                  "%04d-%02d-%02d_%02d:%02d:%02d.png" % \
                                                  (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min,
                                                   now.tm_sec)
                                                  ),
                                     # 스크린샷 x좌표, y좌표, 가로 세로 길이 retina display 에서는 좌표, 크기를 2배로 해야함
                                     region=(float(config_parser['screensize']['axisX1']) * 2,
                                             float(config_parser['screensize']['axisY1']) * 2,
                                             (float(config_parser['screensize']['axisX2']) - float(
                                                 config_parser['screensize']['axisX1'])) * 2,
                                             (float(config_parser['screensize']['axisY2']) - float(
                                                 config_parser['screensize']['axisY1'])) * 2))
                # pyautogui.moveTo(float(config_parser['screensize']['axisX1']),
                #                  float(config_parser['screensize']['axisY1']))
            config_parser.write(configfile)  # 읽어온 마우스 좌표 config에 저장
        configfile.close()  # 저장 후 config 닫기


def coord_arrange(config_parser):  # 받아온 x, y 좌표를 크기 순으로 재배열
    if float(config_parser['screensize']['axisX1']) > float(config_parser['screensize']['axisX2']):
        config_parser['screensize']['axisX1'], config_parser['screensize']['axisX2'] = \
            config_parser['screensize']['axisX2'], config_parser['screensize']['axisX1']
    if float(config_parser['screensize']['axisY1']) > float(config_parser['screensize']['axisY2']):
        config_parser['screensize']['axisY1'], config_parser['screensize']['axisY2'] = \
            config_parser['screensize']['axisY2'], config_parser['screensize']['axisY1']


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScreenshotTranslator()
    sys.exit(app.exec())
    # print('Screenshot Translator by HyungJin Bang\n')
    # with mouse.Listener(on_click=on_click) as listener:
    #     listener.join()
