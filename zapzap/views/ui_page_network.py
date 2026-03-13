from gettext import gettext as _
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PageNetwork(object):

    def setupUi(self, PageNetwork):

        PageNetwork.setObjectName("PageNetwork")
        PageNetwork.resize(600, 500)
        PageNetwork.setWindowTitle("")

        # layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(PageNetwork)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        # frame principal
        self.frame = QtWidgets.QFrame(parent=PageNetwork)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

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
        # PROXY SETTINGS
        # -------------------------------------------------

        self.proxyCheckBox = QtWidgets.QGroupBox(parent=self.frame)
        self.proxyCheckBox.setCheckable(True)
        self.proxyCheckBox.setChecked(False)

        self.proxyLayout = QtWidgets.QVBoxLayout(self.proxyCheckBox)
        self.proxyLayout.setSpacing(12)

        # Proxy type
        self.label_proxy_type = QtWidgets.QLabel(parent=self.proxyCheckBox)
        self.proxyComboBox = QtWidgets.QComboBox(parent=self.proxyCheckBox)

        self.proxyLayout.addWidget(self.label_proxy_type)
        self.proxyLayout.addWidget(self.proxyComboBox)

        # Description
        self.proxyDescription = QtWidgets.QLabel(parent=self.proxyCheckBox)
        self.proxyDescription.setWordWrap(True)

        font = QtGui.QFont()
        font.setPointSize(10)
        self.proxyDescription.setFont(font)

        self.proxyLayout.addWidget(self.proxyDescription)

        # Hostname
        self.hostNameLabel = QtWidgets.QLabel(parent=self.proxyCheckBox)
        self.setHostName = QtWidgets.QLineEdit(parent=self.proxyCheckBox)

        self.proxyLayout.addWidget(self.hostNameLabel)
        self.proxyLayout.addWidget(self.setHostName)

        # Port
        self.portLabel = QtWidgets.QLabel(parent=self.proxyCheckBox)
        self.setPort = QtWidgets.QLineEdit(parent=self.proxyCheckBox)

        self.proxyLayout.addWidget(self.portLabel)
        self.proxyLayout.addWidget(self.setPort)

        # User
        self.userLabel = QtWidgets.QLabel(parent=self.proxyCheckBox)
        self.setUser = QtWidgets.QLineEdit(parent=self.proxyCheckBox)

        self.proxyLayout.addWidget(self.userLabel)
        self.proxyLayout.addWidget(self.setUser)

        # Password
        self.passwordLabel = QtWidgets.QLabel(parent=self.proxyCheckBox)
        self.setPassword = QtWidgets.QLineEdit(parent=self.proxyCheckBox)

        self.setPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.proxyLayout.addWidget(self.passwordLabel)
        self.proxyLayout.addWidget(self.setPassword)

        # -------------------------------------------------
        # BUTTON ROW
        # -------------------------------------------------

        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.btn_ok = QtWidgets.QPushButton(parent=self.proxyCheckBox)
        self.btn_ok.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.buttonLayout.addWidget(self.btn_ok)

        spacer = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )

        self.buttonLayout.addItem(spacer)

        self.btn_restore = QtWidgets.QPushButton(parent=self.proxyCheckBox)
        self.btn_restore.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.buttonLayout.addWidget(self.btn_restore)

        self.proxyLayout.addLayout(self.buttonLayout)

        self.frameLayout.addWidget(self.proxyCheckBox)

        # empurra conteúdo para cima
        self.frameLayout.addStretch()

        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(PageNetwork)


    def retranslateUi(self):

        self.label.setText(_("Network"))

        self.proxyCheckBox.setTitle(_("Network proxy"))

        self.label_proxy_type.setText(_("Proxy type"))

        self.proxyDescription.setText(_("Description"))

        self.hostNameLabel.setText(_("Hostname"))
        self.portLabel.setText(_("Port"))
        self.userLabel.setText(_("User"))
        self.passwordLabel.setText(_("Password"))

        self.btn_ok.setText(_("Apply"))
        self.btn_restore.setText(_("Restore"))