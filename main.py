import sys

from PyQt5.QtWidgets import QApplication

from utils import ZennerWindow


def main():
    app = QApplication(sys.argv)
    w = ZennerWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

