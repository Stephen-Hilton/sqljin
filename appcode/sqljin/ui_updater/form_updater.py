# Form implementation generated from reading ui file 'c:\git\sqljin\appcode\sqljin\form_updater.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_sjUpdater(object):
    def setupUi(self, sjUpdater):
        sjUpdater.setObjectName("sjUpdater")
        sjUpdater.resize(445, 529)
        self.centralwidget = QtWidgets.QWidget(sjUpdater)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTitle = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")
        self.horizontalLayout.addWidget(self.lblTitle)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.btnExpand = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/arrow-expand-all.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.btnExpand.setIcon(icon)
        self.btnExpand.setObjectName("btnExpand")
        self.horizontalLayout.addWidget(self.btnExpand)
        self.btnCollapse = QtWidgets.QToolButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/arrow-collapse-all.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.btnCollapse.setIcon(icon1)
        self.btnCollapse.setObjectName("btnCollapse")
        self.horizontalLayout.addWidget(self.btnCollapse)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chkAutoUpdate = QtWidgets.QCheckBox(self.layoutWidget)
        self.chkAutoUpdate.setObjectName("chkAutoUpdate")
        self.horizontalLayout_2.addWidget(self.chkAutoUpdate)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnCollAdd = QtWidgets.QToolButton(self.layoutWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/plus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.btnCollAdd.setIcon(icon2)
        self.btnCollAdd.setObjectName("btnCollAdd")
        self.horizontalLayout_2.addWidget(self.btnCollAdd)
        self.btnCollRemove = QtWidgets.QToolButton(self.layoutWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/minus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.btnCollRemove.setIcon(icon3)
        self.btnCollRemove.setObjectName("btnCollRemove")
        self.horizontalLayout_2.addWidget(self.btnCollRemove)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.tblUpdates = QtWidgets.QTableWidget(self.layoutWidget)
        self.tblUpdates.setMinimumSize(QtCore.QSize(0, 120))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.tblUpdates.setFont(font)
        self.tblUpdates.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tblUpdates.setAlternatingRowColors(False)
        self.tblUpdates.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tblUpdates.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tblUpdates.setTextElideMode(QtCore.Qt.TextElideMode.ElideRight)
        self.tblUpdates.setObjectName("tblUpdates")
        self.tblUpdates.setColumnCount(5)
        self.tblUpdates.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblUpdates.setItem(4, 3, item)
        self.tblUpdates.horizontalHeader().setVisible(True)
        self.tblUpdates.horizontalHeader().setCascadingSectionResizes(False)
        self.tblUpdates.horizontalHeader().setSortIndicatorShown(False)
        self.tblUpdates.horizontalHeader().setStretchLastSection(True)
        self.tblUpdates.verticalHeader().setCascadingSectionResizes(False)
        self.tblUpdates.verticalHeader().setDefaultSectionSize(24)
        self.tblUpdates.verticalHeader().setSortIndicatorShown(False)
        self.tblUpdates.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tblUpdates)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.btnUpdateRun = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnUpdateRun.sizePolicy().hasHeightForWidth())
        self.btnUpdateRun.setSizePolicy(sizePolicy)
        self.btnUpdateRun.setMaximumSize(QtCore.QSize(125, 16777215))
        self.btnUpdateRun.setBaseSize(QtCore.QSize(0, 0))
        self.btnUpdateRun.setObjectName("btnUpdateRun")
        self.horizontalLayout_4.addWidget(self.btnUpdateRun)
        self.btnPause = QtWidgets.QPushButton(self.layoutWidget)
        self.btnPause.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnPause.setObjectName("btnPause")
        self.horizontalLayout_4.addWidget(self.btnPause)
        self.horizontalLayout_4.setStretch(1, 2)
        self.horizontalLayout_4.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.line = QtWidgets.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_7.addWidget(self.label_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.chkAutoApp = QtWidgets.QCheckBox(self.layoutWidget)
        self.chkAutoApp.setObjectName("chkAutoApp")
        self.horizontalLayout_5.addWidget(self.chkAutoApp)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7.setStretch(1, 100)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.btnOpenApp = QtWidgets.QPushButton(self.layoutWidget)
        self.btnOpenApp.setEnabled(True)
        self.btnOpenApp.setMinimumSize(QtCore.QSize(0, 42))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnOpenApp.setFont(font)
        self.btnOpenApp.setObjectName("btnOpenApp")
        self.horizontalLayout_3.addWidget(self.btnOpenApp)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.line_3 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_4.addWidget(self.line_3)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_8.addWidget(self.label_3)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_9.addWidget(self.label_4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.txtLogs = QtWidgets.QPlainTextEdit(self.layoutWidget1)
        self.txtLogs.setObjectName("txtLogs")
        self.verticalLayout_4.addWidget(self.txtLogs)
        self.verticalLayout_5.addWidget(self.splitter)
        sjUpdater.setCentralWidget(self.centralwidget)

        self.retranslateUi(sjUpdater)
        QtCore.QMetaObject.connectSlotsByName(sjUpdater)

    def retranslateUi(self, sjUpdater):
        _translate = QtCore.QCoreApplication.translate
        sjUpdater.setWindowTitle(_translate("sjUpdater", "Application Update Utility"))
        self.lblTitle.setText(_translate("sjUpdater", "SQLJin Environment Update"))
        self.btnExpand.setText(_translate("sjUpdater", "..."))
        self.btnCollapse.setText(_translate("sjUpdater", "..."))
        self.chkAutoUpdate.setText(_translate("sjUpdater", "Auto-Update on Open"))
        self.btnCollAdd.setToolTip(_translate("sjUpdater", "Add a new Organization"))
        self.btnCollAdd.setText(_translate("sjUpdater", "..."))
        self.btnCollRemove.setToolTip(_translate("sjUpdater", "Remove a highlighted Organization"))
        self.btnCollRemove.setText(_translate("sjUpdater", "..."))
        item = self.tblUpdates.verticalHeaderItem(0)
        item.setText(_translate("sjUpdater", "Application"))
        item = self.tblUpdates.verticalHeaderItem(1)
        item.setText(_translate("sjUpdater", "Global"))
        item = self.tblUpdates.verticalHeaderItem(2)
        item.setText(_translate("sjUpdater", "Teradata"))
        item = self.tblUpdates.verticalHeaderItem(3)
        item.setText(_translate("sjUpdater", "Teradata Partner"))
        item = self.tblUpdates.verticalHeaderItem(4)
        item.setText(_translate("sjUpdater", "Wipro"))
        item = self.tblUpdates.horizontalHeaderItem(0)
        item.setText(_translate("sjUpdater", "Type"))
        item = self.tblUpdates.horizontalHeaderItem(1)
        item.setText(_translate("sjUpdater", "Local Version"))
        item = self.tblUpdates.horizontalHeaderItem(2)
        item.setText(_translate("sjUpdater", "Source Version"))
        item = self.tblUpdates.horizontalHeaderItem(3)
        item.setText(_translate("sjUpdater", "Status"))
        item = self.tblUpdates.horizontalHeaderItem(4)
        item.setText(_translate("sjUpdater", "URL"))
        __sortingEnabled = self.tblUpdates.isSortingEnabled()
        self.tblUpdates.setSortingEnabled(False)
        item = self.tblUpdates.item(0, 0)
        item.setText(_translate("sjUpdater", "App"))
        item = self.tblUpdates.item(0, 1)
        item.setText(_translate("sjUpdater", "0.9.11"))
        item = self.tblUpdates.item(0, 2)
        item.setText(_translate("sjUpdater", "0.9.11"))
        item = self.tblUpdates.item(0, 3)
        item.setText(_translate("sjUpdater", "Up to Date"))
        item = self.tblUpdates.item(1, 0)
        item.setText(_translate("sjUpdater", "Content"))
        item = self.tblUpdates.item(1, 1)
        item.setText(_translate("sjUpdater", "1.25"))
        item = self.tblUpdates.item(1, 2)
        item.setText(_translate("sjUpdater", "1.25"))
        item = self.tblUpdates.item(1, 3)
        item.setText(_translate("sjUpdater", "Up to Date"))
        item = self.tblUpdates.item(2, 0)
        item.setText(_translate("sjUpdater", "Content"))
        item = self.tblUpdates.item(2, 1)
        item.setText(_translate("sjUpdater", "1.33"))
        item = self.tblUpdates.item(2, 2)
        item.setText(_translate("sjUpdater", "1.33"))
        item = self.tblUpdates.item(2, 3)
        item.setText(_translate("sjUpdater", "Up to Date"))
        item = self.tblUpdates.item(3, 0)
        item.setText(_translate("sjUpdater", "Content"))
        item = self.tblUpdates.item(3, 1)
        item.setText(_translate("sjUpdater", "2.11"))
        item = self.tblUpdates.item(3, 2)
        item.setText(_translate("sjUpdater", "2.10"))
        item = self.tblUpdates.item(3, 3)
        item.setText(_translate("sjUpdater", "Connecting..."))
        item = self.tblUpdates.item(4, 0)
        item.setText(_translate("sjUpdater", "Content"))
        item = self.tblUpdates.item(4, 1)
        item.setText(_translate("sjUpdater", "5.22"))
        item = self.tblUpdates.item(4, 2)
        item.setText(_translate("sjUpdater", "5.20"))
        item = self.tblUpdates.item(4, 3)
        item.setText(_translate("sjUpdater", "Queued"))
        self.tblUpdates.setSortingEnabled(__sortingEnabled)
        self.btnUpdateRun.setToolTip(_translate("sjUpdater", "Update all components now"))
        self.btnUpdateRun.setText(_translate("sjUpdater", "Update All"))
        self.btnPause.setToolTip(_translate("sjUpdater", "Pause an update in progress"))
        self.btnPause.setText(_translate("sjUpdater", "Pause"))
        self.label_8.setText(_translate("sjUpdater", "Start Main Application"))
        self.chkAutoApp.setText(_translate("sjUpdater", "Auto-Launch when Update Complete"))
        self.btnOpenApp.setText(_translate("sjUpdater", "Open SQLJin"))
        self.label_4.setText(_translate("sjUpdater", "Logs"))
