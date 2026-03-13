from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QStyle,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit
)

from zapzap.services.SetupManager import SetupManager
from zapzap.services.AutostartManager import AutostartManager
from zapzap.services.DictionariesManager import DictionariesManager
from zapzap.services.DownloadManager import DownloadManager
from zapzap.services.SettingsManager import SettingsManager

from zapzap.views.ui_page_general import Ui_PageGeneral

from gettext import gettext as _


class PageGeneral(QWidget, Ui_PageGeneral):
    """Gerencia a página de configurações gerais."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self._configure_ui()
        self._load_settings()
        self._configure_signals()

    # =========================================================
    # UI
    # =========================================================

    def _configure_ui(self):

        self.btn_path_download.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )

        self.btn_restore_path_download.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)
        )

        self.btn_path_spell.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        )

        self.btn_default_path_spell.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)
        )

        # Flatpak warning
        if SetupManager._is_flatpak:

            self.btn_wayland.setDisabled(True)
            self.btn_wayland.setToolTip(
                _("Use Flatseal to change this mode of execution")
            )

            flatpak_notice = QLabel(self)
            flatpak_notice.setWordWrap(True)
            flatpak_notice.setTextFormat(Qt.TextFormat.RichText)

            flatpak_notice.setText(
                _(
                    "<b>Flatpak tip:</b> If opening PDFs, drag-and-drop, or file uploads fail, "
                    "this is usually caused by sandbox permissions. "
                    "Open <b>Flatseal</b> and grant ZapZap access to folders like "
                    "Documents, Downloads, Pictures and Videos. "
                    "You can also run: "
                    "<code>flatpak override --user --filesystem=home com.rtosta.zapzap</code>."
                )
            )

            self.frameLayout.insertWidget(1, flatpak_notice)

            flatpak_override_command = (
                "flatpak override --user --filesystem=home com.rtosta.zapzap"
            )

            command_layout = QHBoxLayout()

            command_input = QLineEdit(flatpak_override_command, self)
            command_input.setReadOnly(True)
            command_input.setToolTip(
                _("Select and copy this command in your terminal")
            )

            command_copy_button = QPushButton(_("Copy command"), self)

            command_copy_button.clicked.connect(
                lambda: QApplication.clipboard().setText(
                    flatpak_override_command
                )
            )

            command_layout.addWidget(command_input)
            command_layout.addWidget(command_copy_button)

            self.frameLayout.insertLayout(2, command_layout)

            flatseal_button = QPushButton(_("Open Flatseal page"), self)

            flatseal_button.clicked.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl("https://flathub.org/apps/com.github.tchx84.Flatseal")
                )
            )

            self.frameLayout.insertWidget(3, flatseal_button)

    # =========================================================
    # LOAD SETTINGS
    # =========================================================

    def _load_settings(self):

        self.dic_path.setText(DictionariesManager.get_path())

        self.spellchecker_groupBox.setChecked(
            SettingsManager.get("system/spellCheckers", True)
        )

        self.spell_comboBox.clear()
        self.spell_comboBox.addItems(DictionariesManager.list())

        current_language = DictionariesManager.get_current_dict()
        self.spell_comboBox.setCurrentText(current_language)

        self.download_path.setText(DownloadManager.get_path())

        self.btn_quit_in_close.setChecked(
            SettingsManager.get("system/quit_in_close", False)
        )

        self.btn_start_background.setChecked(
            SettingsManager.get("system/start_background", False)
        )

        self.btn_start_system.setChecked(
            SettingsManager.get("system/start_system", False)
        )

        self.btn_wayland.setChecked(
            SettingsManager.get("system/wayland", False)
        )

        self.dontUseNativeDialog.setChecked(
            SettingsManager.get("system/DontUseNativeDialog", False)
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _configure_signals(self):

        self.spellchecker_groupBox.toggled.connect(
            self._handle_toggled_spellcheck
        )

        self.spell_comboBox.textActivated.connect(
            self._handle_spellcheck
        )

        self.btn_path_spell.clicked.connect(
            self._handle_path_spell
        )

        self.btn_default_path_spell.clicked.connect(
            self._handle_default_folder_spell
        )

        self.btn_path_download.clicked.connect(
            self._handle_path_download
        )

        self.btn_restore_path_download.clicked.connect(
            self._handle_restore_path_download
        )

        self.btn_quit_in_close.clicked.connect(
            lambda: SettingsManager.set(
                "system/quit_in_close",
                self.btn_quit_in_close.isChecked()
            )
        )

        self.btn_start_background.clicked.connect(
            lambda: SettingsManager.set(
                "system/start_background",
                self.btn_start_background.isChecked()
            )
        )

        self.btn_start_system.clicked.connect(
            self._handle_autostart
        )

        self.btn_wayland.clicked.connect(
            lambda: SettingsManager.set(
                "system/wayland",
                self.btn_wayland.isChecked()
            )
        )

        self.dontUseNativeDialog.clicked.connect(
            lambda: SettingsManager.set(
                "system/DontUseNativeDialog",
                self.dontUseNativeDialog.isChecked()
            )
        )

    # =========================================================
    # SPELLCHECK
    # =========================================================

    def _handle_toggled_spellcheck(self, toggled):

        SettingsManager.set("system/spellCheckers", toggled)
        self._update_browser_spellcheck()

    def _handle_spellcheck(self, lang: str):

        DictionariesManager.set_lang(lang)
        self._update_browser_spellcheck()

    def _handle_path_spell(self):

        new_path = DownloadManager.open_folder_dialog(self)

        if new_path:

            self.dic_path.setText(new_path)

            DictionariesManager.set_spell_folder(new_path)

            self._load_settings()
            self._update_browser_spellcheck()

    def _handle_default_folder_spell(self):

        new_path = DictionariesManager.restore_default_path()

        self.dic_path.setText(new_path)

        self._load_settings()
        self._update_browser_spellcheck()

    def _update_browser_spellcheck(self):

        QApplication.instance().getWindow().browser.update_spellcheck()

    # =========================================================
    # DOWNLOAD
    # =========================================================

    def _handle_path_download(self):

        new_path = DownloadManager.open_folder_dialog(self)

        if new_path:

            DownloadManager.set_path(new_path)

            self.download_path.setText(
                DownloadManager.get_path()
            )

    def _handle_restore_path_download(self):

        DownloadManager.restore_path()

        self.download_path.setText(
            DownloadManager.get_path()
        )

    # =========================================================
    # AUTOSTART
    # =========================================================

    def _handle_autostart(self):

        enabled = self.btn_start_system.isChecked()

        SettingsManager.set("system/start_system", enabled)

        AutostartManager.create_desktop_file(enabled)