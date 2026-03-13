# Acesso às variáveis de ambiente do sistema
from os import environ, getenv

# Classe Qt usada para obter informações sobre arquivos
from PyQt6.QtCore import QFileInfo

# Gerenciador de dicionários de correção ortográfica
from zapzap.services.DictionariesManager import DictionariesManager

# Gerenciador de configurações do aplicativo
from zapzap.services.SettingsManager import SettingsManager


class SetupManager:
    """
    Classe responsável por configurar o ambiente do sistema
    antes da inicialização do Qt e do QtWebEngine.

    Essa classe define variáveis de ambiente críticas
    para o funcionamento do Chromium embutido no QtWebEngine.
    """

    # Detecta se o app está rodando dentro do sandbox Flatpak
    _is_flatpak = QFileInfo(__file__).absolutePath().startswith('/app/')

    # Plataforma gráfica padrão
    # (nome histórico herdado do Linux)
    _qt_platform_xcb = "cocoa"


    @staticmethod
    def apply():
        """
        Aplica configurações de ambiente antes da inicialização do Qt.

        Muito importante:
        Essas variáveis devem ser definidas antes de criar QApplication.
        """

        # --------------------------------------------------
        # Plataforma gráfica
        # --------------------------------------------------

        # Se não estiver rodando dentro do Flatpak
        if not SetupManager._is_flatpak:

            # Descobre qual backend gráfico usar
            platform = SetupManager.get_qt_platform()

            if platform:
                environ["QT_QPA_PLATFORM"] = platform


        # --------------------------------------------------
        # Escalonamento da interface
        # --------------------------------------------------

        # Obtém escala configurada nas preferências
        scale_factor = int(SettingsManager.get("system/scale", 100)) / 100

        # Define escala manual do Qt
        environ["QT_SCALE_FACTOR"] = f"{scale_factor:.2f}"

        # Permite auto ajuste de escala de tela
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"


        # --------------------------------------------------
        # Caminho dos dicionários de spellcheck
        # --------------------------------------------------

        environ["QTWEBENGINE_DICTIONARIES_PATH"] = DictionariesManager.get_path()


        # --------------------------------------------------
        # Flags do Chromium (Qt WebEngine)
        # --------------------------------------------------

        # Flags já existentes no ambiente
        existing_flags = environ.get("QTWEBENGINE_CHROMIUM_FLAGS", "")

        # Flags definidas nas configurações do ZapZap
        settings_flags = SettingsManager.get("QTWEBENGINE_CHROMIUM_FLAGS", "")

        # Lista final de flags
        flags = []

        def add_flag(flag: str):
            """
            Adiciona flag sem duplicação.
            """
            if flag not in flags:
                flags.append(flag)

        # Flags já definidas no ambiente
        if existing_flags:
            flags.extend(existing_flags.split())

        # Flags definidas nas configurações do usuário
        if settings_flags:
            flags.extend(settings_flags.split())


        # --------------------------------------------------
        # GPU / Renderização
        # --------------------------------------------------

        # Desativa GPU completamente
        if SettingsManager.get("performance/disable_gpu", False):
            add_flag("--disable-gpu")

        # Executa GPU no mesmo processo
        if SettingsManager.get("performance/in_process_gpu", False):
            add_flag("--in-process-gpu")

        # Desativa VSync da GPU
        if SettingsManager.get("performance/disable_gpu_vsync", False):
            add_flag("--disable-gpu-vsync")

        # Força renderização via CPU
        if SettingsManager.get("performance/software_rendering", False):

            environ["QT_OPENGL"] = "software"

            add_flag("--disable-gpu")


        # --------------------------------------------------
        # Processos do Chromium
        # --------------------------------------------------

        # Força modo single process
        if SettingsManager.get("performance/single_process", False):
            add_flag("--single-process")

        # Usa processo por site
        #if SettingsManager.get("performance/process_per_site", True):
        #    add_flag("--process-per-site")


        # --------------------------------------------------
        # Memória JavaScript
        # --------------------------------------------------

        js_mem = SettingsManager.get("performance/js_memory_limit_mb", "0")

        if js_mem and js_mem != "0":
            add_flag(f"--js-flags=--max-old-space-size={js_mem}")


        # --------------------------------------------------
        # Background / timers
        # --------------------------------------------------

        if not SettingsManager.get("web/background_throttling", True):

            add_flag("--disable-background-timer-throttling")

            add_flag("--disable-renderer-backgrounding")


        # --------------------------------------------------
        # Flags obrigatórias
        # --------------------------------------------------

        add_flag("--disable-features=FFmpegAllowLists")


        # --------------------------------------------------
        # Remoção de flags conflitantes
        # --------------------------------------------------

        flags = [f for f in flags if not f.startswith("--ozone-platform")]


        # Define flags finais no ambiente
        environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(flags)


    @staticmethod
    def apply_qt_scale_factor_rounding_policy():
        """
        Define política de arredondamento do Qt para escala.
        Deve ser aplicado após criar QApplication.
        """

        environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "RoundPreferFloor"


    @staticmethod
    def get_argv():
        """
        Mantido apenas por compatibilidade.

        Atualmente o projeto usa variáveis de ambiente
        em vez de argumentos de linha de comando.
        """
        return []


    @staticmethod
    def get_qt_platform():
        """
        Determina qual backend gráfico o Qt deve usar.
        """

        # Se já estiver definido manualmente, não altera
        if "QT_QPA_PLATFORM" in environ:
            return None

        import sys

        # Forçar Wayland manualmente
        if "--wayland" in sys.argv:
            return "wayland"

        # Detecta sessão gráfica no Linux
        XDG_SESSION_TYPE = getenv("XDG_SESSION_TYPE")

        print("XDG_SESSION_TYPE:", XDG_SESSION_TYPE)

        if XDG_SESSION_TYPE == "wayland":

            return "wayland" if SettingsManager.get("system/wayland", False) else "cocoa"

        return SetupManager._qt_platform_xcb