import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


def calculate():
    print("Рассчет")

############### парсинг введеной строки в
    mask = window.lineEdit_mask.text()
    mask_octets_dec = [int(x) for x in mask.split('.')];
    mask_octets_dec_reverse = [(255 - int(x)) for x in mask.split('.')]
    mask_octets_str_reverse = [str(255 - int(x)) for x in mask.split('.')]

############### вычисление префикса исходя из маски
    prefix = 0
    for i in mask_octets_dec:
        prefix += bin(i).count('1')

############### получение введенного ip и разбиение его на октеты в виде списка
    ip_addr = window.lineEdit_ip.text()
    ip_octets_dec = [int(x) for x in ip_addr.split('.')]

############### вывод в таблицу заданного ip
    window.tableWidget.setItem(0, 0, QTableWidgetItem(ip_addr))

############### вывод в таблицу заданного ip в hex
    add_to_table(0, 1, ip_octets_dec, "{:02X}")

############### вывод в таблицу заданного ip в bin
    add_to_table(0, 2, ip_octets_dec, "{:08b}")

############### вывод в таблицу префикса
    window.tableWidget.setItem(1, 0, QTableWidgetItem("/" + str(prefix)))

############### вывод в таблицу маски
    window.tableWidget.setItem(2, 0, QTableWidgetItem(mask))

############### вывод в таблицу заданной маски в hex
    add_to_table(2, 1, mask_octets_dec, "{:02X}")

############### вывод в таблицу заданной маски в bin
    add_to_table(2, 2, mask_octets_dec, "{:08b}")

############### вывод в таблицу обратной маски
    window.tableWidget.setItem(3, 0, QTableWidgetItem('.'.join(mask_octets_str_reverse)))

############### вывод в таблицу обратной маски в hex
    add_to_table(3, 1, mask_octets_dec_reverse, "{:02X}")

############### вывод в таблицу обратной маски в bin
    add_to_table(3, 2,mask_octets_dec_reverse, "{:08b}")

############### рассчет и вывод в таблицу ip адреса сети
    print_ip_network_addr = []
    for i, x in enumerate(mask_octets_dec):
        print_ip_network_addr.append(x & ip_octets_dec[i])
    add_to_table(4, 0, print_ip_network_addr, "{:d}")

############### рассчет и вывод в таблицу ip адреса сети в hex
    for i, x in enumerate(print_ip_network_addr):
        print_ip_network_addr[i] = int(x)
    add_to_table(4, 1, print_ip_network_addr, "{:02X}")

############### рассчет и вывод в таблицу ip адреса сети в bin
    add_to_table(4, 2, print_ip_network_addr, "{:08b}")

############### рассчет и вывод в таблицу широковещательного адреса в dec
    ip_open = []
    for i, x in enumerate(print_ip_network_addr):
        ip_open.append(x | mask_octets_dec_reverse[i])
    add_to_table(5, 0, ip_open, "{:d}")

############### вывод в таблицу широковещательного адреса в hex
    add_to_table(5, 1, ip_open, "{:02X}")

############### рассчет и вывод в таблицу широковещательного адреса в bin
    add_to_table(5, 2, ip_open, "{:08b}")

############### рассчет и вывод в таблицу адреса первого хоста
    temp = print_ip_network_addr
    temp[-1] = 1
    add_to_table(6, 0, temp, "{:d}")

############### вывод в таблицу адреса первого хоста в hex
    add_to_table(6, 1, temp, "{:02X}")

############### вывод в таблицу адреса первого хоста в bin
    add_to_table(6, 2, temp, "{:08b}")

############### рассчет и вывод в таблицу адреса последнего хоста
    ip_last_host = []
    for i, x in enumerate(mask_octets_dec_reverse):
        ip_last_host.append(x | ip_octets_dec[i])
    ip_last_host[-1] -= 1
    add_to_table(7, 0, ip_last_host, "{:d}")

############### рассчет и вывод в таблицу адреса последнего хоста hex
    add_to_table(7, 1, ip_last_host, "{:02X}")

############### рассчет и вывод в таблицу адреса последнего хоста bin
    add_to_table(7, 2, ip_last_host, "{:08b}")

############### рассчет и вывод в таблицу количество доступных адресов
    window.tableWidget.setItem(8, 0, QTableWidgetItem(str(2 ** (32 -prefix))))

############### рассчет и вывод в таблицу количество доступных адресов
    window.tableWidget.setItem(9, 0, QTableWidgetItem(str(2 ** (32 -prefix) - 2)))

def add_to_table(row, column, data, type_print):
    print_str = []
    for i in data:
        print_str.append(type_print.format(i))
    window.tableWidget.setItem(row, column, QTableWidgetItem('.'.join(print_str)))

class MainWindow(QMainWindow):
   def __init__(self):
      super(MainWindow, self).__init__()
      uic.loadUi('gui.ui', self)




if __name__ == '__main__':
    app =  QApplication(sys.argv)   # создание объекта самого приложения
    window = MainWindow()           # создание объекта единственного окна

    window.lineEdit_ip.editingFinished.connect(calculate)       # при окончании редактирования вызов функции перерасчета
    window.lineEdit_mask.editingFinished.connect(calculate)     #

    window.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # запрет редактирования таблицы

    reg_ex = QRegExp("([0-9]{1,3}\.){3}[0-9]{1,3}") # валидатор ip адреса, не позволяет ввести бред
    input_validator = QRegExpValidator(reg_ex, window.lineEdit_ip)
    window.lineEdit_ip.setValidator(input_validator)

    reg_ex = QRegExp("([0-8]{1,3}\.){1,3}[0-8]{1,3}")  # валидатор ip адреса, не позволяет ввести бред
    input_validator = QRegExpValidator(reg_ex, window.lineEdit_mask)
    window.lineEdit_mask.setValidator(input_validator)

    window.show()
    sys.exit(app.exec_())

