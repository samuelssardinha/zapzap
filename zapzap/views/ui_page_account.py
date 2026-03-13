from gettext import gettext as _
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PageAccount(object):

    def setupUi(self, PageAccount):

        PageAccount.setObjectName("PageAccount")
        PageAccount.resize(600, 500)
        PageAccount.setWindowTitle("")

        # layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(PageAccount)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        # frame principal
        self.frame = QtWidgets.QFrame(parent=PageAccount)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.frame.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )

        self.frameLayout = QtWidgets.QVBoxLayout(self.frame)
        self.frameLayout.setSpacing(15)

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        self.label = QtWidgets.QLabel(parent=self.frame)

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)

        self.label.setFont(font)

        self.frameLayout.addWidget(self.label)

        # -------------------------------------------------
        # NEW ACCOUNT BUTTON
        # -------------------------------------------------

        self.btn_new_user = QtWidgets.QPushButton(parent=self.frame)

        self.frameLayout.addWidget(self.btn_new_user)

        # -------------------------------------------------
        # SCROLL AREA
        # -------------------------------------------------

        self.scrollArea = QtWidgets.QScrollArea(parent=self.frame)

        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        self.scrollAreaWidgetContents.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_users = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents
        )

        self.verticalLayout_users.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_users.setSpacing(6)

        # layout onde os usuários são adicionados dinamicamente
        self.user_list_layout = QtWidgets.QVBoxLayout()
        self.user_list_layout.setContentsMargins(0, 0, 0, 0)
        self.user_list_layout.setSpacing(6)

        self.verticalLayout_users.addLayout(self.user_list_layout)

        # empurra conteúdo para cima
        self.verticalLayout_users.addStretch()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.frameLayout.addWidget(self.scrollArea)

        # adiciona frame ao layout principal
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(PageAccount)

    def retranslateUi(self):

        self.label.setText(
            _("My accounts")
        )

        self.btn_new_user.setText(
            _("New account")
        )