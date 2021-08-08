# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

"""
功能清单：
1、打印功能：将zebra命令发送到指定接口（a、获取接口清单；b、发送打印命令）
2、数据校验功能：不足28位的二维码不予打印；
3、数据清空功能：打印/校验失败后自动数据清空；
4、绑定快捷键：打印键绑定回车；（未测试）
"""

from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from ui_2 import Ui_MainWindow
import cgitb # 内置的debug log跟踪的模块，可以显示报错处上下文
from zebra import Zebra
import time
import sys

class MainWindow(QMainWindow, Ui_MainWindow):


    def __init__( self, parent=None ):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.mySignal) # 按钮和方法进行绑定
        self.comboBox.addItems(z.getqueues())
        self.comboBox_2.addItems(["打印一张","打印两张","打印三张"])

    # 发射打印信号：
    # 用模板消息生成zpl指令，发送给打印机
    def mySignal(self): # 打印的函数，需要和按钮绑定起来
        qr_code = self.lineEdit.text() # 采集框体的值
        print_io = self.comboBox.currentText()
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print_num = ["打印一张","打印两张","打印三张"].index(self.comboBox_2.currentText())+1 
        # 采集框体的值，并且在列表中找到这个值所映射的int数量，决定了打印指令的重复次数
        try:
            if len(qr_code)==28: # 校验字符串长度
                print("打印成功，打印端口为：",print_io)
                self.print_info = ("""
                        ^XA

                        ^LH100,0
                        ^FO215,20
                        ^BQA,2,6
                        ^FDHA,%s^FS
                        ^FO205,-240
                        ^A0N,24
                        ^FD%s^FS

                        ^FS^XZ
                    """%(qr_code,localtime))
                print(self.print_info*print_num)
                z = Zebra(print_io) # 设置打印机路径
                z.output(self.print_info*print_num) # 发布打印指令,答应指令依据参数print_num重复多次
            else:
                QMessageBox.warning(self, '数据错误', "数据仅%i位数，长度不符！\n无法打印,请重新扫码！"%len(qr_code),QMessageBox.Ok,QMessageBox.Ok) 
        except ValueError:
            cgitb.enable(format='text')
            pass
        """打印完毕之后清空文本框"""
        self.lineEdit.clear()

if __name__ == "__main__":
    z = Zebra() # 这里是打印机队列，确定队列之后可以发起命令
    app = QApplication(sys.argv) # Create the Qt Application

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())