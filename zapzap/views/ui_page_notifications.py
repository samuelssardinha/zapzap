from gettext import gettext as _
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PageNotifications(object):

    def setupUi(self, PageNotifications):

        PageNotifications.setObjectName("PageNotifications")
        PageNotifications.resize(600, 500)
        PageNotifications.setWindowTitle("")

        # layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(PageNotifications)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        # frame principal
        self.frame = QtWidgets.QFrame(parent=PageNotifications)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.frame.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
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
        # NOTIFICATION GROUP
        # -------------------------------------------------

        self.notify_groupBox = QtWidgets.QGroupBox(parent=self.frame)
        self.notify_groupBox.setCheckable(True)

        self.notifyLayout = QtWidgets.QVBoxLayout(self.notify_groupBox)
        self.notifyLayout.setSpacing(8)

        # checkbox spacing style
        checkbox_style = """
        QCheckBox::indicator {
            margin-right: 6px;
        }
        """

        self.show_photo = QtWidgets.QCheckBox(parent=self.notify_groupBox)
        self.show_photo.setChecked(True)
        self.show_photo.setStyleSheet(checkbox_style)

        self.show_name = QtWidgets.QCheckBox(parent=self.notify_groupBox)
        self.show_name.setChecked(True)
        self.show_name.setStyleSheet(checkbox_style)

        self.show_msg = QtWidgets.QCheckBox(parent=self.notify_groupBox)
        self.show_msg.setChecked(True)
        self.show_msg.setStyleSheet(checkbox_style)

        self.notifyLayout.addWidget(self.show_photo)
        self.notifyLayout.addWidget(self.show_name)
        self.notifyLayout.addWidget(self.show_msg)

        self.frameLayout.addWidget(self.notify_groupBox)

        # -------------------------------------------------
        # DONATION MESSAGE
        # -------------------------------------------------

        self.donationMessage = QtWidgets.QCheckBox(parent=self.frame)
        self.donationMessage.setStyleSheet(checkbox_style)

        self.frameLayout.addWidget(self.donationMessage)

        # empurra conteúdo para cima
        self.frameLayout.addStretch()

        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(PageNotifications)

        QtCore.QMetaObject.connectSlotsByName(PageNotifications)

    # -------------------------------------------------
    # TRANSLATIONS
    # -------------------------------------------------

    def retranslateUi(self, PageNotifications):

        self.label.setText(_("Notifications"))

        self.notify_groupBox.setTitle(
            _("Work area notifications")
        )

        self.show_photo.setText(
            _("Show the photo of the sender")
        )

        self.show_name.setText(
            _("Show the sender's name")
        )

        self.show_msg.setText(
            _("Show message preview")
        )

        self.donationMessage.setText(
            _("Hide donation notification")
        )