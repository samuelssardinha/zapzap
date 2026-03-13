from pathlib import Path
from gettext import gettext as _
import logging
import sys

from PyQt6.QtWebEngineCore import QWebEngineNotification

from zapzap.webengine import WebView
from zapzap.services.SettingsManager import SettingsManager
from zapzap import __appname__

from zapzap.notifications.PortalNotificationBackend import (
    PortalNotificationBackend
)
from zapzap.notifications.FreedesktopNotificationBackend import (
    FreedesktopNotificationBackend
)
from zapzap.notifications.MacOSNotificationBackend import (
    MacOSNotificationBackend
)

logger = logging.getLogger(__name__)


def is_flatpak() -> bool:
    return Path("/.flatpak-info").exists()


class NotificationService:
    """
    Serviço central de notificações.

    Seleciona automaticamente o backend apropriado
    dependendo do ambiente de execução.

    Backends suportados:

        macOS   -> MacOSNotificationBackend
        Flatpak -> PortalNotificationBackend
        Linux   -> FreedesktopNotificationBackend
        outros  -> None (desativado)
    """

    _backend = None

    def __init__(self):

        if NotificationService._backend is None:
            NotificationService._backend = self._select_backend()

        self.backend = NotificationService._backend

    # ------------------------------------------------------------------
    # Backend selection
    # ------------------------------------------------------------------

    def _select_backend(self):

        try:

            # ---------------------------------------------------------
            # macOS
            # ---------------------------------------------------------
            if sys.platform == "darwin":
                backend = MacOSNotificationBackend()
                if backend.available():
                    return backend

            # ---------------------------------------------------------
            # Flatpak / Portal
            # ---------------------------------------------------------
            if is_flatpak():
                backend = PortalNotificationBackend()
                return backend

            # ---------------------------------------------------------
            # Linux Freedesktop
            # ---------------------------------------------------------
            backend = FreedesktopNotificationBackend()

            if backend.available():
                return backend

        except Exception:
            logger.warning(
                "Notification backend selection failed",
                exc_info=True
            )

        # ---------------------------------------------------------
        # Fallback
        # ---------------------------------------------------------
        logger.info("No notification backend available")

        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def notify(
        self,
        page: WebView,
        notification: QWebEngineNotification
    ):

        # =================================================
        # 1. Regras globais
        # =================================================

        if not SettingsManager.get("notification/app", True):
            return

        if not SettingsManager.get(
            f"{page.user.id}/notification", True
        ):
            return

        if not self.backend:
            return

        # =================================================
        # 2. Conteúdo da notificação
        # =================================================

        try:

            title = (
                notification.title()
                if SettingsManager.get("notification/show_name", True)
                else __appname__
            )

            message = (
                notification.message()
                if SettingsManager.get("notification/show_msg", True)
                else _("New message...")
            )

        except Exception:

            logger.warning(
                "Failed to build notification message",
                exc_info=True
            )

            return

        # =================================================
        # 3. Delegação ao backend
        # =================================================

        try:

            self.backend.notify(
                page=page,
                notification=notification,
                title=title,
                message=message,
            )

        except Exception:

            # Notificações nunca devem derrubar o app
            logger.warning(
                "Notification backend failed; dropping notification",
                exc_info=True,
            )