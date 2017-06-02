# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bubbly_pom/note_form.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.note_title = QtWidgets.QLineEdit(Dialog)
        self.note_title.setObjectName("note_title")
        self.verticalLayout.addWidget(self.note_title)
        self.note_body = QtWidgets.QTextEdit(Dialog)
        self.note_body.setDocumentTitle("")
        self.note_body.setObjectName("note_body")
        self.verticalLayout.addWidget(self.note_body)
        self.save_note_btn = QtWidgets.QPushButton(Dialog)
        self.save_note_btn.setObjectName("save_note_btn")
        self.verticalLayout.addWidget(self.save_note_btn)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Note/Idea"))
        self.note_title.setPlaceholderText(_translate("Dialog", "Title"))
        self.note_body.setPlaceholderText(_translate("Dialog", "Content..."))
        self.save_note_btn.setText(_translate("Dialog", "Save"))

