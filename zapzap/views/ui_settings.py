from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):

    def setupUi(self, Settings):

        Settings.setObjectName("Settings")
        Settings.adjustSize()

        Settings.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum
        )

        Settings.setWindowTitle("")
        Settings.setStyleSheet("")

        # --------------------------------------------------
        # LAYOUT PRINCIPAL
        # --------------------------------------------------

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Settings)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # --------------------------------------------------
        # CONTAINER PRINCIPAL
        # --------------------------------------------------

        self.container = QtWidgets.QWidget(parent=Settings)
        self.container.setObjectName("container")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.container)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # --------------------------------------------------
        # SIDEBAR
        # --------------------------------------------------

        self.sidebar = QtWidgets.QFrame(parent=self.container)

        self.sidebar.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Preferred
        )

        self.sidebar.setMinimumSize(QtCore.QSize(300, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(300, 16777215))

        self.sidebar.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.sidebar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.sidebar.setObjectName("sidebar")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # --------------------------------------------------
        # MENU LAYOUT
        # --------------------------------------------------

        self.menu_layout = QtWidgets.QFrame(parent=self.sidebar)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.menu_layout)
        self.verticalLayout_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        # --------------------------------------------------
        # BOTÃO BACK
        # --------------------------------------------------

        self.btn_back = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_back)

        # --------------------------------------------------
        # LABEL SETTINGS
        # --------------------------------------------------

        self.label_4 = QtWidgets.QLabel(parent=self.menu_layout)

        font = QtGui.QFont()
        font.setPointSize(8)

        self.label_4.setFont(font)

        self.verticalLayout_2.addWidget(self.label_4)

        # linha
        self.line_3 = QtWidgets.QFrame(parent=self.menu_layout)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        # --------------------------------------------------
        # BOTÕES SETTINGS
        # --------------------------------------------------

        self.btn_page_general = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_page_general)

        self.btn_account = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_account)

        # --------------------------------------------------
        # LABEL TOOLS
        # --------------------------------------------------

        self.label_3 = QtWidgets.QLabel(parent=self.menu_layout)

        font = QtGui.QFont()
        font.setPointSize(8)

        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.line = QtWidgets.QFrame(parent=self.menu_layout)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        # --------------------------------------------------
        # BOTÕES TOOLS
        # --------------------------------------------------

        self.btn_page_appearence = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_page_appearence)

        self.btn_page_customizations = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_page_customizations)

        self.btn_page_notifications = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_page_notifications)

        self.btn_page_performance = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_page_performance)

        self.btn_page_network = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_page_network)

        # --------------------------------------------------
        # LABEL HELP
        # --------------------------------------------------

        self.label = QtWidgets.QLabel(parent=self.menu_layout)

        font = QtGui.QFont()
        font.setPointSize(8)

        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.line_4 = QtWidgets.QFrame(parent=self.menu_layout)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_4)

        # --------------------------------------------------
        # BOTÃO ABOUT
        # --------------------------------------------------

        self.btn_page_help = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_page_help)

        # --------------------------------------------------
        # BOTÃO QUIT
        # --------------------------------------------------

        self.btn_quit = QtWidgets.QPushButton(parent=self.menu_layout)
        self.verticalLayout_2.addWidget(self.btn_quit)

        # --------------------------------------------------
        # SCROLL AREA DA SIDEBAR
        # --------------------------------------------------

        self.scroll = QtWidgets.QScrollArea(self.sidebar)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.scroll.setWidget(self.menu_layout)

        self.verticalLayout.addWidget(self.scroll)

        # adiciona sidebar
        self.horizontalLayout.addWidget(self.sidebar)

        # --------------------------------------------------
        # ÁREA DAS PÁGINAS
        # --------------------------------------------------

        self.pages = QtWidgets.QStackedWidget(parent=self.container)
        self.pages.setObjectName("pages")

        self.horizontalLayout.addWidget(self.pages)

        # adiciona container
        self.horizontalLayout_2.addWidget(self.container)

        self.retranslateUi(Settings)

        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):

        _translate = QtCore.QCoreApplication.translate

        self.btn_back.setText(_translate("Settings", "Back"))

        self.label_4.setText(_translate("Settings", "SETTINGS"))

        self.btn_page_general.setText(_translate("Settings", "General"))
        self.btn_account.setText(_translate("Settings", "Accounts"))

        self.label_3.setText(_translate("Settings", "TOOLS"))

        self.btn_page_appearence.setText(_translate("Settings", "Appearance"))
        self.btn_page_customizations.setText(_translate("Settings", "Customizations"))
        self.btn_page_notifications.setText(_translate("Settings", "Notifications"))
        self.btn_page_performance.setText(_translate("Settings", "Performance"))
        self.btn_page_network.setText(_translate("Settings", "Network"))

        self.label.setText(_translate("Settings", "HELP"))

        self.btn_page_help.setText(_translate("Settings", "About"))

        self.btn_quit.setText(_translate("Settings", "Quit"))