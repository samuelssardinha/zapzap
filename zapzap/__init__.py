from PyQt6.QtCore import QFileInfo

__version__ = '6.3.4.1'
__appname__ = 'ZapZap'

# Descrição do aplicativo
__comment__ = 'WhatsApp Desktop Client for macOS and Windows'

# Identificação do aplicativo
__domain__ = 'com.samuelssardinha'
__desktopid__ = 'com.samuelssardinha.zapzap'
__appid__ = 'zapzap-application'

# Informações do mantenedor do fork
__author__ = 'Samuel Silva Sardinha'
__email__ = 'samuel@qualitiinternet.com.br'

# URLs do projeto
__website__ = 'https://github.com/samuelssardinha/zapzap'
__bugreport__ = 'https://github.com/samuelssardinha/zapzap/issues'
__releases__ = 'https://github.com/samuelssardinha/zapzap/releases'

# Mantemos os links originais de doação do autor original
__paypal__ = 'https://www.paypal.com/donate/?business=E7R4BVR45GRC2&no_recurring=0&item_name=ZapZap+-+Whatsapp+Desktop+for+linux%0AAn+unofficial+WhatsApp+desktop+application+written+in+Pyqt6+%2B+PyQt6-WebEngine.&currency_code=USD'
__pix__ = 'https://nubank.com.br/pagar/3c3r2/LS2hiJJKzv'
__kofi__ = 'https://ko-fi.com/rafaeltosta'
__githubSponor__ = 'https://github.com/sponsors/rafatosta'

__licence__ = 'GNU General Public License v3.0'

# Página de doações exibida no app
__donationPage__ = 'https://rtosta.com/zapzap/#donate'

# URL do WhatsApp Web
__whatsapp_url__ = 'https://web.whatsapp.com/'

# User-Agent utilizado pelo WebEngine
__user_agent__ = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Limite padrão de contas
# 0 = ilimitado
# limite máximo permitido pelo sistema será controlado na UI
LIMITE_USERS = 10

# Caminho base do aplicativo
APP_PATH = QFileInfo(__file__).absolutePath()