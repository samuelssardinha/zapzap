# Documentação Técnica — ZapZap (Fork)

Esta documentação descreve a arquitetura interna do **ZapZap**, um cliente desktop para WhatsApp Web baseado em **PyQt6 + QtWebEngine**.

Este documento foi adaptado para o fork mantido por **Samuel Silva Sardinha**, cujo foco principal é suporte e melhorias para **macOS e Windows**.

Projeto original desenvolvido por **Rafael Tosta**.

---

# 1) Visão geral

O **ZapZap** é um cliente desktop para **WhatsApp Web** construído utilizando **PyQt6 + QtWebEngine**.

A aplicação encapsula:

https://web.whatsapp.com/

dentro de uma janela nativa, adicionando funcionalidades de integração com o sistema operacional, incluindo:

- múltiplas contas
- notificações nativas
- ícone de bandeja (system tray)
- suporte a temas
- customizações via CSS/JS
- atalhos de teclado
- gerenciamento de downloads
- corretor ortográfico
- gerenciamento de sessão

O aplicativo funciona essencialmente como um **wrapper desktop para WhatsApp Web**, mantendo toda a lógica de mensagens dentro da aplicação web oficial.

---

# 2) Stack e componentes principais

Linguagem:
Python 3.8+

Interface gráfica:
PyQt6

Engine Web:
PyQt6-WebEngine (Chromium embedado)

Persistência de configurações:
QSettings

Persistência de contas:
SQLite (arquivo `zapzap.db`)

Internacionalização:
gettext

Arquivos utilizados:
- po/*.po
- zapzap/po/*/LC_MESSAGES/*.mo

Empacotamento suportado no projeto original:
- Flatpak
- AppImage
- RPM
- instalação direta via pip

No fork atual o foco é execução direta em:

- macOS
- Windows

---

# 3) Fluxo de inicialização

Entrada principal da aplicação:

```
python -m zapzap
```

ou

```
zapzap
```

Fluxo interno:

1. O módulo `zapzap.__main__:main` é executado.
2. `SetupManager.apply()` configura variáveis de ambiente importantes:
   - escala da interface
   - dicionários
   - flags do QtWebEngine / Chromium
3. `TranslationManager.apply()` configura o domínio gettext e as traduções.
4. O **CrashDumpHandler global** é registrado.
5. A aplicação cria `SingleApplication` para impedir múltiplas instâncias simultâneas.
6. `MainWindow` é criada.
7. O estado da janela é restaurado:
   - geometria
   - estado da janela
   - tray
   - tema
8. `Browser` carrega as contas existentes.
9. Para cada conta habilitada é criado um `WebView`.
10. Cada `WebView` cria um `QWebEngineProfile` isolado e carrega:

```
https://web.whatsapp.com/
```

Cada conta possui um perfil Chromium separado.

---

# 4) Arquitetura em camadas

A arquitetura do projeto segue uma organização modular.

## 4.1 UI e controle

Diretório:

```
zapzap/controllers
```

Responsável por:

- comportamento da janela principal
- páginas de configurações
- fluxo da interface

Diretório:

```
zapzap/views
```

Contém classes Python geradas a partir de:

```
.ui
```

arquivos do Qt Designer.

Diretório:

```
zapzap/ui
```

Contém os arquivos `.ui` originais.

---

## 4.2 Navegação e sessão Web

Diretório:

```
zapzap/webengine
```

Componentes principais:

### WebView.py

Gerencia:

- perfil web isolado
- downloads
- spellcheck
- menu de contexto
- eventos da aba
- integração com notificações

### PageController.py

Extende:

```
QWebEnginePage
```

Responsável por:

- controlar navegação
- interceptar novas janelas
- abrir links externos no navegador padrão
- injetar addons
- aplicar customizações
- aplicar permissões
- sincronizar tema

---

## 4.3 Serviços de domínio

Diretório:

```
zapzap/services
```

Principais serviços:

SettingsManager  
Interface estática para `QSettings`.

CustomizationsManager  
Gerencia CSS e JS personalizados:

- globais
- por conta

ThemeManager  
Aplica:

- tema claro
- tema escuro
- tema automático

SysTrayManager  
Controla o ícone de bandeja e seu menu.

DownloadManager  
Gerencia downloads iniciados pelo QtWebEngine.

DictionariesManager  
Gerencia dicionários de correção ortográfica.

PathManager  
Resolve caminhos dependendo do ambiente de execução.

AddonsManager  
Carrega scripts JavaScript internos para injeção na página.

---

## 4.4 Sistema de notificações

`NotificationService` atua como uma **fachada de notificações**.

Ele escolhe automaticamente o backend de notificação em tempo de execução.

Dependendo do sistema operacional, diferentes APIs podem ser utilizadas.

As notificações respeitam preferências configuradas pelo usuário, incluindo:

- ocultar nome do contato
- ocultar conteúdo da mensagem
- desabilitar notificações por conta

---

## 4.5 Persistência de dados

Persistência ocorre em três níveis.

### Banco SQLite

Arquivo:

```
zapzap.db
```

Armazena:

- contas
- metadados das contas
- preferências associadas

### QSettings

Armazena:

- configurações do aplicativo
- tema
- comportamento da janela
- configurações de performance
- idioma do corretor ortográfico

### Sistema de arquivos local

Arquivos de customização:

```
customizations/global/css
customizations/global/js
customizations/accounts/<id>/css
customizations/accounts/<id>/js
customizations/extensions
```

---

# 5) Modelo de contas

Cada conta gera:

- um botão lateral (`PageButton`)
- uma aba web (`WebView`)
- um perfil Chromium isolado

Cada conta possui:

- notificações próprias
- customizações próprias
- configurações independentes

A primeira conta usa o identificador especial:

```
storage-whats
```

Esse alias existe por motivos de compatibilidade histórica do projeto.

---

# 6) Build, execução e release

Script principal:

```
run.py
```

Responsável por orquestrar:

- execução
- preview
- build

---

## 6.1 Desenvolvimento

Executar:

```
python run.py dev
```

ou

```
python run.py dev --build-translations
```

Esse modo:

- compila arquivos `.ui`
- compila traduções
- inicia o aplicativo

---

## 6.2 Preview

Preview de empacotamento:

Flatpak:

```
python run.py preview --flatpak
```

AppImage:

```
python run.py preview --appimage
```

---

## 6.3 Build

AppImage:

```
python run.py build --appimage <version>
```

Flatpak:

```
python run.py build --flatpak-onefile
```

---

# 7) Estrutura de diretórios

Resumo da estrutura principal:

```
zapzap/controllers
zapzap/webengine
zapzap/services
zapzap/models
zapzap/config
zapzap/resources
zapzap/views
zapzap/debug
zapzap/notifications
```

Outros diretórios:

```
po/
zapzap/po/
_scripts/
```

---

# 8) Extensão e manutenção

## Pontos recomendados de extensão

1. Novos serviços  
Adicionar em:

```
zapzap/services
```

2. Novas configurações  
Persistir via:

```
SettingsManager
```

3. Novas customizações web  
Utilizar:

```
CustomizationsManager
```

ou

```
AddonsManager
```

4. Novos backends de notificação  
Implementar backend adicional e registrar no `NotificationService`.

---

## Cuidados técnicos

Alterações em `SetupManager` podem afetar:

- inicialização do QtWebEngine
- compatibilidade entre sistemas

Alterações em notificações devem ser testadas cuidadosamente.

Chaves usadas em `QSettings` devem manter compatibilidade retroativa para evitar perda de configurações em atualizações.

---

# 9) Troubleshooting rápido

Problemas comuns:

Upload de arquivos não funciona  
Verificar permissões de acesso ao sistema de arquivos.

Corretor ortográfico não funciona  
Verificar caminho dos dicionários.

Tema não sincroniza  
Verificar backend de notificações e suporte do sistema.

Notificações não aparecem  
Verificar:

- preferências globais
- preferências da conta
- permissões do sistema operacional

---

# Créditos

Projeto original:

Rafael Tosta  
https://github.com/rafatosta/zapzap

Fork mantido por:

Samuel Silva Sardinha

---

Esta documentação pode evoluir futuramente para o padrão **ADR (Architecture Decision Records)** para registrar decisões arquiteturais importantes do projeto.