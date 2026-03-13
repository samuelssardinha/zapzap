from gettext import gettext as _
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PageAppearance(object):

    def setupUi(self, PageAppearance):

        PageAppearance.setObjectName("PageAppearance")
        PageAppearance.resize(600, 500)
        PageAppearance.setWindowTitle("")

        # espaço visual checkbox
        PageAppearance.setStyleSheet("""
        QCheckBox::indicator {
            margin-right: 6px;
        }
        """)

        # layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(PageAppearance)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        # frame principal
        self.frame = QtWidgets.QFrame(parent=PageAppearance)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.frame.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )

        self.frameLayout = QtWidgets.QVBoxLayout(self.frame)
        self.frameLayout.setSpacing(15)

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        self.label = QtWidgets.QLabel(parent=self.frame)

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)

        self.label.setFont(font)

        self.frameLayout.addWidget(self.label)

        # --------------------------------------------------
        # STYLE
        # --------------------------------------------------

        self.style_groupBox = QtWidgets.QGroupBox(parent=self.frame)
        self.styleLayout = QtWidgets.QGridLayout(self.style_groupBox)

        self.theme_auto_radioButton = QtWidgets.QRadioButton(parent=self.style_groupBox)
        self.theme_auto_radioButton.setChecked(True)

        self.theme_light_radioButton = QtWidgets.QRadioButton(parent=self.style_groupBox)
        self.theme_dark_radioButton = QtWidgets.QRadioButton(parent=self.style_groupBox)

        self.styleLayout.addWidget(self.theme_auto_radioButton, 0, 0)
        self.styleLayout.addWidget(self.theme_light_radioButton, 0, 1)
        self.styleLayout.addWidget(self.theme_dark_radioButton, 0, 2)

        self.frameLayout.addWidget(self.style_groupBox)

        # --------------------------------------------------
        # TRAY ICON
        # --------------------------------------------------

        self.tray_groupBox = QtWidgets.QGroupBox(parent=self.frame)
        self.tray_groupBox.setCheckable(True)

        self.trayLayout = QtWidgets.QGridLayout(self.tray_groupBox)

        self.tray_default_radioButton = QtWidgets.QRadioButton(parent=self.tray_groupBox)
        self.tray_default_radioButton.setChecked(True)

        self.tray_slight_radioButton = QtWidgets.QRadioButton(parent=self.tray_groupBox)
        self.tray_sdark_radioButton = QtWidgets.QRadioButton(parent=self.tray_groupBox)

        self.line = QtWidgets.QFrame(parent=self.tray_groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)

        self.notificationCounter = QtWidgets.QCheckBox(parent=self.tray_groupBox)

        self.trayLayout.addWidget(self.tray_default_radioButton, 0, 0)
        self.trayLayout.addWidget(self.tray_slight_radioButton, 0, 1)
        self.trayLayout.addWidget(self.tray_sdark_radioButton, 0, 2)

        self.trayLayout.addWidget(self.line, 1, 0, 1, 3)

        self.trayLayout.addWidget(self.notificationCounter, 2, 0, 1, 3)

        self.frameLayout.addWidget(self.tray_groupBox)

        # --------------------------------------------------
        # SIDEBAR
        # --------------------------------------------------

        self.browser_sidebar = QtWidgets.QCheckBox(parent=self.frame)
        self.browser_sidebar.setChecked(True)

        self.frameLayout.addWidget(self.browser_sidebar)

        # --------------------------------------------------
        # MENU BAR
        # --------------------------------------------------

        self.mainwindow_menu = QtWidgets.QCheckBox(parent=self.frame)
        self.mainwindow_menu.setChecked(True)

        self.frameLayout.addWidget(self.mainwindow_menu)

        # --------------------------------------------------
        # SCALE
        # --------------------------------------------------

        self.scaleLayout = QtWidgets.QGridLayout()

        self.scaleLabel = QtWidgets.QLabel(parent=self.frame)

        self.scaleComboBox = QtWidgets.QComboBox(parent=self.frame)

        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")

        self.scaleLayout.addWidget(self.scaleLabel, 0, 0)
        self.scaleLayout.addWidget(self.scaleComboBox, 0, 1)

        self.frameLayout.addLayout(self.scaleLayout)

        # --------------------------------------------------
        # NOTE
        # --------------------------------------------------

        self.label_2 = QtWidgets.QLabel(parent=self.frame)

        font = QtGui.QFont()
        font.setItalic(True)

        self.label_2.setFont(font)

        self.frameLayout.addWidget(self.label_2)

        # empurra conteúdo para cima
        self.frameLayout.addStretch()

        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(PageAppearance)


    def retranslateUi(self):

        self.label.setText(_("Appearance"))

        self.style_groupBox.setTitle(_("Style"))

        self.theme_auto_radioButton.setText(_("Adaptive"))
        self.theme_dark_radioButton.setText(_("Dark"))
        self.theme_light_radioButton.setText(_("Light"))

        self.tray_groupBox.setTitle(_("Tray icon"))

        self.notificationCounter.setText(
            _("Remove notification indicator")
        )

        self.tray_default_radioButton.setText(_("Default"))
        self.tray_sdark_radioButton.setText(_("Symbolic dark"))
        self.tray_slight_radioButton.setText(_("Symbolic light"))

        self.browser_sidebar.setText(
            _("Show sidebar")
        )

        self.mainwindow_menu.setText(
            _("Show menu bar")
        )

        self.scaleLabel.setText(_("Scale"))

        self.scaleComboBox.setItemText(0, _("100 %"))
        self.scaleComboBox.setItemText(1, _("125 %"))
        self.scaleComboBox.setItemText(2, _("150 %"))
        self.scaleComboBox.setItemText(3, _("175 %"))
        self.scaleComboBox.setItemText(4, _("200 %"))

        self.label_2.setText(
            _("Note: The change of scale will only have effect until restarting.")
        )