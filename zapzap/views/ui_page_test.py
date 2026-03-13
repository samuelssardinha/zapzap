from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PageTest(object):

    def setupUi(self, PageTest):

        PageTest.setObjectName("PageTest")
        PageTest.resize(693, 620)
        PageTest.setWindowTitle("")

        # layout principal
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(PageTest)

        # layout horizontal (responsável pela centralização)
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        # spacer esquerdo
        spacer_left = QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout.addItem(spacer_left)

        # frame central
        self.frame = QtWidgets.QFrame(parent=PageTest)
        self.frame.setMinimumSize(QtCore.QSize(550, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(15)

        # título
        self.label = QtWidgets.QLabel(parent=self.frame)

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)

        self.label.setFont(font)
        self.label.setText("TEST PAGE")

        self.verticalLayout_2.addWidget(self.label)

        # conteúdo simples
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Test input")

        self.verticalLayout_2.addWidget(self.input)

        self.horizontalLayout.addWidget(self.frame)

        # spacer direito
        spacer_right = QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout.addItem(spacer_right)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        # spacer inferior (igual Network)
        spacer_bottom = QtWidgets.QSpacerItem(
            20, 295,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.verticalLayout_3.addItem(spacer_bottom)

        QtCore.QMetaObject.connectSlotsByName(PageTest)