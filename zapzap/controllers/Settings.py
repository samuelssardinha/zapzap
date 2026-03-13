from PyQt6.QtWidgets import QWidget, QApplication, QButtonGroup, QStyle
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QGuiApplication, QIcon

# páginas
from zapzap.controllers.PageGeneral import PageGeneral
from zapzap.controllers.PageAbout import PageAbout
from zapzap.controllers.PageNetwork import PageNetwork
from zapzap.controllers.PageNotifications import PageNotifications
from zapzap.controllers.PageAccount import PageAccount
from zapzap.controllers.PageAppearance import PageAppearance
from zapzap.controllers.PageCustomizations import PageCustomizations
from zapzap.controllers.PagePerformance import PagePerformance

# interface
from zapzap.views.ui_settings import Ui_Settings


class Settings(QWidget, Ui_Settings):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        # ---------------------------------------------------------
        # tamanho da janela
        # ---------------------------------------------------------

        screen = QGuiApplication.primaryScreen()
        available = screen.availableGeometry()

        height = int(available.height() * 0.75)
        width = int(available.width() * 0.8)

        self.setFixedHeight(height)
        self.setMaximumWidth(width)

        # largura da sidebar
        self.sidebar.setMinimumWidth(260)

        # mapa botão -> página
        self.page_buttons = {}

        # grupo exclusivo de botões
        self.sidebar_group = QButtonGroup(self)
        self.sidebar_group.setExclusive(True)

        # setup
        self._setup_ui()
        self._setup_signals()
        self._select_default_page()

    # =========================================================
    # UI
    # =========================================================

    def _setup_ui(self):

        # ---------------------------------------------------------
        # estilo sidebar
        # ---------------------------------------------------------

        self.sidebar.setStyleSheet("""
        QPushButton {
            text-align: left;
            padding: 8px 12px;
            border-radius: 8px;
            border: none;
            font-size: 13px;
        }

        QPushButton:hover {
            background-color: rgba(255,255,255,0.06);
        }

        QPushButton:checked {
            background-color: rgba(0,122,255,0.35);
            color: white;
        }

        QLabel {
            font-size: 11px;
            color: rgba(255,255,255,0.55);
            padding-left: 10px;
            margin-top: 12px;
        }
        """)

        # ---------------------------------------------------------
        # botões da sidebar
        # ---------------------------------------------------------

        buttons = [
            self.btn_page_general,
            self.btn_account,
            self.btn_page_appearence,
            self.btn_page_customizations,
            self.btn_page_notifications,
            self.btn_page_performance,
            self.btn_page_network,
            self.btn_page_help
        ]

        for btn in buttons:
            btn.setMinimumHeight(32)
            btn.setIconSize(QSize(18, 18))
            btn.setCheckable(True)
            self.sidebar_group.addButton(btn)

        # ---------------------------------------------------------
        # ícones
        # ---------------------------------------------------------
        style = QApplication.style()

        # General
        self.btn_page_general.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        )

        # Accounts
        self.btn_account.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )

        # Network
        self.btn_page_network.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        )

        # Notifications
        self.btn_page_notifications.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        )

        # Appearance
        self.btn_page_appearence.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )

        # Customizations
        self.btn_page_customizations.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        )

        # Performance
        self.btn_page_performance.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_DriveHDIcon)
        )

        # Help / About
        self.btn_page_help.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )

        # ---------------------------------------------------------
        # páginas
        # ---------------------------------------------------------

        self._add_page(PageGeneral(), self.btn_page_general)
        self._add_page(PageAccount(), self.btn_account)
        self._add_page(PageAppearance(), self.btn_page_appearence)
        self._add_page(PageCustomizations(), self.btn_page_customizations)
        self._add_page(PageNotifications(), self.btn_page_notifications)
        self._add_page(PageNetwork(), self.btn_page_network)
        self._add_page(PagePerformance(), self.btn_page_performance)
        self._add_page(PageAbout(), self.btn_page_help)

    # =========================================================
    # SIGNALS
    # =========================================================

    def _setup_signals(self):

        app = QApplication.instance()

        if not app or not hasattr(app, "getWindow"):
            return

        window = app.getWindow()

        if not window:
            return

        self.btn_quit.clicked.connect(window.close)
        self.btn_back.clicked.connect(window.close_settings)

    # =========================================================
    # PAGES
    # =========================================================

    def _add_page(self, page: QWidget, button):

        index = self.pages.addWidget(page)

        self.page_buttons[index] = button

        button.clicked.connect(lambda _, p=page: self.switch_to_page(p))

        page.setSizePolicy(
            page.sizePolicy().Policy.Expanding,
            page.sizePolicy().Policy.Preferred
        )

    def switch_to_page(self, page: QWidget):

        if self.pages.currentWidget() == page:
            return

        # troca página
        self.pages.setCurrentWidget(page)

        # marca botão correspondente
        button = self.page_buttons[self.pages.indexOf(page)]
        button.setChecked(True)

        # ajusta layout
        page.adjustSize()

        app = QApplication.instance()

        if app and hasattr(app, "getWindow"):
            window = app.getWindow()

            if window:
                window._adjust_window_size()

    def _select_default_page(self):

        if self.page_buttons:
            first_page = self.pages.widget(0)
            self.switch_to_page(first_page)

    # =========================================================
    # ABOUT
    # =========================================================

    def open_about(self):

        self.btn_page_help.click()