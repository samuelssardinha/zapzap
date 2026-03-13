# Classe que controla páginas do Chromium dentro do Qt
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings

# Manipulação de URLs
from PyQt6.QtCore import QUrl

# Permite abrir links no navegador padrão do sistema
from PyQt6.QtGui import QDesktopServices

# URL principal do WhatsApp Web
from zapzap import __whatsapp_url__

# Gerenciador de addons (extensões customizadas)
from zapzap.services.AddonsManager import AddonsManager

# Gerenciador de customizações CSS e JS
from zapzap.services.CustomizationsManager import CustomizationsManager

# Gerenciador de temas
from zapzap.services.ThemeManager import ThemeManager

# Biblioteca para manipular URLs
import urllib.parse

# Sistema de tradução
from gettext import gettext as _


class PageController(QWebEnginePage):
    """
    Classe responsável por controlar o comportamento da página do WhatsApp.

    Ela herda de QWebEnginePage e intercepta:

    - navegação
    - criação de novas janelas
    - permissões
    - injeção de scripts
    - tema
    - notificações
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Último link onde o mouse passou
        self.link_url = ""

        # Último link usado no menu de contexto
        self.link_context = ''

        # ID da conta associada a esta página
        self.user_id = None

        # Quando o mouse passa sobre um link
        self.linkHovered.connect(self._on_link_hovered)

        # Quando a página termina de carregar
        self.loadFinished.connect(self._on_load_finished)

        # Quando o site pede acesso a recursos (notificação, câmera etc.)
        self.featurePermissionRequested.connect(
            self._on_feature_permission_requested
        )

    def createWindow(self, _type):
        """
        Intercepta criação de novas janelas.

        WhatsApp às vezes tenta abrir links em novas abas.
        Aqui interceptamos e abrimos no navegador padrão.
        """

        # Cria uma nova página temporária
        new_page = QWebEnginePage(self.profile(), self)

        # Marca que nenhum link externo foi aberto ainda
        new_page.setProperty("externalUrlOpened", False)

        # Quando a URL mudar, abrimos no navegador
        new_page.urlChanged.connect(self.open_in_browser)

        return new_page

    def open_in_browser(self, url: QUrl):
        """
        Abre links externos no navegador padrão do sistema.

        Evita abrir múltiplas vezes se o link redirecionar.
        """

        page = self.sender()

        # Alguns sites geram múltiplos redirecionamentos
        if isinstance(page, QWebEnginePage):

            if page.property("externalUrlOpened"):
                return

            page.setProperty("externalUrlOpened", True)

        if not url.isValid() or url.isEmpty():
            return

        normalized_url = self.normalize_url(url.toString())

        QDesktopServices.openUrl(QUrl(normalized_url))

    def normalize_url(self, url: str) -> str:
        """
        Remove parâmetros redundantes da URL.
        """

        parsed_url = urllib.parse.urlparse(url)

        normalized_query = urllib.parse.unquote(parsed_url.query)

        return urllib.parse.urlunparse(
            parsed_url._replace(query=normalized_query)
        )

    def acceptNavigationRequest(self, url, type, isMainFrame):
        """
        Impede navegar para fora do WhatsApp.

        Isso garante que o ZapZap funcione apenas com:
        https://web.whatsapp.com/
        """

        if url != QUrl(__whatsapp_url__):
            return False

        return super().acceptNavigationRequest(url, type, isMainFrame)

    def close_conversation(self):
        """
        Fecha conversa simulando tecla ESC.
        """

        script = """
        document.dispatchEvent(
            new KeyboardEvent("keydown", {'key': 'Escape'})
        );
        """

        self.runJavaScript(script)

    def set_theme_light(self):
        """
        Define tema claro.
        """

        self.profile().settings().setAttribute(
            QWebEngineSettings.WebAttribute.ForceDarkMode,
            False
        )

        self.runJavaScript(
            "document.body.classList.remove('dark');"
        )

    def set_theme_dark(self):
        """
        Define tema escuro.
        """

        self.profile().settings().setAttribute(
            QWebEngineSettings.WebAttribute.ForceDarkMode,
            False
        )

        self.runJavaScript(
            "document.body.classList.add('dark');"
        )

    def new_chat(self):
        """
        Simula atalho Ctrl+Alt+N para novo chat.
        """

        script = """
        var event = new KeyboardEvent('keydown', {
            key: 'n',
            code: 'KeyN',
            ctrlKey: true,
            altKey: true,
            bubbles: true,
            cancelable: true
        });

        document.dispatchEvent(event);
        """

        self.runJavaScript(script)

    def open_chat_by_number(self):
        """
        Abre conversa a partir de um número digitado.
        """

        prompt_text = _(
            "Please enter the phone number with country code (e.g., +5511999999999):"
        )

        prompt_error = _(
            "Invalid number! Please enter at least 9 digits, including the country code."
        )

        script = f"""
        (function() {{

            var number = prompt('{prompt_text}');

            if (number) {{

                number = number.replace(/\\D/g, "");

                if (number.startsWith("00"))
                    number = "+" + number.slice(2);
                else if (!number.startsWith("+"))
                    number = "+" + number;

                number = number.substring(0, 15);

                if (number.length >= 9) {{

                    var a = document.createElement("a");
                    a.href = "https://api.whatsapp.com/send?phone=" + encodeURIComponent(number);

                    document.body.appendChild(a);
                    a.click();
                    a.remove();

                }} else {{

                    alert('{prompt_error}');

                }}
            }}

        }})();
        """

        self.runJavaScript(script)

    def xdg_open_chat(self, url):
        """
        Abre chat via URL externa.
        """

        script = """(function(){var a = document.createElement("a");a.href=\"""" + \
            url + \
            """\";document.body.appendChild(a);a.click();a.remove(); return;})();"""

        self.runJavaScript(script)

    def _on_link_hovered(self, url):
        """
        Guarda o link quando o mouse passa por ele.
        """

        self.link_url = url

        if self.link_url != "":
            self.link_context = url

    def _on_feature_permission_requested(self, frame, feature):
        """
        Concede automaticamente permissões pedidas pelo site.

        Exemplo:
        - notificações
        - câmera
        - microfone
        """

        self.setFeaturePermission(
            frame,
            feature,
            QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
        )

    def _on_load_finished(self, success):
        """
        Executa ações após carregar o WhatsApp.
        """

        if success:

            # Injeta addons
            AddonsManager.inject_addons(self)

            # Aplica customizações
            self.apply_customizations()

            # Permite notificações
            self.setFeaturePermission(
                self.url(),
                QWebEnginePage.Feature.Notifications,
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )

            # Sincroniza tema
            ThemeManager.sync()

    def apply_customizations(self):

        self.apply_custom_css()
        self.apply_custom_js()

    def apply_custom_css(self):

        css_entries = CustomizationsManager.build_effective_ordered_assets(
            CustomizationsManager.TYPE_CSS,
            self.user_id,
        )

        self.runJavaScript(
            CustomizationsManager.css_injection_script(css_entries)
        )

    def apply_custom_js(self):

        js_entries = CustomizationsManager.build_effective_ordered_assets(
            CustomizationsManager.TYPE_JS,
            self.user_id,
        )

        self.runJavaScript(
            CustomizationsManager.js_injection_script(js_entries)
        )

    def show_toast(self, message, duration=1000):
        """
        Mostra uma notificação temporária dentro da página.
        """

        script = f"""
        (function() {{

            var toast = document.createElement('div');

            toast.style.position = 'fixed';
            toast.style.bottom = '20px';
            toast.style.left = '50%';
            toast.style.transform = 'translateX(-50%)';

            toast.style.padding = '10px 20px';
            toast.style.backgroundColor = '#333';
            toast.style.color = '#fff';
            toast.style.borderRadius = '5px';

            toast.style.fontSize = '14px';
            toast.style.zIndex = '9999';

            toast.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';

            toast.innerText = '{message}';

            document.body.appendChild(toast);

            setTimeout(function() {{
                toast.remove();
            }}, {duration});

        }})();
        """

        self.runJavaScript(script)

    def javaScriptConsoleMessage(self, level, message, line, sourceID):
        """
        Ignora mensagens do console JS.
        """
        pass