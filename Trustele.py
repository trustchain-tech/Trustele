import logging
import sys
import qdarkstyle

from trustele.ui import Ui
from PyQt5.QtWidgets import QApplication, QMainWindow

logging.basicConfig(level=logging.INFO, filename='./trustele.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('trustele.main')


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow = QMainWindow()
    ui = Ui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


main()
