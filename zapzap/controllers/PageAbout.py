from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

from zapzap.resources.UserIcon import UserIcon
from zapzap.views.ui_page_about import Ui_PageAbout
from zapzap import __website__, __version__

from gettext import gettext as _


class PageAbout(QWidget, Ui_PageAbout):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        # ícone do app
        self.icon.setIcon(UserIcon.get_icon())

        # versão
        self.version.setText(
            _("Version {v}").format(v=__version__)
        )

        # link website
        self.website.setText(
            "<a href='{url}'>Project website</a>".format(url=__website__)
        )

        self.website.setOpenExternalLinks(True)