# -*- coding: utf-8 -*-
import sys
import os
import logging
import threading
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

logger = logging.getLogger(__name__)

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
    logger.debug("Using QtWebEngineWidgets")
except ImportError as e:
    logger.warn("import webEngineWidgets error")
    _import_error = True
else:
    _import_error = False

if _import_error:
    try:
        from PyQt5.QtWebKitWidgets import QWebView
        logger.debug("Using QWebView")
    except ImportError as e:
        logger.warn("import QWebView error")
        _import_error = True
    else:
        _import_error = False


if _import_error:
    raise Exception("This module requires PyQt4 or PyQt5 to work under your system.")

class BrowserView(QMainWindow):
    instance = None
    load_url_trigger = pyqtSignal(str)
    html_trigger = pyqtSignal(str, str)
    dialog_trigger = pyqtSignal(int, str, bool, str)
    destroy_trigger = pyqtSignal()
    fullscreen_trigger = pyqtSignal()
    current_url_trigger = pyqtSignal()

    def __init__(self, title, url, width, height, resizable, fullscreen, min_size):
        super(BrowserView, self).__init__()
        BrowserView.instance = self
        self.is_fullscreen = False

        self._file_name_semaphor = threading.Semaphore(0)
        self._current_url_semaphore = threading.Semaphore()

        self.resize(width, height)
        self.setWindowTitle(title)

        if not resizable:
            self.setFixedSize(width, height)

        self.setMinimumSize(min_size[0], min_size[1])

        #self.view = QWebView(self)
        self.view = QWebView(self)
        self.view.setContextMenuPolicy(Qt.NoContextMenu)  # disable right click context menu

        if url is not None:
            self.view.setUrl(QUrl(url))

        self.setCentralWidget(self.view)
        self.load_url_trigger.connect(self._handle_load_url)
        self.html_trigger.connect(self._handle_load_html)
        #self.dialog_trigger.connect(self._handle_file_dialog)
        self.destroy_trigger.connect(self._handle_destroy_window)
        self.fullscreen_trigger.connect(self._handle_fullscreen)
        #self.current_url_trigger.connect(self._handle_current_url)

        if fullscreen:
            self.toggle_fullscreen()

        self.move(QApplication.desktop().availableGeometry().center() - self.rect().center())
        self.activateWindow()
        self.raise_()
        #webview_ready.set()

    def _handle_get_current_url(self):
        self._current_url = self.view.url().toString()
        self._current_url_semaphore.release()

    def _handle_load_url(self, url):
        self.view.setUrl(QUrl(url))

    def _handle_load_html(self, content, base_uri):
        self.view.setHtml(content, QUrl(base_uri))

    def _handle_destroy_window(self):
        self.close()

    def _handle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()

        self.is_fullscreen = not self.is_fullscreen

    def get_current_url(self):
        self.current_url_trigger.emit()
        self._current_url_semaphore.acquire()

        return self._current_url

    def load_url(self, url):
        self.load_url_trigger.emit(url)

    def load_html(self, content, base_uri):
        self.html_trigger.emit(content, base_uri)

def create_window(title, url=None, width=800, height=600,
                  resizable=True, fullscreen=False, min_size=(200, 100), strings={}):
    app = QApplication([])

    browser = BrowserView(title, url, width, height, resizable, fullscreen, min_size)
    browser.show()
    app.exec_()


def get_current_url():
    return BrowserView.instance.get_current_url()


def load_url(url):
    BrowserView.instance.load_url(url)


def load_html(content, base_uri):
    BrowserView.instance.load_html(content, base_uri)


def destroy_window():
    BrowserView.instance.destroy_()


def toggle_fullscreen():
    BrowserView.instance.toggle_fullscreen()


def create_file_dialog(dialog_type, directory, allow_multiple, save_filename):
    return BrowserView.instance.create_file_dialog(dialog_type, directory, allow_multiple, save_filename)

def _transform_url(url):
    if url == None:
        return url
    if url.find(":") == -1:
        return 'file://' + os.path.abspath(url)
    else:
        return url
