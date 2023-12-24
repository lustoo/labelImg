from PyQt5 import QtCore, QtGui, QtWidgets

from Ui_label_window import Ui_LabelWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class LabelWindow(QDialog,Ui_LabelWindow):
    def __init__(self,dir_path=None) -> None:
        super().__init__()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui =LabelWindow()  
    ui.initUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())