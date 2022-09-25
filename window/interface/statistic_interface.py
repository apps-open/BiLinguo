# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statistic_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200, 213)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tests_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.tests_label_2.setObjectName("tests_label_2")
        self.verticalLayout.addWidget(self.tests_label_2)
        self.total_pts_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.total_pts_label_2.setObjectName("total_pts_label_2")
        self.verticalLayout.addWidget(self.total_pts_label_2)
        self.avg_accuracy_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.avg_accuracy_label_2.setObjectName("avg_accuracy_label_2")
        self.verticalLayout.addWidget(self.avg_accuracy_label_2)
        self.total_words_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.total_words_label_2.setObjectName("total_words_label_2")
        self.verticalLayout.addWidget(self.total_words_label_2)
        self.learned_words_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.learned_words_label_2.setObjectName("learned_words_label_2")
        self.verticalLayout.addWidget(self.learned_words_label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.total_pts_label = QtWidgets.QLabel(self.centralwidget)
        self.total_pts_label.setObjectName("total_pts_label")
        self.verticalLayout_2.addWidget(self.total_pts_label)
        self.tests_label = QtWidgets.QLabel(self.centralwidget)
        self.tests_label.setObjectName("tests_label")
        self.verticalLayout_2.addWidget(self.tests_label)
        self.avg_accuracy_label = QtWidgets.QLabel(self.centralwidget)
        self.avg_accuracy_label.setObjectName("avg_accuracy_label")
        self.verticalLayout_2.addWidget(self.avg_accuracy_label)
        self.total_words_label = QtWidgets.QLabel(self.centralwidget)
        self.total_words_label.setObjectName("total_words_label")
        self.verticalLayout_2.addWidget(self.total_words_label)
        self.learned_words_label = QtWidgets.QLabel(self.centralwidget)
        self.learned_words_label.setObjectName("learned_words_label")
        self.verticalLayout_2.addWidget(self.learned_words_label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.export_button = QtWidgets.QPushButton(self.centralwidget)
        self.export_button.setStyleSheet("*{image: url(:/share_icon/icons8-upload-24.png);\n"
"background: #424242;\n"
"border-radius: 5px;\n"
"border: 0px solid;\n"
"height: 32px;}\n"
"*:hover {\n"
"     height: 32px;\n"
"      border: 1px solid white;\n"
"      background: #626262;\n"
"}")
        self.export_button.setText("")
        self.export_button.setObjectName("export_button")
        self.verticalLayout_3.addWidget(self.export_button)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Statistic"))
        self.label.setText(_translate("MainWindow", "Statistic"))
        self.tests_label_2.setText(_translate("MainWindow", "Tests:"))
        self.total_pts_label_2.setText(_translate("MainWindow", "Total points: "))
        self.avg_accuracy_label_2.setText(_translate("MainWindow", "Average accuracy: "))
        self.total_words_label_2.setText(_translate("MainWindow", "Total words: "))
        self.learned_words_label_2.setText(_translate("MainWindow", "Learned words: "))
        self.total_pts_label.setText(_translate("MainWindow", "0"))
        self.tests_label.setText(_translate("MainWindow", "0"))
        self.avg_accuracy_label.setText(_translate("MainWindow", "0.00%"))
        self.total_words_label.setText(_translate("MainWindow", "0"))
        self.learned_words_label.setText(_translate("MainWindow", "0/0"))
import window.interface.resource.src_rc
