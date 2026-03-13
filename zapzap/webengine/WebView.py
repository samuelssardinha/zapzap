import shutil

# QWebEngineView é o widget que renderiza o Chromium embutido
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Classes principais do WebEngine
# QWebEngineProfile → define perfil (cookies, cache, storage)
# QWebEngineSettings → configurações do navegador
# QWebEnginePage → objeto que controla a página
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage

# Classes utilitárias do Qt
from PyQt6.QtCore import QUrl, pyqtSignal, QTimer

# Acesso à aplicação Qt
from PyQt6.QtWidgets import QApplication

# Usado em menus
from PyQt6.QtGui import QAction


# Controlador da página do WhatsApp
from zapzap.webengine.PageController import PageController

# Modelo de dados de usuário (cada conta)
from zapzap.models import User

# Configurações globais
from zapzap import __user_agent__, __whatsapp_url__

# Sistema de notificações
from zapzap.notifications.NotificationService import NotificationService

# Gerenciamento de dicionários de idioma
from zapzap.services.DictionariesManager import DictionariesManager

# Gerenciador de downloads
from zapzap.services.DownloadManager import DownloadManager

# Configurações persistentes
from zapzap.services.SettingsManager import SettingsManager

# Handler global de crash
from zapzap.debug import crash_handler

from gettext import gettext as _


# WebView representa uma instância isolada do navegador
# Cada conta do WhatsApp cria um WebView independente
class WebView(QWebEngineView):

    # Sinal usado para atualizar número de notificações no botão da conta
    update_button_signal = pyqtSignal(int, int)

    # Tipos possíveis de cache do WebEngine
    QWEBENGINE_CACHE_TYPES = {
        "MemoryHttpCache": QWebEngineProfile.HttpCacheType.MemoryHttpCache,
        "DiskHttpCache": QWebEngineProfile.HttpCacheType.DiskHttpCache,
        "NoCache": QWebEngineProfile.HttpCacheType.NoCache
    }

    def __init__(self, user: User = None, page_index=None, parent=None):

        super().__init__(parent)

        # Usuário associado a este WebView
        self.user = user

        # Índice da página no navegador
        self.page_index = page_index

        # Perfil Chromium usado por esta conta
        self.profile = None

        # Sistema de notificações
        self.notifications = NotificationService()

        # DevTools
        self._devtools_view = None
        self._devtools_page = None

        self._last_tmp_file = None

        # Inicializa apenas se a conta estiver ativa
        if user.enable:
            self._initialize()

    def __del__(self):
        try:
            # Salva nível de zoom quando a página é destruída
            if self.user and not self.isHidden():
                self.user.zoomFactor = self.zoomFactor()
        except RuntimeError:
            pass

    def _initialize(self):

        # Inicialização principal do WebView
        self._configure_signals()
        self._configure_profile()
        self._setup_page()

    def _configure_signals(self):

        # Conecta eventos importantes
        self.titleChanged.connect(self._on_title_changed)
        self.loadFinished.connect(self._on_load_finished)

    def _configure_profile(self):

        # Cria um perfil Chromium isolado por usuário
        # storageName = id do usuário
        self.profile = QWebEngineProfile(str(self.user.id), self)

        # Define User-Agent customizado
        self.profile.setHttpUserAgent(__user_agent__)

        # Conecta downloads ao gerenciador
        self.profile.downloadRequested.connect(
            lambda download: DownloadManager.on_downloadRequested(
                download,
                self
            )
        )

        # Conecta notificações ao sistema interno
        self.profile.setNotificationPresenter(
            lambda notification: self.notifications.notify(self, notification)
        )

        # Habilita/desabilita animação de scroll
        self.profile.settings().setAttribute(
            QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled,
            SettingsManager.get("web/scroll_animator", False))

        self.configure_spellcheck()

        # Configura tamanho máximo do cache
        size_cache = SettingsManager.get("performance/cache_size_max", 0)

        self.profile.setHttpCacheMaximumSize(1024 * 1024 * int(size_cache))

        # Define tipo de cache
        self.profile.setHttpCacheType(
            self.QWEBENGINE_CACHE_TYPES.get(
                SettingsManager.get("performance/cache_type", "DiskHttpCache")
            )
        )

        # Registra o profile no sistema de crash dump
        crash_handler.register_profile(self.profile)

    def configure_spellcheck(self):

        # Configura corretor ortográfico
        if self.user.enable:

            self.profile.setSpellCheckEnabled(
                SettingsManager.get("system/spellCheckers", True)
            )

            self.profile.setSpellCheckLanguages(
                [
                    SettingsManager.get(
                        "system/spellCheckLanguage",
                        DictionariesManager.get_current_dict()
                    )
                ]
            )

    def _setup_page(self):

        # Cria a página do WhatsApp controlada por PageController
        self.whatsapp_page = PageController(self.profile, self)

        self.whatsapp_page.user_id = self.user.id

        # Associa página ao WebView
        self.setPage(self.whatsapp_page)

        # Carrega WhatsApp Web
        self.load(QUrl(__whatsapp_url__))

        # Aplica zoom salvo
        self.setZoomFactor(self.user.zoomFactor)

    def contextMenuEvent(self, event):

        # Cria menu padrão
        menu = self.createStandardContextMenu()

        actions_to_remove = [
            'Back', 'View page source', 'Save page', 'Forward',
            'Open link in new tab', 'Save link', 'Open link in new window',
            'Paste and match style', 'Reload', 'Copy image address'
        ]

        menu = self._remove_actions(menu, actions_to_remove)

        translations = {
            'Undo': _('Undo'), 'Redo': _('Redo'), 'Cut': _('Cut'),
            'Copy': _('Copy'), 'Paste': _('Paste'), 'Select all': _('Select all'),
            'Save image': _('Save image'), 'Copy image': _('Copy image'),
            'Copy link address': _('Copy link address')
        }

        self._translate_actions(menu, translations)

        self._set_copy_link_behavior(menu)

        self._add_spellcheck_actions(menu)

        menu.exec(event.globalPos())

    def _remove_actions(self, menu, actions_to_remove):

        for action in menu.actions():
            if action.text() in actions_to_remove:
                menu.removeAction(action)

        return menu

    def _translate_actions(self, menu, translations):

        for action in menu.actions():
            if action.text() in translations:
                action.setText(translations[action.text()])

    def _set_copy_link_behavior(self, menu):

        for action in menu.actions():

            if action.text() == _("Copy link address"):

                try:
                    action.triggered.disconnect()
                except TypeError:
                    pass

                def setClipboard():

                    cb = QApplication.clipboard()

                    cb.clear(mode=cb.Mode.Clipboard)

                    cb.setText(
                        self.whatsapp_page.link_context,
                        mode=cb.Mode.Clipboard
                    )

                action.triggered.connect(setClipboard)

    def _add_spellcheck_actions(self, menu):

        profile = self.page().profile()

        languages = profile.spellCheckLanguages()

        spellcheck_action = QAction(_("Check Spelling"), self)

        spellcheck_action.setCheckable(True)

        spellcheck_action.setChecked(profile.isSpellCheckEnabled())

        spellcheck_action.toggled.connect(self._toggle_spellcheck)

        menu.addAction(spellcheck_action)

        if profile.isSpellCheckEnabled():

            sub_menu = menu.addMenu(_("Select Language"))

            for lang_name in DictionariesManager.list():

                action = sub_menu.addAction(lang_name)

                action.setCheckable(True)

                action.setChecked(lang_name in languages)

                action.triggered.connect(
                    lambda _, lang=lang_name: self._select_language(lang)
                )

    def _toggle_spellcheck(self, toggled):

        print("Correção ortográfica:", toggled)

        SettingsManager.set("system/spellCheckers", toggled)

        QApplication.instance().getWindow().browser.update_spellcheck()

    def _select_language(self, lang):

        print("Linguagem selecionada via menu de contexto:", lang)

        DictionariesManager.set_lang(lang)

        QApplication.instance().getWindow().browser.update_spellcheck()

    def _on_title_changed(self, title):

        # Extrai número de notificações do título
        num = ''.join(filter(str.isdigit, title))

        qtd = int(num) if num else 0

        self.update_button_signal.emit(self.page_index, qtd)

    def _on_load_finished(self, success):

        if not success:

            print("You are not connected to the Internet.")

            self.timer = QTimer(self)

            self.timer.timeout.connect(self.load_page)

            self.timer.setSingleShot(True)

            self.timer.start(5000)

    def set_zoom_factor_page(self, factor=None):

        new_zoom = 1.0 if factor is None else self.zoomFactor() + factor

        self.setZoomFactor(new_zoom)

    def load_page(self):

        if self.user.enable:

            self.setPage(self.whatsapp_page)

            self.load(QUrl(__whatsapp_url__))

            self.setZoomFactor(self.user.zoomFactor)

    def apply_custom_css(self):

        if self.user.enable and self.whatsapp_page:

            self.whatsapp_page.apply_custom_css()

    def close_conversation(self):

        if self.user.enable:

            self.whatsapp_page.close_conversation()

    def set_theme_light(self):

        if self.user.enable:

            self.whatsapp_page.set_theme_light()

    def set_theme_dark(self):

        if self.user.enable:

            self.whatsapp_page.set_theme_dark()

    def remove_files(self):

        try:

            if not self.user.enable:
                self.profile = QWebEngineProfile(str(self.user.id), self)

            cache_path = self.profile.cachePath()

            storage_path = self.profile.persistentStoragePath()

            shutil.rmtree(cache_path, ignore_errors=True)

            shutil.rmtree(storage_path, ignore_errors=True)

            self.stop()

            self.close()

            return True

        except Exception:

            return False

    def enable_page(self):

        self._initialize()

        self.setVisible(True)

    def disable_page(self):

        if self.profile:

            crash_handler.unregister_profile(self.profile)

            self.profile.clearHttpCache()

        self.setPage(None)

        self.setVisible(False)

    def open_devtools(self):

        current_page = self.page()

        if not self.user.enable or not current_page:
            return

        if self._devtools_view is None:

            self._devtools_view = QWebEngineView()

            account_name = self.user.name if self.user.name else _("Account")

            self._devtools_view.setWindowTitle(
                _("DevTools - {}").format(account_name)
            )

            self._devtools_view.resize(1100, 700)

        if self._devtools_page is None:

            self._devtools_page = QWebEnginePage(
                self.profile,
                self._devtools_view
            )

        current_page.setDevToolsPage(self._devtools_page)

        self._devtools_view.setPage(self._devtools_page)

        self._devtools_view.show()

        self._devtools_view.raise_()

        self._devtools_view.activateWindow()