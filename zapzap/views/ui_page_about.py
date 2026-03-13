from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PageAbout(object):

    def setupUi(self, PageAbout):

        PageAbout.setObjectName("PageAbout")
        PageAbout.resize(600, 500)
        PageAbout.setWindowTitle("")

        # layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(PageAbout)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        # frame principal
        self.frame = QtWidgets.QFrame(parent=PageAbout)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.frame.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )

        self.frameLayout = QtWidgets.QVBoxLayout(self.frame)
        self.frameLayout.setSpacing(15)

        # TITLE
        self.label = QtWidgets.QLabel(parent=self.frame)

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)

        self.label.setFont(font)

        self.frameLayout.addWidget(self.label)

        # ICON (usado pelo controller)
        self.icon = QtWidgets.QPushButton(parent=self.frame)
        self.icon.setFlat(True)
        self.icon.setIconSize(QtCore.QSize(96, 96))

        self.frameLayout.addWidget(
            self.icon,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # DESCRIPTION
        self.description = QtWidgets.QLabel(parent=self.frame)
        self.description.setWordWrap(True)
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.frameLayout.addWidget(self.description)

        # WEBSITE LINK
        self.website = QtWidgets.QLabel(parent=self.frame)
        self.website.setOpenExternalLinks(True)
        self.website.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.frameLayout.addWidget(self.website)

        # VERSION
        self.version = QtWidgets.QLabel(parent=self.frame)

        font = QtGui.QFont()
        font.setItalic(True)

        self.version.setFont(font)
        self.version.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.frameLayout.addWidget(self.version)

        # empurra conteúdo para cima
        self.frameLayout.addStretch()

        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(PageAbout)

        QtCore.QMetaObject.connectSlotsByName(PageAbout)

    def retranslateUi(self, PageAbout):

        _translate = QtCore.QCoreApplication.translate

        self.label.setText(_translate("PageAbout", "About"))

        self.description.setText(
            _translate(
                "PageAbout",
                "ZapZap is an unofficial WhatsApp Web client built with Qt."
            )
        )

        self.website.setText(
            _translate(
                "PageAbout",
                "<a href='https://github.com/rafatosta/zapzap'>Project website</a>"
            )
        )

        self.version.setText(
            _translate(
                "PageAbout",
                "Version"
            )
        )