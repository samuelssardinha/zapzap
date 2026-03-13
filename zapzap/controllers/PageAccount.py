from PyQt6.QtWidgets import QWidget, QApplication

from zapzap.controllers.CardUser import CardUser
from zapzap.models.User import User
from zapzap.services.AlertManager import AlertManager
from zapzap.views.ui_page_account import Ui_PageAccount


class PageAccount(QWidget, Ui_PageAccount):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        # carrega usuários existentes
        self._load_users()

        # botão novo usuário
        self.btn_new_user.clicked.connect(self._new_user)

    # ------------------------------------------------------
    # LOAD USERS
    # ------------------------------------------------------

    def _load_users(self):
        """Carrega usuários e cria os cards correspondentes."""

        # limpa layout primeiro
        while self.user_list_layout.count():

            item = self.user_list_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        # carrega usuários do modelo
        self.user_list = User.select()

        for user in self.user_list:

            card = CardUser(user)

            self.user_list_layout.addWidget(card)

    # ------------------------------------------------------
    # NEW USER
    # ------------------------------------------------------

    def _new_user(self):
        """Cria novo usuário se limite não for atingido."""

        new_user = User.create_new_user()

        if not new_user:
            AlertManager.limit_users(self)
            return

        # adiciona card na interface
        card = CardUser(new_user)
        self.user_list_layout.addWidget(card)

        # atualiza navegador
        QApplication.instance().getWindow().browser.add_new_user(new_user)