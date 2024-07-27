from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pweblib

home = "pweb.pog/index/index"

class Window(QMainWindow):
    fs = 17
    def gopage(self):
        text = self.urlbar.text().split("/")
        if text[0] == "":
            self.urlbar.setText(home)
            self.gopage()
        try:
            url = text[0]
            sub = text[1]
            page = text[2]
        except:

            if len(text) == 1:
                sub = "index"
                page = "index"
            if len(text) == 2:
                page = "index"
        try:
            c = pweblib.read_document(url, sub, page)
        except:
            self.mainview.setPlainText("Page not found!")
            return
        self.mainview.setPlainText(c.decode())

    def sizechange(self, up = True):
        f = QFont()
        if up:
            self.fs += 1
        else:
            self.fs -= 1
        f.setPixelSize(self.fs)
        self.navbar.setFont(f)
        self.mainview.setFont(f)
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.navbar = QToolBar("navbar", self)
        self.go = QPushButton()
        self.go.setText("Go!")
        self.go.pressed.connect(lambda: self.gopage())
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(lambda: self.gopage())
        self.navbar.addWidget(self.urlbar)
        self.navbar.addWidget(self.go)
        self.addToolBar(self.navbar)
        self.mainview = QPlainTextEdit()
        self.mainview.setReadOnly(True)
        self.FontUpKey = QShortcut(self)
        self.FontUpKey.setKey(Qt.Key.Key_Plus)
        self.FontUpKey.activated.connect(lambda: self.sizechange())
        self.FontDownKey = QShortcut(self)
        self.FontDownKey.setKey(Qt.Key.Key_Underscore)
        self.FontDownKey.activated.connect(lambda: self.sizechange(False))
        self.setCentralWidget(self.mainview)
        self.sizechange()
        self.urlbar.setText(home)
        self.gopage()
        self.show()

def main():
    app = QApplication([])
    app.setApplicationName("PWeb UI")
    window = Window()
    app.exec_()

if __name__ == "__main__":
    main()