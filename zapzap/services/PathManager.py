from zapzap.services.EnvironmentManager import Packaging
from zapzap.services.SettingsManager import SettingsManager
import os
import sys


# ----------------------------------------------------------
# Caminho padrão dos dicionários
# ----------------------------------------------------------

if sys.platform == "darwin":

    # app empacotado
    if getattr(sys, "frozen", False):

        DEFAULT_DICT_PATH = os.path.abspath(
            os.path.join(
                os.path.dirname(sys.executable),
                "..",
                "Resources",
                "zapzap",
                "dictionaries"
            )
        )

    # modo desenvolvimento
    else:

        DEFAULT_DICT_PATH = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "dictionaries"
            )
        )

else:

    DEFAULT_DICT_PATH = "/usr/share/qt6/qtwebengine_dictionaries"


DEFAULT_PATHS = {
    "Official": DEFAULT_DICT_PATH,
    "Unofficial": DEFAULT_DICT_PATH,
}


# ----------------------------------------------------------
# PathManager
# ----------------------------------------------------------

class PathManager:

    paths = {

        Packaging.APPIMAGE: {
            "path": "",
            "default": os.path.join(
                os.getenv("APPDIR", "/"),
                "qtwebengine_dictionaries"
            ),
        },

        Packaging.FLATPAK: {
            "path": "",
            "default": os.getenv(
                "QTWEBENGINE_DICTIONARIES_PATH",
                ""
            ),
        },

        Packaging.RPM: {
            "path": "",
            "default": "/usr/share/qt6/qtwebengine_dictionaries",
        },

        Packaging.UNOFFICIAL: {
            "path": "",
            "default": DEFAULT_DICT_PATH,
        }

    }

    # ------------------------------------------------------

    @staticmethod
    def get_paths(packaging_type):

        paths = PathManager.paths.get(packaging_type)

        if not paths:
            return None

        # copia segura
        result = dict(paths)

        custom_path = SettingsManager.get(
            f"spellcheck/folder_{packaging_type.value}",
            result["default"]
        )

        if custom_path:
            result["path"] = custom_path

        return result

    # ------------------------------------------------------

    @staticmethod
    def show_paths(packaging_type):

        paths = PathManager.get_paths(packaging_type)

        if not paths:

            print("Tipo de empacotamento não encontrado.")
            return

        print(f"Caminho: {paths['path']}")
        print(f"Caminho padrão: {paths['default']}")

    # ------------------------------------------------------

    @staticmethod
    def set_custom_path(packaging_type, new_path):

        SettingsManager.set(
            f"spellcheck/folder_{packaging_type.value}",
            new_path
        )

        print(
            f"Caminho customizado para {packaging_type.value} alterado para: {new_path}"
        )

    # ------------------------------------------------------

    @staticmethod
    def restore_default_path(packaging_type):

        SettingsManager.remove(
            f"spellcheck/folder_{packaging_type.value}"
        )

        print(
            f"Caminho customizado para {packaging_type.value} restaurado para o padrão."
        )