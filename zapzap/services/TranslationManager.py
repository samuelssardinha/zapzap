import gettext
import os
import locale

from zapzap import APP_PATH, __appname__


class TranslationManager:

    _domain = "zapzap"
    _locale_dir = os.path.join(APP_PATH, "po")

    @staticmethod
    def apply():

        # força locale português
        try:
            locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        except:
            pass

        gettext.bindtextdomain(
            __appname__.lower(),
            TranslationManager._locale_dir
        )

        gettext.textdomain(__appname__.lower())

        translation = gettext.translation(
            __appname__.lower(),
            TranslationManager._locale_dir,
            languages=["pt_BR"],
            fallback=True
        )

        translation.install()