import pyautogui
import string
from multiprocessing.connection import Listener

import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QGridLayout, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pynput.keyboard import Listener, Key
from PyQt5.QtGui import QIcon, QFont


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.searchStr = ''

        self.caps_lock_pressed = False
        self.caps_lock_toggled = False
        # self.windowShow = False;

        # 设置窗口透明
        # self.setWindowOpacity(0.7)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        # 创建网格布局
        self.grid_layout = QGridLayout()
        # grid_layout.

        # characterRange = getCharacterRange()

        # 添加标签到网格布局中
        self.initLables()

        # 将网格布局设置为窗口的布局
        self.setLayout(self.grid_layout)

        # 全屏窗口
        self.showFullScreen()

        # 设置窗口标志，隐藏标题
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        # 设置窗口属性，使其置顶并且不在任务栏上显示
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('resource/pandaFace.ico'))

        # 创建菜单
        self.tray_menu = QMenu(self)
        self.restore_action = self.tray_menu.addAction("Restore")
        self.quit_action = self.tray_menu.addAction("Quit")

        # 关联菜单动作
        self.restore_action.triggered.connect(self.restore_window)
        self.quit_action.triggered.connect(self.quit_application)

        # 设置托盘图标的菜单
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        # 创建键盘监听器线程实例
        self.keyboard_listener = KeyboardListener()
        # 将信号连接到槽函数
        self.keyboard_listener.caps_lock_pressed_twice.connect(self.on_caps_lock_pressed_twice)
        self.keyboard_listener.esc_pressed.connect(self.on_esc_pressed)
        self.keyboard_listener.get_element.connect(self.on_get_ele_pressed)

        # 启动键盘监听器线程
        self.keyboard_listener.start()

        # self.show()

    def initLables(self):
        row = getCharacterRange(46)
        column = getCharacterRange(46)
        self.searchStr = ''
        self.labels = []
        self.labelTexts = []
        for i, rVal in enumerate(row):  # 行
            for j, cVal in enumerate(column):  # 列
                label = QLabel()  # 创建标签
                self.labels.append(label)
                labelText = f'{rVal}{cVal}'
                self.labelTexts.append(labelText)
                label.setText(labelText)
                # 设置字体样式
                # label.setStyleSheet("border:1px solid black;background-color:rgba(255,255,255,0.9);")
                label.setStyleSheet("color:red;background-color:rgba(0,255,0,0.5);")
                # 设置字体样式
                font = QFont()
                font.setPointSize(14)
                # font.setco
                font.setBold(True)
                # font.setStyle()
                font.setFamilies(["Courier New", "Consolas", "Lucida Console", "Microsoft YaHei"])
                label.setFont(font)
                self.grid_layout.addWidget(label, i, j)  # 将标签添加到指定位置的网格中

    def recoverLablesText(self):
        self.searchStr = '';
        for index, label in enumerate(self.labels):
            label.setStyleSheet("color:red;background-color:rgba(0,255,0,0.5);")
            label.setText(self.labelTexts[index])

    def checkBuckWall(self):
        if self.isVisible():
            print("当前窗口正在显示")
            return True
        else:
            print("当前窗口未显示")
            return False

    def on_get_ele_pressed(self, key):

        if not self.checkBuckWall():
            return
        # self.minimumSize()
        old_searchStr = self.searchStr
        self.searchStr += key
        new_searchStr = self.searchStr
        for label in self.labels:
            old_fontStr = f'<font color="blue">{old_searchStr}</font>';
            new_fontStr = f'<font color="blue">{new_searchStr}</font>';
            labelPlainText = label.text()
            if labelPlainText.find('<font') != -1:
                labelPlainText = labelPlainText.replace(old_fontStr, old_searchStr)
            # else:
            #     labelPlainText = labelPlainText.replace(old_searchStr, old_searchStr)
            if labelPlainText == new_searchStr:
                # pos = label.mapToGlobal(label.pos())
                # 获取实际像素值
                pos = label.parentWidget().mapToGlobal(label.pos()) / label.window().devicePixelRatio()
                self.hide()
                # self.tray_icon.show()
                x = pos.x()
                y = pos.y()
                print(f'x:{x}')
                print(f'y:{y}')
                pyautogui.click(x, y)
                self.recoverLablesText()
                break
            if labelPlainText.startswith(new_searchStr):
                # label.setStyleSheet("background-color: yellow;")
                # text = label.text()
                # print('text:' + text)
                # text = labelPlainText.replace(new_searchStr, new_fontStr)
                text = labelPlainText.removeprefix(new_searchStr)
                text = new_fontStr + text
                label.setText(text)
            elif label.text().find(old_fontStr) != -1:
                label.setText(labelPlainText)

        # print('xxxxxxxxx')

    def on_esc_pressed(self):
        # self.minimumSize()
        # self.initLables()
        self.recoverLablesText()
        self.hide()
        # self.tray_icon.show()
        print("maximumSize")

    def on_caps_lock_pressed_twice(self):
        """
        处理连续两次按下CAPS LOCK键的事件

        该方法实现了CAPS LOCK键的双击检测机制：
        - 第一次按下：将caps_lock_pressed标志设为True
        - 第二次按下（连续）：触发主要操作显示窗口

        方法管理两个状态标志：
        - caps_lock_pressed：跟踪是否按过一次CAPS LOCK
        - caps_lock_toggled：表示双击检测成功

        当检测到双击时：
        - 显示主窗口部件
        - 重置跟踪标志
        - 打印"minimumSize"到控制台用于调试
        """
        # self.searchStr = '';
        # self.minimumSize()

        if not self.caps_lock_pressed:
            # 第一次按下CAPS LOCK - 设置标志以跟踪连续按下
            self.caps_lock_pressed = True
        else:
            # 检测到连续第二次按下CAPS LOCK - 触发主要操作
            self.caps_lock_toggled = True
            self.caps_lock_pressed = False
            self.show()  # 显示主窗口部件
            # self.tray_icon.hide()
            print("minimumSize")  # 调试输出

    # def closeEvent(self, event):
    #     # 将窗口隐藏并显示在系统托盘中
    #     event.ignore()
    #     self.hide()
    #     self.tray_icon.show()

    def restore_window(self):
        # 将窗口从系统托盘还原
        self.show()
        self.raise_()
        self.activateWindow()
        self.tray_icon.hide()

    def quit_application(self):
        # 退出应用程序
        self.tray_icon.hide()
        QApplication.quit()


def getCharacterRange(size):
    # 生成包含 a-z 的列表
    letters = list(string.ascii_uppercase)
    # 生成包含 0-9 的列表
    numbers = [str(i) for i in range(10)]
    # 符号
    punctuations = [
        '-', '=',
        # '(', ')', '_', '+',
        '[', ']', '\\',
        # '{', '}','|',
        ';', '\'',
        # ':', '\"',
        ',', '.', '/',
        # '<', '>', '?'
    ]
    # punctuations = []
    # 合并列表
    combined = letters + numbers + punctuations
    result = []
    for i in range(size):
        length = len(combined)
        times = i // length
        ele = combined[i % length]
        eleStr = ele
        for t in range(times):
            eleStr += ele
        result.append(eleStr)
    # for k in combined:
    #     for j in combined:
    #         if len(result) <= size:
    #             result.append(f"{k}{j}")
    # print(result)
    return result


class KeyboardListener(QThread):
    # 自定义信号，用于发射 CAPS LOCK 连续按下事件
    caps_lock_pressed_twice = pyqtSignal()
    esc_pressed = pyqtSignal()
    get_element = pyqtSignal(str)

    def run(self):
        # 开始监听键盘事件
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        pass

    def on_release(self, key):
        # if key == Key.caps_lock:
        char = ''
        try:
            # 判断按下的键是否是字符键
            char = key.char
            print("Character:", char)
            # check is window show now
        except AttributeError as ex:
            # 如果不是字符键，则打印键名
            print("Special Key:", key)
            print(ex)
        print(key)
        if key == Key.esc:
            # 发射 CAPS LOCK 连续按下事件
            self.esc_pressed.emit()
        elif key == Key.caps_lock:
            self.caps_lock_pressed_twice.emit()
        elif char:
            self.get_element.emit(char.upper())


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        widget = MyWidget()
        # sys.exit(app.exec_())
        app.exec_()
    except Exception as e:
        print(e)
