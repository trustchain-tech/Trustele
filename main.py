import sys
import re
import logging
import qdarkstyle
import mainWindow
from send import Sender

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

# digit and letter only
RULE1 = "^[A-Za-z0-9]+$"

logging.basicConfig(level=logging.INFO, filename='./trustele.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('trustele.main')


class MyUi(mainWindow.Ui_MainWindow):

    def setupUi(self, mw):
        super().setupUi(mw)
        self._prepare()

    def _prepare(self):
        self.pushButton.clicked.connect(self.on_launch)

    def on_launch(self):
        info = ''
        err_flag = False

        users = self.user_area.toPlainText()
        # split, trim, duplicate
        user_list = list(set(u.strip() for u in re.split('[\s;,|]', users) if u))
        if len(user_list) == 0:
            err_flag = True
            info += '[ERROR] no user to send \n'


        my_id = self.my_id.text().strip()
        if not re.match(RULE1, my_id):
            err_flag = True
            info += '[ERROR] only digit and letters is valid in User ID \n'

        msg = self.msg_area.toPlainText()
        if len(msg) == 0:
            err_flag = True
            info += '[ERROR] empty message \n'

        if err_flag:
            self.info_area.setText(info)
            return
        else:
            self.info_area.clear()
            log.info("launch sender...")
            try:
                sender = Sender(my_id)
                for progress in sender.launch(user_list, msg):
                    self.progressBar.setValue(progress)
            except Exception as e:
                log.error(str(e))


if __name__ == '__main__':
    log.info("starting...")
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    try:
        MainWindow = QMainWindow()
        ui = MyUi()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        log.error(str(e))
