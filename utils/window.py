import sys
from os import path, makedirs

from PyQt5.QtWidgets import QMainWindow
from typing import Optional

from config import Settings
from designer import Ui_MainWindow
from utils import GThread, clear_folder, os_start_folder, TimerMessageBox


class ZennerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(ZennerWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.setFixedSize(342, 670)
        self.ui.setupUi(self)
        self.ui.statusbar.showMessage(Settings.STATUS_INIT)
        self.ui.exec_btn.clicked.connect(self.generator_thread)
        self.ui.open_folder_btn.clicked.connect(self.open_folder)
        self.ui.open_file_btn.clicked.connect(self.open_report_file)
        self.ui.clear_folder_btn.clicked.connect(self.clear_generated_folder)
        self.ui.exit_qt_btn.clicked.connect(sys.exit)
        self.gen_thread = None

    def generator_thread(self) -> None:
        _nums = self.get_numbers()
        if _nums:
            self.gen_thread = GThread(nums=self.get_numbers())
            self.gen_thread.started.connect(self.gen_thread_start)
            self.gen_thread.signal.connect(self.on_gen_thread_signal)
            self.gen_thread.finished.connect(self.gen_thread_finish)
            self.gen_thread.start()
        else:
            msg = "Введите номера для генерации!"
            self.show_qt_message(message=msg)

    def gen_thread_start(self):
        self.clear_generated_folder(call_type="thread")
        self.disable_buttons()

    def gen_thread_finish(self):
        self.enable_buttons()
        # erasing input in PlainTextBox numbers
        if self.ui.clear_text_check_box.isChecked():
            self.ui.plainTextEdit.setPlainText('')

    def on_gen_thread_signal(self, msg: str):
        self.show_qt_message(message=msg)

    def get_numbers(self) -> Optional[tuple]:
        """Read numbers from PlainTextBox"""

        numbers = self.ui.plainTextEdit.toPlainText()
        if numbers:
            num_set = set(numbers.split('\n'))
            if '' in num_set:
                num_set.remove('')
            nums = tuple(num_set)
            return nums

    def disable_buttons(self) -> None:
        self.ui.exec_btn.setEnabled(False)
        self.ui.open_file_btn.setEnabled(False)
        self.ui.open_folder_btn.setEnabled(False)
        self.ui.clear_folder_btn.setEnabled(False)
        self.ui.exit_qt_btn.setEnabled(False)

    def enable_buttons(self) -> None:
        self.ui.exec_btn.setEnabled(True)
        self.ui.open_file_btn.setEnabled(True)
        self.ui.open_folder_btn.setEnabled(True)
        self.ui.clear_folder_btn.setEnabled(True)
        self.ui.exit_qt_btn.setEnabled(True)

    def show_qt_message(self, message: str):
        if self.ui.msg_check_box.isChecked():
            m = TimerMessageBox(msg=message, parent=self)
            m.exec_()

    def clear_generated_folder(self, call_type: str = None) -> None:
        if path.exists(Settings.GENERATED):
            clear_folder(folder=Settings.GENERATED)
        if not call_type:
            self.show_qt_message(message="Папка очищена")

    @staticmethod
    def open_folder() -> None:
        if not path.exists(Settings.GENERATED):
            makedirs(Settings.GENERATED)
        os_start_folder(Settings.GENERATED)

    @staticmethod
    def open_report_file() -> None:
        if path.exists(Settings.INNER_FILE):
            os_start_folder(Settings.INNER_FILE)
        else:
            f = open(Settings.INNER_FILE, "w")
            f.close()
            os_start_folder(Settings.INNER_FILE)
