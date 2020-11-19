# This Python file uses the following encoding: utf-8
import sys
import os


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile
from PyQt5.QtUiTools import QUiLoader


class visPy_Main(QMainWindow):
    def __init__(self):
        super(visPy_Main, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

if __name__ == "__main__":
    app = QApplication([])
    widget = visPy_Main()
    widget.show()
    sys.exit(app.exec_())
