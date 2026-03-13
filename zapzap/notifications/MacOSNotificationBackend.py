from __future__ import annotations

import tempfile
from pathlib import Path
import logging

from PyQt6.QtWidgets import QApplication

from zapzap.webengine import WebView
from zapzap.resources.TrayIcon import TrayIcon
from zapzap.notifications.FreedesktopNotificationBackend import IconRenderer

logger = logging.getLogger(__name__)

try:
    from pync import Notifier
except Exception:
    Notifier = None


class MacOSNotificationBackend:
    """
    Backend de notificações para macOS.

    Usa Notification Center através da biblioteca pync
    (wrapper do terminal-notifier).
    """

    def __init__(self):
        self._last_key = None

    # -------------------------------------------------
    # Availability
    # -------------------------------------------------

    def available(self) -> bool:
        return Notifier is not None

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def notify(
        self,
        page: WebView,
        notification,
        title: str,
        message: str,
    ):

        if not self.available():
            return

        # -------------------------------------------------
        # Evita notificações duplicadas
        # -------------------------------------------------

        key = f"{title}:{message}"

        if key == self._last_key:
            return

        self._last_key = key

        # -------------------------------------------------
        # Ícone (foto do contato se disponível)
        # -------------------------------------------------

        icon_path = ""

        try:
            icon_path = IconRenderer.from_notification_icon(
                notification.icon(),
                title
            )
        except Exception:
            icon_path = ""

        if not icon_path:
            icon_path = self._default_icon()

        # -------------------------------------------------
        # Callback ao clicar na notificação
        # -------------------------------------------------

        def on_click():

            try:

                app = QApplication.instance()

                if not app:
                    return

                main = app.getWindow()

                if not main:
                    return

                main.show()
                main.raise_()
                main.activateWindow()

                main.browser.switch_to_page(
                    page,
                    main.browser.page_buttons[page.page_index],
                )

                try:
                    notification.click()
                except Exception:
                    pass

            except Exception:
                logger.warning(
                    "Failed to process notification click",
                    exc_info=True
                )

        # -------------------------------------------------
        # Envia notificação
        # -------------------------------------------------

        try:

            Notifier.notify(
                message,
                title=title,
                appName="ZapZap",
                appIcon=icon_path,
                execute="",  # necessário para compatibilidade
            )

        except Exception:
            logger.warning(
                "macOS notification failed",
                exc_info=True
            )

        # -------------------------------------------------
        # Mantém compatibilidade com QWebEngineNotification
        # -------------------------------------------------

        try:
            notification.closed.connect(lambda: None)
        except Exception:
            pass

    # -------------------------------------------------
    # Default icon fallback
    # -------------------------------------------------

    def _default_icon(self) -> str:

        try:

            icon = TrayIcon.getIcon()
            pixmap = icon.pixmap(128, 128)

            tmp = Path(tempfile.gettempdir()) / "zapzap_notify.png"

            pixmap.save(str(tmp))

            return str(tmp)

        except Exception:
            return ""