import re
import os
import logging
import time
from enum import Enum
from trustele.bots import Bot
from trustele.bots.send import Sender
from trustele.forms import mainWindow_ui
from trustele.models.model import TeleUser
from PyQt5 import QtWidgets, QtCore

# my_id format: digit and letter only
RULE1 = "^\+[0-9]+$"
# telegram username format
# valid format is @blockchainaire or u744728214_12686683581455040581
RULE2 = "^@\w+|u[0-9]{9}_[0-9]{20}$"
# username split rule
RULE3 = "[\s;,|]"

logging.basicConfig(level=logging.INFO, filename='./trustele.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('trustele.ui')



class State(Enum):
    unlogged = 1
    to_validate = 2
    logged = 3


class LoginThread(QtCore.QThread):
        signal = QtCore.pyqtSignal('PyQt_PyObject')

        def __init__(self):
            QtCore.QThread.__init__(self)

        def prepare(self, phone_number, phone_callback):
            self.phone_number = phone_number
            self.callback = phone_callback

        def run(self):
            Bot.login(self.phone_number, phone_callback=self.callback)
            self.signal.emit('finished')


class Ui(mainWindow_ui.Ui_MainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.info = []
        self.err_flag = False
        self.bot = None
        self.phone_number = None
        self.valid_code = ''
        self.login_state = State.unlogged
        self.validate_timer = QtCore.QTimer()
        self.login_thread = LoginThread()

    def setupUi(self, mw):
        super().setupUi(mw)
        self._prepare()
        log.info('ui initialized...')

    def _prepare(self):
        self.launch_button.clicked.connect(self.on_launch)
        self.fetch_button.clicked.connect(self.on_fetch)
        self.login_button.clicked.connect(self.on_login)

        self.fetch_select_button.clicked.connect(self.select_all_fetch_user)
        self.fetch_unselect_button.clicked.connect(self.unselect_all_fetch_user)

        self.upload_select_button.clicked.connect(self.select_all_upload_user)
        self.upload_unselect_button.clicked.connect(self.unselect_all_upload_user)
        self.upload_button.clicked.connect(self.on_upload)

        self.user_upload_list.itemClicked.connect(self.refresh_upload_selected)
        self.user_upload_list.currentItemChanged.connect(self.refresh_upload_selected)
        self.user_fetch_list.itemClicked.connect(self.refresh_fetch_selected)
        self.user_fetch_list.currentItemChanged.connect(self.refresh_fetch_selected)

        self.validate_timer.timeout.connect(self.return_unlogged)
        self.validate_timer.setInterval(120000)

        self.login_thread.signal.connect(self.finished)

    def finished(self, result):
        self.validate_timer.stop()

    def return_unlogged(self):
        self.phone_label.setText('My Phone is ')
        self.phone_number_input.setText(self.phone_number)
        self.login_button.setText('Login')
        self.login_state = State.unlogged

    def get_valid_code(self, phone_number=''):
        print('+' * 10)
        valid_code = yield
        return valid_code

    def on_login(self):
        # login state: [unlogged] <-----------logout---------------- [logged]
        # login state: [unlogged] -login-> [to_validate] -validate-> [logged]
        #                       <-timeout- [to_validate]
        if self.login_state == State.unlogged:
            self.phone_number = self.phone_number_input.text().strip()
            if not re.match(RULE1, self.phone_number):
                self._err('invalid phone number format, example +8617612345678\n')
                return

            self.login_button.setDisabled(True)
            self.phone_label.setText('Working...')
            self.phone_number_input.clear()

            self.validate_timer.start()
            self.login_thread.prepare(self.phone_number, self.get_valid_code)
            self.login_thread.start()
            next(self.get_valid_code())

            self.login_state = State.to_validate

            self.phone_label.setText('My Code is ')
            self.login_button.setText('Validate')
            self.login_button.setEnabled(True)
        elif self.login_state == State.to_validate:
            phone_code = self.phone_number_input.text().strip()
            self.login_button.setDisabled(True)
            self.phone_label.setText('Working...')

            self.get_valid_code.send(phone_code)

            self.valid_code = phone_code
            self.login_button.setText('Logout')
            self.login_button.setEnabled(True)
        elif self.login_state == State.logged:
            self.bot.logout()
            self.return_unlogged()

    def on_launch(self):
        log.info("on launch...")
        self.info.clear()
        self.err_flag = False
        self.progressBar.setValue(0)

        if not self.login_state == State.logged:
            self._show_info("not logged in yet")
            return

        msg = self.msg_area.toPlainText()
        if len(msg) == 0:
            self._err('empty message')

        user_list = []
        for upload in self.user_upload_list:
            user_list.append(upload)
        for fetch in self.user_fetch_list:
            user_list.append(fetch)

        if len(user_list) == 0:
            self._err("no user to send")

        if self.err_flag:
            self._show_info()
            return

        log.info("launch sender...")
        try:
            sender = Sender(self.bot.phone)
            for progress in sender.launch(user_list, msg):
                self.progressBar.setValue(progress)
        except Exception as e:
            log.error(str(e))

    def on_fetch(self):
        for u in TeleUser.select():
            display = "%s%s %s (%d)" % (
                u.first_name if u.first_name else '',
                u.last_name if u.last_name else '',
                '@'+u.username if u.username else '', u.id)
            item = QtWidgets.QListWidgetItem(display)
            self.user_fetch_list.addItem(item)
        self.refresh_fetch_selected()

    @staticmethod
    def _format_user_input(raw_users):
        # split, trim, duplicate
        user_list = list(set(u.strip() for u in re.split(RULE3, raw_users) if u))
        valid_user_list = [u for u in user_list if re.match(RULE2, u)]
        invalid_user_list = [u for u in user_list if not re.match(RULE2, u)]
        return valid_user_list, invalid_user_list

    def on_upload(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "User Upload")
        if not os.path.exists(file_name):
            return

        with open(file_name, 'r') as f:
            users = f.read()
            valid_user_list, invalid_user_list = self._format_user_input(users)

            if len(valid_user_list) == 0:
                self._warn('no valid user input')
            else:
                self.user_upload_list.addItems(valid_user_list)

            if len(invalid_user_list) > 0:
                self._warn('invalid user names:')
                self._warn('\n'.join(invalid_user_list), with_tag=False)

        self._show_info()
        self.refresh_upload_selected()

    def _show_info(self, msg=''):
        self.info_area.clear()
        if msg:
            self.info.append(msg)
        self.info_area.setText('\n'.join(self.info))
        self.info.clear()

    def refresh_fetch_selected(self):
        self._refresh_selected(self.user_fetch_list, self.fetch_selected_label)

    def refresh_upload_selected(self):
        self._refresh_selected(self.user_upload_list, self.upload_selected_label)

    @staticmethod
    def _refresh_selected(refresh_list, refresh_label):
        total = len(refresh_list)
        selected = len(refresh_list.selectedItems())
        label_text = '%d / %d selected' % (selected, total)
        refresh_label.setText(label_text)

    def select_all_fetch_user(self):
        self._select_all_user(self.user_fetch_list, self.fetch_selected_label, unselect=False)

    def unselect_all_fetch_user(self):
        self._select_all_user(self.user_fetch_list, self.fetch_selected_label, unselect=True)

    def select_all_upload_user(self):
        self._select_all_user(self.user_upload_list, self.upload_selected_label, unselect=False)

    def unselect_all_upload_user(self):
        self._select_all_user(self.user_upload_list, self.upload_selected_label, unselect=True)

    def _select_all_user(self, user_list, refresh_label, unselect=False):
        if unselect:
            user_list.clearSelection()
        else:
            user_list.selectAll()
        self._refresh_selected(user_list, refresh_label)

    def _err(self, msg, with_tag=True):
        self.err_flag = True
        tag = '[ERROR] ' if with_tag else ''
        self._info(msg, tag)

    def _warn(self, msg, with_tag=True):
        tag = '[WARN] ' if with_tag else ''
        self._info(msg, tag)

    def _info(self, msg, tag):
        assert type(msg) == str
        self.info.append(tag + msg)

