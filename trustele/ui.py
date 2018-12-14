import re
import logging
from trustele.forms import mainWindow_ui
from trustele.bots.send import Sender

# my_id format: digit and letter only
RULE1 = "^[A-Za-z0-9]+$"
# telegram username format
# valid format is @blockchainaire or u744728214_12686683581455040581
RULE2 = "^@\w+|u[0-9]{9}_[0-9]{20}$"
# username split rule
RULE3 = "[\s;,|]"

logging.basicConfig(level=logging.INFO, filename='./trustele.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('trustele.ui')


class Ui(mainWindow_ui.Ui_MainWindow):

    def setupUi(self, mw):
        super().setupUi(mw)
        self._prepare()
        log.info('ui initialized...')

    def _prepare(self):
        self.pushButton.clicked.connect(self.on_launch)

    def on_launch(self):
        info = []
        err_flag = False

        log.info("on launch...")
        # clear progress first
        self.progressBar.setValue(0)

        users = self.user_area.toPlainText()
        # split, trim, duplicate
        user_list = list(set(u.strip() for u in re.split(RULE3, users) if u))

        if len(user_list) == 0:
            err_flag = True
            info.append('[ERROR] no user to send')

        valid_user_list = [u for u in user_list if re.match(RULE2, u)]
        invalid_user_list = [u for u in user_list if not re.match(RULE2, u)]

        if len(invalid_user_list) > 0:
            err_flag = True
            info.append('[ERROR] invalid user names:')
            info.extend(invalid_user_list)

        self.user_area.setText('\n'.join(valid_user_list))

        my_id = self.my_id.text().strip()
        if not re.match(RULE1, my_id):
            err_flag = True
            info.append('[ERROR] only digit and letters is valid in User ID \n')

        msg = self.msg_area.toPlainText()
        if len(msg) == 0:
            err_flag = True
            info.append('[ERROR] empty message')

        if err_flag:
            self.info_area.setText('\n'.join(info))
            return
        else:
            self.info_area.clear()
            log.info("launch sender...")
            try:
                sender = Sender(my_id)
                for progress in sender.launch(valid_user_list, msg):
                    self.progressBar.setValue(progress)
            except Exception as e:
                log.error(str(e))
