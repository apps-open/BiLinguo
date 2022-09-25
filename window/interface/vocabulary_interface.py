# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vocabulary_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 495)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.info_button = QtWidgets.QPushButton(self.centralwidget)
        self.info_button.setStyleSheet("image: url(:/info_button/icons8-help-24.png);")
        self.info_button.setText("")
        self.info_button.setObjectName("info_button")
        self.horizontalLayout_5.addWidget(self.info_button)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.search_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_edit.setObjectName("search_edit")
        self.horizontalLayout_3.addWidget(self.search_edit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(sizePolicy)
        self.search_button.setStyleSheet("image: url(:/enter_icon/icons8-next-page-24.png);")
        self.search_button.setText("")
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_2.addWidget(self.search_button)
        self.clear_search = QtWidgets.QPushButton(self.centralwidget)
        self.clear_search.setStyleSheet("image: url(:/close_icon/icons8-close-24.png);")
        self.clear_search.setText("")
        self.clear_search.setObjectName("clear_search")
        self.horizontalLayout_2.addWidget(self.clear_search)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_word_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_word_button.setAutoFillBackground(False)
        self.add_word_button.setStyleSheet("image:url(:/add_icon/icons8-add-24.png)")
        self.add_word_button.setText("")
        self.add_word_button.setObjectName("add_word_button")
        self.horizontalLayout.addWidget(self.add_word_button)
        self.delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_button.setStyleSheet("image: url(:/delete_icon/icons8-remove-24.png);")
        self.delete_button.setText("")
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.translate_button = QtWidgets.QPushButton(self.centralwidget)
        self.translate_button.setStyleSheet("image: url(:/translate_icon/icons8-translate-24.png);")
        self.translate_button.setText("")
        self.translate_button.setObjectName("translate_button")
        self.horizontalLayout.addWidget(self.translate_button)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setStyleSheet("image: url(:/save_icon/icons8-save-24.png);")
        self.save_button.setText("")
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.test_button = QtWidgets.QPushButton(self.centralwidget)
        self.test_button.setStyleSheet("image: url(:/test_icon/icons8-pass-fail-24.png);")
        self.test_button.setText("")
        self.test_button.setObjectName("test_button")
        self.horizontalLayout.addWidget(self.test_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.vocabulary_table = QtWidgets.QTableWidget(self.centralwidget)
        self.vocabulary_table.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.vocabulary_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.vocabulary_table.setObjectName("vocabulary_table")
        self.vocabulary_table.setColumnCount(3)
        self.vocabulary_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.vocabulary_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.vocabulary_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.vocabulary_table.setHorizontalHeaderItem(2, item)
        self.vocabulary_table.horizontalHeader().setCascadingSectionResizes(False)
        self.vocabulary_table.horizontalHeader().setStretchLastSection(False)
        self.vocabulary_table.verticalHeader().setSortIndicatorShown(False)
        self.vocabulary_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.vocabulary_table)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.load_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_button.setStyleSheet("image: url(:/load_icon/icons8-download-24.png)")
        self.load_button.setText("")
        self.load_button.setObjectName("load_button")
        self.horizontalLayout_4.addWidget(self.load_button)
        self.close_button = QtWidgets.QPushButton(self.centralwidget)
        self.close_button.setStyleSheet("image: url(:/close_icon/icons8-close-24.png)")
        self.close_button.setText("")
        self.close_button.setObjectName("close_button")
        self.horizontalLayout_4.addWidget(self.close_button)
        self.create_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_button.setToolTipDuration(5)
        self.create_button.setStyleSheet("image: url(:/edit_icon/icons8-edit-24.png);")
        self.create_button.setText("")
        self.create_button.setObjectName("create_button")
        self.horizontalLayout_4.addWidget(self.create_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vocabulary"))
        self.search_edit.setPlaceholderText(_translate("MainWindow", "Enter any text to search in vocabuary..."))
        self.vocabulary_table.setSortingEnabled(True)
        item = self.vocabulary_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Word"))
        item = self.vocabulary_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Translation"))
        item = self.vocabulary_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Notes"))
        self.create_button.setToolTip(_translate("MainWindow", "Create table"))
import window.interface.resource.src_rc
