import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


def calculate():
    print("Рассчет")
    window.lineEdit_ip.clear()

def clear():
    print("clear")
    window.lineEdit_ip.clear()

class MainWindow(QMainWindow):
   def __init__(self):
      super(MainWindow, self).__init__()
      uic.loadUi('gui.ui', self)




if __name__ == '__main__':
    app =  QApplication(sys.argv)
    window = MainWindow()

    window.lineEdit_ip.editingFinished.connect(calculate)
    window.lineEdit_mask.editingFinished.connect(calculate)


    reg_ex = QRegExp("([0-9]{1,3}\.){3}[0-9]{1,3}")
    input_validator = QRegExpValidator(reg_ex, window.lineEdit_ip)
    window.lineEdit_ip.setValidator(input_validator)


    window.show()
    sys.exit(app.exec_())

