import subprocess
import sys

from os import listdir, path, remove
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal, QTimer, QThread, QTimerEvent

from .barcode import BarCoder


class GThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, nums: tuple, parent=None) -> None:
        QThread.__init__(self, parent)
        self._nums = nums

    def run(self) -> None:
        bc = BarCoder(numbers=self._nums)
        msg = str(bc.create())
        bc.report()
        self.signal.emit(msg)


class TimerMessageBox(QMessageBox):
    """Creates QMessageBox that automatically closes with Qtimer timeout"""
    def __init__(self, msg: str,  timeout=3, parent=None) -> None:
        super(TimerMessageBox, self).__init__(parent)
        self.msg = msg
        self.setWindowTitle("wait")
        self.time_to_wait = timeout
        self.setText(f"{msg}<br>wait (closing automatically in {timeout} secondes.)")
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.change_content)
        self.timer.start()

    def change_content(self) -> None:
        self.setText(f"{self.msg}<br> message box closes automatically in {self.time_to_wait} seconds.)")
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event: QTimerEvent) -> None:
        self.timer.stop()
        event.accept()


def os_start_folder(folder_path: str):
    """Opens file or folder"""
    def _show_file_darwin():
        subprocess.check_call(["open",  folder_path])

    def _show_file_linux():
        subprocess.check_call(["xdg-open",  folder_path])

    def _show_file_win32():
        subprocess.check_call(["explorer", "/select", folder_path])

    try:
        if sys.platform == 'darwin':
            _show_file_darwin()
        elif sys.platform == 'linux':
            _show_file_linux()
        elif sys.platform == 'win32':
            _show_file_win32()
    except Exception as e:
        print(f"Exception occured: {e}")


def clear_folder(folder: str):
    filelist = [f for f in listdir(folder) if f.endswith(".png")]

    for f in filelist:
        remove(path.join(folder, f))
