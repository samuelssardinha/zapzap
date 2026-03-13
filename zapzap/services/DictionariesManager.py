import os
import struct
from PyQt6.QtCore import QLocale

from zapzap.services.EnvironmentManager import EnvironmentManager
from zapzap.services.PathManager import PathManager
from zapzap.services.SettingsManager import SettingsManager


class DictionariesManager:

    # assinatura usada pelo formato BDICT do Chromium
    BDIC_MAGIC = b"BDIC"

    @staticmethod
    def get_path() -> str:

        return PathManager.get_paths(
            EnvironmentManager.identify_packaging()
        )['path']

    @staticmethod
    def _is_valid_bdic(path: str) -> bool:
        """
        Verifica se um arquivo .bdic parece válido.

        Critérios:
        - arquivo existe
        - tamanho plausível (>50 KB)
        - contém dados binários (não texto)
        """

        try:
            if not os.path.exists(path):
                return False

            size = os.path.getsize(path)

            # dicionários reais têm geralmente alguns MB
            if size < 50_000:
                return False

            # lê primeiros bytes
            with open(path, "rb") as f:
                header = f.read(32)

            # evita arquivos texto ou vazios
            if header.strip() == b"":
                return False

            # verifica se não é texto ASCII simples
            if all(32 <= b <= 126 for b in header):
                return False

            return True

        except Exception:
            return False

    @staticmethod
    def list() -> list:
        """
        Retorna lista de idiomas com dicionários válidos.
        """

        dictionaries_path = DictionariesManager.get_path()

        if not dictionaries_path or not os.path.isdir(dictionaries_path):
            return []

        languages = []

        for file in os.listdir(dictionaries_path):

            if not file.endswith(".bdic"):
                continue

            full_path = os.path.join(dictionaries_path, file)

            if DictionariesManager._is_valid_bdic(full_path):

                languages.append(file.replace(".bdic", ""))

        return languages

    @staticmethod
    def set_lang(lang: str):

        SettingsManager.set("system/spellCheckLanguage", lang)

    @staticmethod
    def set_spell_folder(path: str) -> str:

        PathManager.set_custom_path(
            EnvironmentManager.identify_packaging(),
            path
        )

    @staticmethod
    def get_current_dict() -> str:
        """
        Retorna idioma configurado.

        Se idioma salvo for inválido,
        faz fallback automático.
        """

        lang = SettingsManager.get(
            "system/spellCheckLanguage",
            DictionariesManager.get_system_language()
        )

        available = DictionariesManager.list()

        if lang not in available and available:
            lang = available[0]

        return lang

    @staticmethod
    def get_system_language() -> str:

        return QLocale.system().name()

    @staticmethod
    def restore_default_path() -> str:

        PathManager.restore_default_path(
            EnvironmentManager.identify_packaging()
        )

        return DictionariesManager.get_path()