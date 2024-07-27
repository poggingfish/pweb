from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pweblib
import os
import json
import hashlib

home = "pweb.pog/index/index"

class Window(QMainWindow):
    fs = 17
    currurl = ""
    currdata = ""
    bookmarks = {}

    def parse_url(self, text):
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
        return [url, sub, page]

    def gopage(self, url = ""):
        if url != "":
            text = url.split("/")
            self.urlbar.setText(url)
        else:
            text = self.urlbar.text().split("/")
        if text[0] == "":
            self.urlbar.setText(home)
            self.gopage(url=home)
            return
        url, sub, page = self.parse_url(text)
        try:
            c = pweblib.read_document(url, sub, page)
        except:
            self.mainview.setPlainText("Page not found!")
            return
        self.mainview.setPlainText(c.decode())
        self.currurl = "/".join(text)
        self.currdata = c.decode()

    def sizechange(self, up = True):
        f = QFont()
        if up:
            self.fs += 1
        else:
            self.fs -= 1
        f.setPixelSize(self.fs)
        self.navbar.setFont(f)
        self.mainview.setFont(f)
        self.bookmarkbar.setFont(f)

    def add_bookmark(self):
        bookmark = {
            self.currurl: {
                "url": self.currurl,
                "hashdata": hashlib.sha256(self.currdata.encode()).hexdigest()
            }
        }
        self.bookmarks.update(bookmark)
        json.dump(self.bookmarks, open(".browserdata/bookmarks.json", "w"))
        self.updatebmbar()

    def remove_bookmark(self, url, newhash):
        del self.bookmarks[url]
        json.dump(self.bookmarks, open(".browserdata/bookmarks.json", "w"))
        self.updatebmbar()
        
    def load_bookmarks(self):
        self.bookmarks = json.load(open(".browserdata/bookmarks.json"))
        self.updatebmbar()

    def bmctx(self, point, url):
        menu = QMenu()
        action = QAction("Remove Bookmark", self)
        action.triggered.connect(lambda b, _=url: self.remove_bookmark(_))
        menu.addAction(action)
        menu.exec(self.mapToGlobal(point))

    def gotopage_hash(self, page: str, newhash: str):
        self.bookmarks[page]["hashdata"] = newhash
        json.dump(self.bookmarks, open(".browserdata/bookmarks.json", "w"))
        self.updatebmbar()
        self.gopage(page)

    def updatebmbar(self):
        self.bookmarkbar.clear()
        for i in self.bookmarks:
            button = QPushButton()
            button.setText(i)
            button.pressed.connect(lambda _=i: self.gopage(_))
            button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            button.customContextMenuRequested.connect(lambda point, _=i: self.bmctx(point, url=_))
            url, sub, page = self.parse_url(i.split("/"))
            try:
                c = pweblib.read_document(url, sub, page)
                h = hashlib.sha256(c.decode().encode()).hexdigest()
                if h != self.bookmarks[i]["hashdata"]:
                    button.pressed.connect(lambda _=i: self.gotopage_hash(_, h))
                    button.setStyleSheet("background-color: yellow") 
            except:
                button.setStyleSheet("background-color: red") 
            self.bookmarkbar.addWidget(button)

    def showCtx(self, point):
        "Displays the context menu"
        menu = QMenu()
        action = QAction("Add Bookmark", self)
        action.triggered.connect(lambda: self.add_bookmark())
        menu.addAction(action)
        menu.exec(self.mapToGlobal(point))

    def init_browser(self):
        try:
            os.mkdir(".browserdata")
        except:
            pass
        if not os.path.exists(".browserdata/bookmarks.json"):
            open(".browserdata/bookmarks.json", "w").write("{}")

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.init_browser()
        self.navbar = QToolBar("navbar", self)
        self.go = QPushButton()
        self.go.setText("Go!")
        self.go.pressed.connect(lambda: self.gopage())
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(lambda: self.gopage())
        self.navbar.addWidget(self.urlbar)
        self.navbar.addWidget(self.go)
        self.addToolBar(self.navbar)
        self.bookmarkbar = QToolBar("bookmarks", self)
        self.addToolBarBreak()
        self.addToolBar(self.bookmarkbar)
        self.mainview = QPlainTextEdit()
        self.mainview.setReadOnly(True)
        self.mainview.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.mainview.customContextMenuRequested.connect(self.showCtx)
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
        self.load_bookmarks()
        self.show()

def main():
    app = QApplication([])
    app.setApplicationName("PWeb UI")
    window = Window()
    app.exec_()

if __name__ == "__main__":
    main()