from gettext import gettext as _
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PageGeneral(object):

    def setupUi(self, PageGeneral):
        PageGeneral.setObjectName("PageGeneral")
        PageGeneral.resize(600, 500)
        PageGeneral.setWindowTitle("")

        # espaçamento checkbox
        PageGeneral.setStyleSheet("""
        QCheckBox::indicator {
            margin-right: 6px;
        }
        """)

        self.verticalLayout = QtWidgets.QVBoxLayout(PageGeneral)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        self.frame = QtWidgets.QFrame(parent=PageGeneral)
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

        # DOWNLOAD DIRECTORY
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.frame)

        self.groupBox_3.setContentsMargins(10, 10, 10, 10)

        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)

        self.download_path = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.download_path.setReadOnly(True)

        self.gridLayout_2.addWidget(self.download_path, 0, 0)

        self.btn_path_download = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btn_path_download.setText("")

        self.gridLayout_2.addWidget(self.btn_path_download, 0, 1)

        self.btn_restore_path_download = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btn_restore_path_download.setText("")

        self.gridLayout_2.addWidget(self.btn_restore_path_download, 0, 2)

        self.frameLayout.addWidget(self.groupBox_3)

        # SPELLCHECKER
        self.spellchecker_groupBox = QtWidgets.QGroupBox(parent=self.frame)

        self.spellchecker_groupBox.setCheckable(True)
        self.spellchecker_groupBox.setContentsMargins(10, 10, 10, 10)

        self.gridLayout = QtWidgets.QGridLayout(self.spellchecker_groupBox)

        self.spell_comboBox = QtWidgets.QComboBox(parent=self.spellchecker_groupBox)

        self.gridLayout.addWidget(self.spell_comboBox, 0, 0, 1, 3)

        self.label_2 = QtWidgets.QLabel(parent=self.spellchecker_groupBox)

        self.gridLayout.addWidget(self.label_2, 1, 0)

        self.dic_path = QtWidgets.QLineEdit(parent=self.spellchecker_groupBox)
        self.dic_path.setReadOnly(True)

        self.gridLayout.addWidget(self.dic_path, 2, 0)

        self.btn_path_spell = QtWidgets.QPushButton(parent=self.spellchecker_groupBox)
        self.btn_path_spell.setText("")

        self.gridLayout.addWidget(self.btn_path_spell, 2, 1)

        self.btn_default_path_spell = QtWidgets.QPushButton(parent=self.spellchecker_groupBox)
        self.btn_default_path_spell.setText("")

        self.gridLayout.addWidget(self.btn_default_path_spell, 2, 2)

        self.label_3 = QtWidgets.QLabel(parent=self.spellchecker_groupBox)

        font = QtGui.QFont()
        font.setItalic(True)

        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 3, 0)

        self.frameLayout.addWidget(self.spellchecker_groupBox)

        # BEHAVIOR
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.frame)

        self.groupBox_2.setContentsMargins(10, 10, 10, 10)

        self.verticalLayout_behavior = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_behavior.setSpacing(6)

        self.btn_quit_in_close = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.verticalLayout_behavior.addWidget(self.btn_quit_in_close)

        self.btn_start_background = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.verticalLayout_behavior.addWidget(self.btn_start_background)

        self.btn_start_system = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.verticalLayout_behavior.addWidget(self.btn_start_system)

        self.dontUseNativeDialog = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.verticalLayout_behavior.addWidget(self.dontUseNativeDialog)

        self.btn_wayland = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.verticalLayout_behavior.addWidget(self.btn_wayland)

        self.frameLayout.addWidget(self.groupBox_2)

        # empurra conteúdo para cima
        self.frameLayout.addStretch()

        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(PageGeneral)

    def retranslateUi(self):

        self.label.setText(_("General"))

        self.groupBox_3.setTitle(_("Download Directory"))

        self.btn_path_download.setToolTip(
            _("Set new folder for downloads")
        )

        self.btn_restore_path_download.setToolTip(
            _("Define default folder for downloads")
        )

        self.spellchecker_groupBox.setTitle(_("Spellchecker"))

        self.label_2.setText(_("Directory"))

        self.btn_path_spell.setToolTip(
            _("Recognizes only compiled dictionaries (.bdic)")
        )

        self.btn_default_path_spell.setToolTip(
            _("Define standard dictionaries")
        )

        self.label_3.setText(_("Note: Required restart."))

        self.groupBox_2.setTitle(_("Behavior"))

        self.btn_quit_in_close.setText(
            _("Close when closing the window")
        )

        self.btn_start_background.setText(
            _("Start minimized")
        )

        self.btn_start_system.setText(
            _("Start with the system")
        )

        self.dontUseNativeDialog.setText(
            _("Don't use a platform-native file dialog")
        )

        self.btn_wayland.setText(
            _("Wayland window system")
        )