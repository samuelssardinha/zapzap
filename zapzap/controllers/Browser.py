# Importa classes do Qt responsáveis por animações e manipulação de URLs
from PyQt6.QtCore import QEasingCurve, QParallelAnimationGroup, QPropertyAnimation, QUrl

# Widgets base utilizados na interface
from PyQt6.QtWidgets import QWidget, QPushButton, QMessageBox, QApplication

# Classes de ação de menu e abertura de URLs externas
from PyQt6.QtGui import QAction, QDesktopServices

# Botão que representa uma conta/aba do WhatsApp
from zapzap.controllers.PageButton import PageButton

# Componente que contém o navegador Chromium embutido
from zapzap.webengine.WebView import WebView

# Modelo de dados do usuário/conta
from zapzap.models.User import User

# Sistema de ícones do aplicativo
from zapzap.resources.SystemIcon import SystemIcon
from zapzap.resources.UserIcon import UserIcon

# Serviços auxiliares
from zapzap.services.AlertManager import AlertManager
from zapzap.services.SettingsManager import SettingsManager
from zapzap.services.SetupManager import SetupManager
from zapzap.services.SysTrayManager import SysTrayManager

# Interface gerada pelo Qt Designer
from zapzap.views.ui_browser import Ui_Browser

# Sistema de tradução
from gettext import gettext as _


class Browser(QWidget, Ui_Browser):
    """
    Classe responsável por controlar o navegador interno do ZapZap.

    Ela gerencia:
    - criação de contas
    - páginas WebView
    - botões de conta
    - notificações
    - troca de páginas
    - animação da sidebar
    """

    def __init__(self, parent=None):
        # Inicializa QWidget
        super().__init__(parent)

        # Carrega interface criada no Qt Designer
        self.setupUi(self)

        # Guarda referência da janela principal
        self.parent = parent

        # Contador de páginas WebView
        self.page_count = 0

        # Dicionário que liga index → botão da página
        self.page_buttons = {}

        # Largura expandida da barra lateral
        self._sidebar_expanded_width = max(50, self.browser_sidebar.maximumWidth())

        # Grupo de animação da sidebar
        self._sidebar_animation_group = None

        # Inicializa estrutura do navegador
        self._initialize()

    def __del__(self):
        """
        Destrutor da classe.
        Garante que todas as páginas WebView sejam fechadas.
        """
        self.close_pages()

    # ================================
    # Inicialização
    # ================================
    def _initialize(self):
        """
        Executa todas as etapas necessárias
        para inicializar o navegador.
        """

        # Mostra ajuda do Flatpak caso esteja rodando nesse ambiente
        self._configure_flatpak_guidance()

        # Conecta eventos da interface
        self._configure_signals()

        # Carrega usuários salvos
        self._load_users()

        # Seleciona a página padrão
        self._select_default_page()

        # Atualiza menu de usuários
        self._update_user_menu()

        # Configura visibilidade da sidebar
        self.settings_sidebar()

    def _configure_signals(self):
        """
        Conecta eventos dos botões da interface
        com as funções correspondentes.
        """

        # Criar nova conta
        self.btn_new_account.clicked.connect(lambda: self.add_new_user())

        # Abrir chat digitando número
        self.btn_new_chat_number.clicked.connect(
            lambda: self.parent.new_chat_by_phone())

        # Novo chat
        self.btn_new_chat.clicked.connect(lambda: self.parent.new_chat())

        # Abrir configurações
        self.btn_open_settings.clicked.connect(
            lambda: self.parent.open_settings())

    def _configure_flatpak_guidance(self):
        """
        Caso o aplicativo esteja rodando dentro de Flatpak,
        adiciona botão de ajuda para permissões sandbox.
        """

        if not SetupManager._is_flatpak:
            return

        # Cria botão de ajuda
        self.btn_flatpak_help = QPushButton(self.settings_buttons_layout)
        self.btn_flatpak_help.setMinimumSize(35, 35)
        self.btn_flatpak_help.setText("")
        self.btn_flatpak_help.setIconSize(self.btn_open_settings.iconSize())
        self.btn_flatpak_help.setToolTip(_("Flatpak sandbox help"))

        # Evento do botão
        self.btn_flatpak_help.clicked.connect(self._show_flatpak_sandbox_popover)

        # Insere botão no layout
        self.layout_2.insertWidget(4, self.btn_flatpak_help)

    def _show_flatpak_sandbox_popover(self):
        """
        Mostra instruções para liberar permissões no Flatpak.
        """

        command = "flatpak override --user --filesystem=home com.rtosta.zapzap"

        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setWindowTitle(_("Flatpak sandbox"))
        dialog.setText(_("ZapZap is running in Flatpak sandbox."))

        dialog.setInformativeText(
            _(
                "Some features like opening files or drag-and-drop may require additional permissions."
            )
        )

        instructions_button = dialog.addButton(_("Instructions"), QMessageBox.ButtonRole.ActionRole)
        copy_button = dialog.addButton(_("Copy command"), QMessageBox.ButtonRole.ActionRole)
        dialog.addButton(_("Close"), QMessageBox.ButtonRole.RejectRole)

        dialog.exec()

        # Ação do botão selecionado
        if dialog.clickedButton() == instructions_button:
            QDesktopServices.openUrl(QUrl("https://flathub.org/apps/com.github.tchx84.Flatseal"))

        elif dialog.clickedButton() == copy_button:
            QApplication.clipboard().setText(command)

    def _load_users(self):
        """
        Carrega usuários salvos no banco de dados
        e cria uma página WebView para cada um.
        """

        # Se não existir usuário cria o primeiro
        self._create_user_in_first_access()

        # Busca todos usuários
        self.user_list = User.select()

        # Cria páginas para cada usuário
        for user in self.user_list:
            self._add_page(user)

    def _create_user_in_first_access(self):
        """
        Caso seja o primeiro uso do aplicativo,
        cria automaticamente um usuário.
        """

        if User.count_users() == 0:
            User.create_new_user(icon=UserIcon.ICON_DEFAULT)

    def _select_default_page(self):
        """
        Seleciona a primeira página habilitada.
        """

        button, page = self._find_button_and_page_enabled()

        if button and page:
            self.switch_to_page(page, button)

    def add_new_user(self, new_user=None):
        """
        Cria nova conta de WhatsApp no aplicativo.
        """

        if not new_user:
            new_user = User.create_new_user()

        if new_user:
            self._add_page(new_user)
            self._update_user_menu()
        else:
            AlertManager.limit_users(self)

    # ================================
    # Gerenciamento de páginas
    # ================================
    def _add_page(self, user: User):
        """
        Cria nova página WebView e botão lateral.
        """

        # Incrementa contador
        self.page_count += 1
        page_index = self.page_count

        # Cria navegador da conta
        new_page = WebView(user, page_index)

        # Conecta notificações
        new_page.update_button_signal.connect(
            self.update_page_button_number_notifications
        )

        # Adiciona página no stacked widget
        self.pages.addWidget(new_page)

        # Cria botão da página
        page_button = PageButton(user, page_index)

        # Evento de troca de página
        page_button.clicked.connect(
            lambda: self.switch_to_page(new_page, page_button))

        page_button.setObjectName(f"page_button_{page_index}")

        # Adiciona botão no layout lateral
        self.page_buttons_layout.addWidget(page_button)

        # Guarda referência
        self.page_buttons[page_index] = page_button

    # ================================
    # (demais métodos mantidos iguais)
    # ================================

    def disable_page(self, user: User):
        button, page = self._find_button_and_page_by_user(user)

        if button and page:
            if user.enable:
                button.show()
                page.enable_page()
            else:
                button.hide()
                page.disable_page()

        self._select_default_page()
        self._update_user_menu()

    def delete_page(self, user: User):
        button, page = self._find_button_and_page_by_user(user)

        if button and page:
            button.close()
            del self.page_buttons[button.page_index]
            page.remove_files()

        self._select_default_page()
        self._update_user_menu()

    def update_icons_page_button(self, user: User):
        button, page = self._find_button_and_page_by_user(user)

        if button and page:
            button.user = user
            page.user = user

        self._update_user_menu()

    def _update_user_menu(self):
        self.parent.menuUsers.clear()

        new_action = QAction(_("New account"), self)
        new_action.triggered.connect(lambda: self.add_new_user())
        new_action.setShortcut("Ctrl+U")

        self.parent.menuUsers.addAction(new_action)
        self.parent.menuUsers.addSeparator()

        for count, button in enumerate(self.page_buttons.values(), start=1):
            if button.user.enable:

                new_action = QAction(
                    button.user.name if button.user.name != "" else _("Account {}").format(count), self)

                new_action.setShortcut(f'Ctrl+{count}')
                new_action.triggered.connect(button.clicked)

                self.parent.menuUsers.addAction(new_action)

    def _find_button_and_page_by_user(self, user: User):
        for button in self.page_buttons.values():
            if button.user.id == user.id:
                page = self.pages.widget(button.page_index - 1)
                return button, page
        return None, None

    def _find_button_and_page_enabled(self):
        for button in self.page_buttons.values():
            if button.user.enable:
                page = self.pages.widget(button.page_index - 1)
                return button, page
        return None, None

    def switch_to_page(self, page: WebView, button: PageButton):
        self._reset_button_styles()
        self.pages.setCurrentWidget(page)

        page.page().show_toast(
            page.user.name if page.user.name != "" else _("Account {}").format(page.page_index)
        )

        button.selected()

    def close_pages(self):
        for i in range(self.pages.count()):
            page = self.pages.widget(i)
            if page:
                page.__del__()

    def reload_pages(self):
        for i in range(self.pages.count()):
            page = self.pages.widget(i)
            page.load_page()

    def close_conversations(self):
        for i in range(self.pages.count()):
            page = self.pages.widget(i)
            page.close_conversation()

    def apply_custom_css_all_pages(self):
        for i in range(self.pages.count()):
            page = self.pages.widget(i)
            page.apply_custom_css()

    def current_webview(self):
        return self.pages.currentWidget()

    def update_spellcheck(self):
        for i in range(self.pages.count()):
            page = self.pages.widget(i)
            page.configure_spellcheck()

    def update_page_button_number_notifications(self, page_index, number_notifications):

        if page_index in self.page_buttons:
            self.page_buttons[page_index].update_notifications(
                number_notifications
            )

            self._update_total_notifications()

    def _update_total_notifications(self):

        total_notifications = sum(
            button.number_notifications for button in self.page_buttons.values()
        )

        SysTrayManager.set_number_notifications(total_notifications)

    def _reset_button_styles(self):
        for button in self.page_buttons.values():
            button.unselected()

    def set_theme_light(self):

        for i in range(self.pages.count()):
            page = self.pages.widget(i)
            page.set_theme_light()

        self.__set_button_icons(SystemIcon.Type.Light)

    def set_theme_dark(self):

        for i in range(self.pages.count()):
            page = self.pages.widget(i)
            page.set_theme_dark()

        self.__set_button_icons(SystemIcon.Type.Dark)

    def __set_button_icons(self, theme):

        self.btn_new_account.setIcon(SystemIcon.get_icon("new_account", theme))
        self.btn_open_settings.setIcon(
            SystemIcon.get_icon("open_settings", theme))

        self.btn_new_chat.setIcon(SystemIcon.get_icon("new_chat", theme))
        self.btn_new_chat_number.setIcon(
            SystemIcon.get_icon("new_chat_number", theme))

        if hasattr(self, "btn_flatpak_help"):
            self.btn_flatpak_help.setIcon(SystemIcon.get_icon("flatpak_help", theme))

    def settings_sidebar(self):
        self.set_sidebar_visible(SettingsManager.get("system/sidebar", True), animated=False)

    def set_sidebar_visible(self, visible: bool, animated: bool = True):

        if self._sidebar_animation_group:
            self._sidebar_animation_group.stop()
            self._sidebar_animation_group = None

        current_width = self.browser_sidebar.maximumWidth()
        is_expanded = current_width > 0
        is_visible = self.browser_sidebar.isVisible()

        if visible == is_expanded and visible == is_visible:
            return

        target_width = self._sidebar_expanded_width if visible else 0

        if not animated:

            if visible:
                self.browser_sidebar.show()

            self.browser_sidebar.setMinimumWidth(target_width)
            self.browser_sidebar.setMaximumWidth(target_width)

            if not visible:
                self.browser_sidebar.hide()

            return

        if visible:
            self.browser_sidebar.show()

        self._animate_sidebar_width(
            current_width,
            target_width,
            on_finished=(lambda: self.browser_sidebar.hide()) if not visible else None,
        )

    def _animate_sidebar_width(self, start_width: int, end_width: int, on_finished=None):

        min_animation = QPropertyAnimation(self.browser_sidebar, b"minimumWidth", self)
        min_animation.setDuration(180)
        min_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        min_animation.setStartValue(start_width)
        min_animation.setEndValue(end_width)

        max_animation = QPropertyAnimation(self.browser_sidebar, b"maximumWidth", self)
        max_animation.setDuration(180)
        max_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        max_animation.setStartValue(start_width)
        max_animation.setEndValue(end_width)

        group = QParallelAnimationGroup(self)

        group.addAnimation(min_animation)
        group.addAnimation(max_animation)

        def _on_finished():
            self._sidebar_animation_group = None
            if on_finished:
                on_finished()

        group.finished.connect(_on_finished)

        self._sidebar_animation_group = group
        group.start()