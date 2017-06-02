# Qt imports
from PyQt5.QtWidgets import QApplication

# Python imports
import sys

# Local includes
from bubbly_pom.bubbly_pom import BubblyPom


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    a = BubblyPom()

    screenGeometry = QApplication.desktop().screenGeometry()
    x = (screenGeometry.width() - a.width()) / 2
    y = (screenGeometry.height() - a.height()) / 2
    a.move(x, y)

    a.show()
    app.exec_()


if __name__ == '__main__':
    main()
