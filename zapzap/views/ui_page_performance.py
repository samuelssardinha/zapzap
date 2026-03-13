from gettext import gettext as _
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PagePerformance(object):

    def setupUi(self, PagePerformance):

        PagePerformance.setObjectName("PagePerformance")
        PagePerformance.resize(600, 650)
        PagePerformance.setWindowTitle("")

        # espaçamento checkbox
        PagePerformance.setStyleSheet("""
        QCheckBox::indicator {
            margin-right: 6px;
        }
        """)

        # layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(PagePerformance)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        # frame principal
        self.frame = QtWidgets.QFrame(parent=PagePerformance)
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

        self.label_title = QtWidgets.QLabel(parent=self.frame)

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)

        self.label_title.setFont(font)

        self.frameLayout.addWidget(self.label_title)

        # -------------------------------------------------
        # CACHE
        # -------------------------------------------------

        self.group_cache = QtWidgets.QGroupBox(parent=self.frame)
        self.cacheLayout = QtWidgets.QVBoxLayout(self.group_cache)
        self.cacheLayout.setSpacing(10)

        self.label = QtWidgets.QLabel(parent=self.group_cache)
        self.cache_type = QtWidgets.QComboBox(parent=self.group_cache)

        self.label1 = QtWidgets.QLabel(parent=self.group_cache)
        self.cache_size_max = QtWidgets.QComboBox(parent=self.group_cache)
        self.cache_size_max.addItem("")
        self.cache_size_max.addItem("")
        self.cache_size_max.addItem("")
        self.cache_size_max.addItem("")

        self.persistent_cookies = QtWidgets.QCheckBox(parent=self.group_cache)

        self.cacheLayout.addWidget(self.label)
        self.cacheLayout.addWidget(self.cache_type)

        self.cacheLayout.addWidget(self.label1)
        self.cacheLayout.addWidget(self.cache_size_max)

        self.cacheLayout.addWidget(self.persistent_cookies)

        self.frameLayout.addWidget(self.group_cache)

        # -------------------------------------------------
        # GPU
        # -------------------------------------------------

        self.group_gpu = QtWidgets.QGroupBox(parent=self.frame)
        self.vboxlayout = QtWidgets.QVBoxLayout(self.group_gpu)

        self.in_process_gpu = QtWidgets.QCheckBox(parent=self.group_gpu)
        self.disable_gpu = QtWidgets.QCheckBox(parent=self.group_gpu)
        self.disable_gpu_vsync = QtWidgets.QCheckBox(parent=self.group_gpu)
        self.software_rendering = QtWidgets.QCheckBox(parent=self.group_gpu)

        self.vboxlayout.addWidget(self.in_process_gpu)
        self.vboxlayout.addWidget(self.disable_gpu)
        self.vboxlayout.addWidget(self.disable_gpu_vsync)
        self.vboxlayout.addWidget(self.software_rendering)

        self.frameLayout.addWidget(self.group_gpu)

        # -------------------------------------------------
        # PROCESS
        # -------------------------------------------------

        self.group_process = QtWidgets.QGroupBox(parent=self.frame)
        self.gridlayout = QtWidgets.QVBoxLayout(self.group_process)

        self.single_process = QtWidgets.QCheckBox(parent=self.group_process)
        self.process_per_site = QtWidgets.QCheckBox(parent=self.group_process)

        self.label2 = QtWidgets.QLabel(parent=self.group_process)
        self.js_memory_limit = QtWidgets.QComboBox(parent=self.group_process)
        self.js_memory_limit.addItem("")
        self.js_memory_limit.addItem("")
        self.js_memory_limit.addItem("")
        self.js_memory_limit.addItem("")

        self.gridlayout.addWidget(self.single_process)
        self.gridlayout.addWidget(self.process_per_site)
        self.gridlayout.addWidget(self.label2)
        self.gridlayout.addWidget(self.js_memory_limit)

        self.frameLayout.addWidget(self.group_process)

        # -------------------------------------------------
        # WEB
        # -------------------------------------------------

        self.group_web = QtWidgets.QGroupBox(parent=self.frame)
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.group_web)

        self.scroll_animator = QtWidgets.QCheckBox(parent=self.group_web)
        self.background_throttling = QtWidgets.QCheckBox(parent=self.group_web)
        self.disable_animations = QtWidgets.QCheckBox(parent=self.group_web)

        self.vboxlayout1.addWidget(self.scroll_animator)
        self.vboxlayout1.addWidget(self.background_throttling)
        self.vboxlayout1.addWidget(self.disable_animations)

        self.frameLayout.addWidget(self.group_web)

        # -------------------------------------------------
        # ACTIONS
        # -------------------------------------------------

        self.hboxlayout = QtWidgets.QHBoxLayout()

        spacerItem = QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.hboxlayout.addItem(spacerItem)

        self.btn_restore = QtWidgets.QPushButton(parent=self.frame)
        self.hboxlayout.addWidget(self.btn_restore)

        self.frameLayout.addLayout(self.hboxlayout)

        # -------------------------------------------------
        # NOTE
        # -------------------------------------------------

        self.label3 = QtWidgets.QLabel(parent=self.frame)

        font = QtGui.QFont()
        font.setItalic(True)

        self.label3.setFont(font)

        self.frameLayout.addWidget(self.label3)

        # empurra conteúdo para cima
        self.frameLayout.addStretch()

        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(PagePerformance)

    def retranslateUi(self):

        self.label_title.setText(_("Performance (Experimental)"))

        self.group_cache.setTitle(_("Cache and Storage"))
        self.label.setText(_("Cache type"))
        self.label1.setText(_("Maximum cache size"))
        self.cache_size_max.setItemText(0, _("0 MB"))
        self.cache_size_max.setItemText(1, _("50 MB"))
        self.cache_size_max.setItemText(2, _("100 MB"))
        self.cache_size_max.setItemText(3, _("200 MB"))
        self.persistent_cookies.setText(_("Use persistent cookies"))

        self.group_gpu.setTitle(_("GPU and Rendering"))
        self.in_process_gpu.setText(_("Use GPU in the same process"))
        self.disable_gpu.setText(_("Disable GPU hardware acceleration"))
        self.disable_gpu_vsync.setText(_("Disable GPU VSync"))
        self.software_rendering.setText(_("Force software rendering (experimental)"))

        self.group_process.setTitle(_("Processes and Memory"))
        self.single_process.setText(_("Run everything in a single process"))
        self.process_per_site.setText(_("Use one process per site"))
        self.label2.setText(_("JavaScript memory limit"))
        self.js_memory_limit.setItemText(0, _("Automatic"))
        self.js_memory_limit.setItemText(1, _("Minimum (256 MB)"))
        self.js_memory_limit.setItemText(2, _("Default (1024 MB)"))
        self.js_memory_limit.setItemText(3, _("Maximum (4096 MB)"))

        self.group_web.setTitle(_("Web Behavior"))
        self.scroll_animator.setText(_("Animated scrolling"))
        self.background_throttling.setText(_("Allow background optimizations"))
        self.disable_animations.setText(_("Disable page animations"))

        self.btn_restore.setText(_("Restore defaults"))

        self.label3.setText(_("Note: Restart required to apply changes."))