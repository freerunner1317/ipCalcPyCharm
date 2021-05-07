import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *


def calculate():
    print("Рассчет")

def clear():
    print("clear")

class MainWindow(QMainWindow):
   def __init__(self):
      super(MainWindow, self).__init__()
      uic.loadUi('gui.ui', self)




if __name__ == '__main__':
    app =  QApplication(sys.argv)
    window = MainWindow()

    window.lineEdit_ip.editingFinished.connect(calculate)
    window.lineEdit_mask.editingFinished.connect(calculate)

    window.lineEdit_ip.returnPressed.connect(clear)


    window.show()
    sys.exit(app.exec_())

