# Notificações e Ícones Dinâmicos

Este documento descreve como o sistema de notificações funciona no **ZapZap** e quais são as limitações técnicas relacionadas à exibição de **ícones dinâmicos (como fotos de contato)**.

Este documento foi adaptado no fork mantido por **Samuel Silva Sardinha**, com foco em **macOS e Windows**.

O objetivo desta documentação é esclarecer o comportamento das notificações e evitar confusão sobre limitações que não são controladas diretamente pelo aplicativo.

---

# 📌 Resumo

O ZapZap utiliza o sistema de notificações nativo da plataforma onde está sendo executado.

Dependendo do sistema operacional, algumas funcionalidades podem ou não estar disponíveis.

| Sistema | Backend de Notificação | Ícones Dinâmicos |
|-------|-------------------------|------------------|
| macOS | Notification Center | ⚠️ Dependente do sistema |
| Windows | Windows Notifications | ⚠️ Dependente do sistema |

➡️ O comportamento pode variar dependendo das regras de cada sistema operacional.

---

# 🔔 Como funcionam as notificações

Quando uma nova mensagem chega no WhatsApp Web, o aplicativo:

1. intercepta o evento da página
2. envia a informação para o sistema de notificações do sistema operacional
3. exibe uma notificação contendo:
   - nome do contato
   - mensagem
   - ícone do aplicativo

Dependendo do ambiente, o sistema pode permitir ou não exibir **imagens dinâmicas**.

---

# 📷 Ícones dinâmicos (foto do contato)

Em algumas plataformas, notificações podem suportar:

- foto do contato
- avatar dinâmico
- imagens personalizadas

No entanto, essa funcionalidade depende **inteiramente das APIs do sistema operacional**.

Nem todos os sistemas permitem que aplicativos exibam imagens arbitrárias nas notificações.

Por esse motivo, o comportamento pode variar.

---

# ❗ Importante

Se você perceber que:

- a foto do contato **não aparece**
- apenas o **ícone do aplicativo** é exibido

isso **não é necessariamente um bug do ZapZap**.

Na maioria dos casos, trata-se de **limitações da API de notificações do sistema operacional**.

---

# 🧠 Decisão de arquitetura

O ZapZap foi projetado para:

- usar **as APIs oficiais do sistema**
- respeitar **as regras de segurança da plataforma**
- evitar hacks ou métodos não suportados

Isso garante:

- maior estabilidade
- maior compatibilidade entre sistemas
- menor risco de falhas após atualizações do sistema operacional

---

# 💡 Alternativas utilizadas

Quando ícones dinâmicos não são suportados, o aplicativo prioriza:

- nome do contato no título
- mensagem exibida claramente
- acesso rápido à conversa

Essas são as opções **mais compatíveis com diferentes sistemas operacionais**.

---

# 📅 Suporte futuro

Caso os sistemas operacionais passem a permitir notificações mais avançadas, o ZapZap poderá implementar suporte adicional.

Essas mudanças dependem exclusivamente das APIs fornecidas pelo sistema.

---

# ✅ Conclusão

Se as notificações exibirem apenas o ícone do aplicativo em vez da foto do contato, isso pode ser o comportamento esperado do sistema operacional.

O ZapZap sempre utilizará a melhor implementação possível dentro das limitações da plataforma.

---

# Créditos

Projeto original:

Rafael Tosta  
https://github.com/rafatosta/zapzap

Fork mantido por:

Samuel Silva Sardinha