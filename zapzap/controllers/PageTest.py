from PyQt6.QtWidgets import QWidget
from zapzap.views.ui_page_test import Ui_PageTest


class PageTest(QWidget, Ui_PageTest):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)