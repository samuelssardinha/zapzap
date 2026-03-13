from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QByteArray, Qt, QEvent, QBuffer, QTimer, QIODevice
from PyQt6.QtGui import QImage

from zapzap.controllers.QtoasterDonation import QtoasterDonation
from zapzap.controllers.Settings import Settings
from zapzap.controllers.Browser import Browser
from zapzap.controllers.ShortcutsDialog import ShortcutsDialog

from zapzap.services.AlertManager import AlertManager
from zapzap.services.SettingsManager import SettingsManager
from zapzap.services.SysTrayManager import SysTrayManager
from zapzap.services.ThemeManager import ThemeManager

from zapzap.views.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.setMinimumSize(0, 0)

        # largura fixa estilo macOS Settings
        self.setFixedWidth(1080)

        self.is_fullscreen = False
        self.browser = Browser(self)
        self.app_settings = None
        self._last_sanitized_key = None

        # flag para encerramento forçado
        self._force_quit = False

        self._setup_ui()

        if not SettingsManager.get("notification/donation_message", False):
            QtoasterDonation.showMessage(parent=self)

    # =========================================================
    # Setup inicial
    # =========================================================

    def _setup_ui(self):

        self.stackedWidget.addWidget(self.browser)

        self.stackedWidget.currentChanged.connect(self._adjust_window_size)

        self._connect_menu_actions()
        self.settings_menubar()

        self.set_sidebar_visible(
            SettingsManager.get("system/sidebar", True),
            animated=False,
            persist=False,
        )

    # =========================================================
    # Resize automático
    # =========================================================

    def _adjust_window_size(self):

        page = self.stackedWidget.currentWidget()

        if not page:
            return

        page.adjustSize()

        content_height = page.sizeHint().height()

        screen = self.screen().availableGeometry()

        max_height = screen.height()

        height = min(max(self.height(), content_height), max_height)

        self.resize(self.width(), height)

    # =========================================================
    # Eventos do sistema
    # =========================================================

    def changeEvent(self, event):

        super().changeEvent(event)

        if event.type() == QEvent.Type.ActivationChange and self.isActiveWindow():

            clipboard = QApplication.clipboard()

            if not clipboard.image().isNull():
                QTimer.singleShot(50, self._on_paste)

    def _on_paste(self):

        clipboard = QApplication.clipboard()
        image = clipboard.image()

        if image.isNull():
            return

        if image.cacheKey() == self._last_sanitized_key:
            return

        self._last_sanitized_key = image.cacheKey()

        buffer = QBuffer()

        try:

            buffer.open(QIODevice.OpenModeFlag.ReadWrite)

            if image.save(buffer, "PNG"):

                clean_img = QImage()
                clean_img.loadFromData(buffer.data(), "PNG")

                QTimer.singleShot(
                    0,
                    lambda img=clean_img.copy(): clipboard.setImage(img)
                )

        finally:
            buffer.close()

    # =========================================================
    # Configurações salvas
    # =========================================================

    def load_settings(self):

        self.restoreGeometry(
            SettingsManager.get("main/geometry", QByteArray())
        )

        self.restoreState(
            SettingsManager.get("main/windowState", QByteArray())
        )

        SysTrayManager.start()
        ThemeManager.start()

    # =========================================================
    # Menu
    # =========================================================

    def _connect_menu_actions(self):

        self._connect_file_menu_actions()
        self._connect_view_menu_actions()
        self._connect_help_menu_actions()

    def _connect_file_menu_actions(self):

        self.actionSettings.triggered.connect(self.open_settings)

        # Quit agora encerra o app corretamente
        self.actionQuit.triggered.connect(self.quit_app)

        self.actionHide.triggered.connect(self.hide)

        self.actionReload.triggered.connect(self.browser.reload_pages)
        self.actionNew_chat.triggered.connect(self.new_chat)
        self.actionBy_phone_number.triggered.connect(self.new_chat_by_phone)

        self.actionSobre_o_ZapZap.triggered.connect(self.open_about)

    def _connect_view_menu_actions(self):

        self.actionOpen_DevTools.triggered.connect(self.open_devtools)
        self.actionToggle_sidebar.triggered.connect(self.set_sidebar_visible)

        self.actionReset_zoom.triggered.connect(self._reset_zoom)
        self.actionToggle_full_screen.triggered.connect(self.toggle_fullscreen)
        self.actionZoom_in.triggered.connect(self._zoom_in)
        self.actionZoom_out.triggered.connect(self._zoom_out)

    def _connect_help_menu_actions(self):

        self.actionShortcuts.triggered.connect(
            lambda: ShortcutsDialog().exec()
        )

    # =========================================================
    # Sidebar
    # =========================================================

    def set_sidebar_visible(self, visible: bool, animated=True, persist=True):

        self.browser.set_sidebar_visible(visible, animated=animated)

        self.actionToggle_sidebar.blockSignals(True)
        self.actionToggle_sidebar.setChecked(visible)
        self.actionToggle_sidebar.blockSignals(False)

        if persist:
            SettingsManager.set("system/sidebar", visible)

    # =========================================================
    # Chat
    # =========================================================

    def new_chat(self):

        try:
            self._current_page().page().new_chat()
        except Exception:
            AlertManager.no_active_account()

    def new_chat_by_phone(self):

        try:
            self._current_page().page().open_chat_by_number()
        except Exception:
            AlertManager.no_active_account()

    # =========================================================
    # Zoom
    # =========================================================

    def _reset_zoom(self):
        self._current_page().set_zoom_factor_page()

    def _zoom_in(self):
        self._current_page().set_zoom_factor_page(+0.1)

    def _zoom_out(self):
        self._current_page().set_zoom_factor_page(-0.1)

    # =========================================================
    # DevTools
    # =========================================================

    def open_devtools(self):

        try:
            self._current_page().open_devtools()
        except Exception:
            AlertManager.no_active_account()

    # =========================================================
    # Página atual
    # =========================================================

    def _current_page(self):
        return self.browser.pages.currentWidget()

    # =========================================================
    # Fullscreen
    # =========================================================

    def toggle_fullscreen(self):

        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()

    # =========================================================
    # Encerrar aplicação
    # =========================================================

    def quit_app(self):

        self._force_quit = True

        self._save_window_state()

        if self.app_settings:
            self.close_settings()

        if self.browser:
            self.browser.close_conversations()
            self.browser.deleteLater()

        QApplication.instance().quit()

    # =========================================================
    # Fechamento da janela
    # =========================================================

    def closeEvent(self, event):

        self._save_window_state()

        if self._force_quit:
            event.accept()
            return

        if not SettingsManager.get("system/quit_in_close", False):
            self._prepare_for_background(event)
        else:
            event.accept()

    def _save_window_state(self):

        SettingsManager.set("main/geometry", self.saveGeometry())
        SettingsManager.set("main/windowState", self.saveState())

    def _prepare_for_background(self, event):

        if self.app_settings:
            self.close_settings()

        self.browser.close_conversations()

        self.hide()

        if event:
            event.ignore()

    # =========================================================
    # Mostrar / esconder janela
    # =========================================================

    def show_window(self):

        if self.isHidden():

            if self.is_fullscreen:
                self.showFullScreen()
            else:
                self.showNormal()

            QApplication.instance().setActiveWindow(self)

        elif not self.isActiveWindow():

            self.activateWindow()
            self.raise_()

        else:
            self.hide()

    # =========================================================
    # Configurações
    # =========================================================

    def open_settings(self):

        if self.app_settings:
            return

        self.app_settings = Settings(self)

        self.stackedWidget.addWidget(self.app_settings)
        self.stackedWidget.setCurrentWidget(self.app_settings)

        self._adjust_window_size()

    def close_settings(self):

        if not self.app_settings:
            return

        self.stackedWidget.removeWidget(self.app_settings)
        self.app_settings.deleteLater()
        self.app_settings = None

        self.stackedWidget.setCurrentWidget(self.browser)

    def open_about(self):

        self.open_settings()

        if self.app_settings:
            self.app_settings.open_about()

    # =========================================================
    # Notificações externas
    # =========================================================

    def xdgOpenChat(self, url):

        try:
            self._current_page().page().xdg_open_chat(url)
        except Exception:
            AlertManager.no_active_account()

    # =========================================================
    # Menu bar
    # =========================================================

    def settings_menubar(self):

        if SettingsManager.get("system/menubar", True):
            self.menubar.setMaximumHeight(2000)
        else:
            self.menubar.setMaximumHeight(0)
            
        