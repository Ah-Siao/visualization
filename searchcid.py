# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cid.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pubchempy import Compound


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(690, 439)


        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(420, 360, 231, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.smiles=''
        self.COPYSMILES = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.COPYSMILES.setObjectName("COPYSMILES")
        self.COPYSMILES.hide()
        self.COPYSMILES.clicked.connect(self.copy_smiles)
        self.horizontalLayout.addWidget(self.COPYSMILES)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.hide()
        self.pushButton.clicked.connect(Dialog.close)
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 321, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.horizontalLayoutWidget_2.setFont(font)
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cid_text = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.cid_text.setFont(font)
        self.cid_text.setTextFormat(QtCore.Qt.PlainText)
        self.cid_text.setObjectName("cid_text")
        self.horizontalLayout_2.addWidget(self.cid_text)
        ## Enter CID
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setToolTip("Please enter the CID number.")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        # Push button
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_2.clicked.connect(self.searchinfo)

        # Text Browser: 
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 100, 641, 231))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CID Search"))
        self.COPYSMILES.setText(_translate("Dialog", "Copy SMILES"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.cid_text.setText(_translate("Dialog", "CID:"))
        self.pushButton_2.setText(_translate("Dialog", "Search"))
    
    
    def ERROR_MSG(self):
        msg= QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please Enter Correct CID Number!")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        x = msg.exec_()
    
    def copy_smiles(self):
        clipboard=QtGui.QGuiApplication.clipboard()
        clipboard.setText(self.smiles)
        self.COPYSMILES.setToolTip('SMILES is copied!')


    def searchinfo(self):
        try:
            cidno=int(self.lineEdit.text())
            substance=Compound.from_cid(cidno)
            iupac=substance.iupac_name
            formula=substance.molecular_formula
            Mw=substance.molecular_weight
            syn=' , '.join(substance.synonyms[:5])
            xlogp=substance.xlogp
            self.smiles=substance.isomeric_smiles
            self.textBrowser.setText(f"CID: {cidno}\nSMILES: {self.smiles}\nIUPAC: {iupac}\nFormula: {formula}\nMolecular Weight: {Mw}\nSynonyms: {syn}\nxlogp: {xlogp}")
            self.textBrowser.setFont(QtGui.QFont('Arial',14))
            self.COPYSMILES.show()
            self.pushButton.show()
        except Exception as e:
            self.ERROR_MSG()






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
