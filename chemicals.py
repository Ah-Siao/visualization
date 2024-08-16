# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# You can try example 2-Benzoylmalononitrile: C1=CC=C(C=C1)C(=O)C(C#N)C#N or 1H-indene-1-carboxylic acid: C1=CC=C2C(C=CC2=C1)C(=O)O



from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from rdkit import Chem
from rdkit.Chem import AllChem, Draw, Descriptors, rdMolDescriptors
import py3Dmol
import sys
from searchcid import Ui_Dialog as SearchCIDUI



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 712)
        MainWindow.setWindowTitle("Chemical Visualization Tool")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Add menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.SearchSMILES=QtWidgets.QMenu(self.menubar)
        self.SearchSMILES.setObjectName("SearchSMILES")
        self.SearchSMILES.setTitle("Search")

        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.CIDSearch = QtWidgets.QAction(MainWindow)
        self.CIDSearch.setObjectName("CIDSearch")
        self.CIDSearch.setText("CIDSearch")

        self.SearchSMILES.addAction(self.CIDSearch)

        self.menubar.addAction(self.SearchSMILES.menuAction())

        self.CIDSearch.triggered.connect(self.SearchCID)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # SMILES label
        self.label_SMILES = QtWidgets.QLabel(self.centralwidget)
        self.label_SMILES.setGeometry(QtCore.QRect(50, 40, 80, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_SMILES.setFont(font)
        self.label_SMILES.setObjectName("label_SMILES")

        # smiles input:lineEdit
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(150, 40, 280, 41))
        self.lineEdit.setToolTip("Enter a SMILES string representing a molecule.")
        font = QtGui.QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")


        # Button for visualization
        self.Button = QtWidgets.QPushButton(self.centralwidget)
        self.Button.setGeometry(QtCore.QRect(590, 40, 150, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily('Alegreya')
        self.Button.setFont(font)
        self.Button.setObjectName("Button")
        self.Button.clicked.connect(self.visualize)

        # Label for explaination
        self.explain=QtWidgets.QLabel(self.centralwidget)
        self.explain.setText("e.g. For 2-Benzoylmalononitrile, you have to type in : C1=CC=C(C=C1)C(=O)C(C#N)C#N")
        self.explain.setGeometry(QtCore.QRect(QtCore.QRect(50, 80, 500, 35)))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setFamily('Arial')
        self.explain.setFont(font)
        self.explain.setObjectName("Explain")
        


        # visualize_region to show the stuff

        self.visualize_region = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.visualize_region.setGeometry(QtCore.QRect(50, 200, 500, 500))
        self.visualize_region.setObjectName("visualize_region")

        # Create checkboxes: 'line', 'stick', 'sphere',"cross"
        self.hbox=QtWidgets.QWidget(self.centralwidget)
        self.hbox.setGeometry(50,100,500,100)
        self.h_layout=QtWidgets.QHBoxLayout(self.hbox)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily('Arial')
        self.hbox.setFont(font)

        self.check1=QtWidgets.QCheckBox(self.centralwidget)
        self.check1.setText("line")
        self.check1.setAutoExclusive(True)
        self.check1.setObjectName("line")
        self.h_layout.addWidget(self.check1)
        

        self.check2=QtWidgets.QCheckBox(self.centralwidget)
        self.check2.setText("stick")
        self.check2.setAutoExclusive(True)
        self.check2.setObjectName("stick")
        self.h_layout.addWidget(self.check2)

        self.check3=QtWidgets.QCheckBox(self.centralwidget)
        self.check3.setText("sphere")
        self.check3.setAutoExclusive(True)
        self.check3.setObjectName("sphere")
        self.h_layout.addWidget(self.check3)
        self.check3.setChecked(True)

        self.check4=QtWidgets.QCheckBox(self.centralwidget)
        self.check4.setText("cross")
        self.check4.setAutoExclusive(True)
        self.check4.setObjectName("cross")
        self.h_layout.addWidget(self.check4)


        # Label for 2D images        
        self.label2=QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(600,160,220,40))
        self.label2.setText("2D Image")
        self.label2.setObjectName('label2')
        self.label2.setFont(QtGui.QFont('Arial',12))

        # 2D images
        self.tiny2D = QtWidgets.QLabel(self.centralwidget)
        self.tiny2D.setGeometry(QtCore.QRect(600, 210, 220, 220))
        #self.tiny2D.setPixmap(QtGui.QPixmap('none'))
        self.tiny2D.setStyleSheet("background-color:white")
        self.tiny2D.setScaledContents(True)
        self.tiny2D.setObjectName("tiny2D")

        #Label explain the Image
        self.labelC=QtWidgets.QLabel(self.centralwidget)
        self.labelC.setGeometry(QtCore.QRect(600,435,200,20))
        self.labelC.setText("Gasteiger Charge")
        self.labelC.setObjectName('tinyC2D')
        self.labelC.setFont(QtGui.QFont('Arial',12))

        # 2D images with Gasteiger Charge
        self.tinyC2D=QtWidgets.QLabel(self.centralwidget)
        self.tinyC2D.setGeometry(QtCore.QRect(600,460,220,220))
        self.tinyC2D.setStyleSheet("background-color:white")
        self.tinyC2D.setScaledContents(True)
        self.tinyC2D.setObjectName("tinyC2D")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chemical Visualization Tool"))
        self.label_SMILES.setText(_translate("MainWindow", "SMILES"))
        self.Button.setText(_translate("MainWindow", "Visualize"))

        self.check1.setText(_translate("MainWindow", "line"))
        self.check2.setText(_translate("MainWindow", "stick"))
        self.check3.setText(_translate("MainWindow", "sphere"))
        self.check4.setText(_translate("MainWindow", "cross"))

        self.SearchSMILES.setTitle(_translate("MainWindow", "Search SMILES"))
        self.CIDSearch.setText(_translate("MainWindow", "CIDSearch"))
    
    def SearchCID(self):
        self.Dialog = QtWidgets.QDialog()
        self.cid=SearchCIDUI()
        self.cid.setupUi(self.Dialog)
        self.Dialog.show()




    def MolTo3DView(self, mol, size=(300, 300), style="stick", surface=False, opacity=0.5):
        """Draw molecule in 3D"""
        assert style in ('line', 'stick', 'sphere',"cross")
        mblock = Chem.MolToMolBlock(mol)
        viewer = py3Dmol.view(width=size[0], height=size[1])
        viewer.addModel(mblock, 'mol')
        viewer.setStyle({style: {}})
        if surface:
            viewer.addSurface(py3Dmol.SAS, {'opacity': opacity})
        viewer.zoomTo()
        return viewer
    
    def MolTo2DImg(self,mol):
        dos = Draw.MolDrawOptions()
        dos.addAtomIndices=True
        dos.addStereoAnnotation = True
        img=Draw.MolToImage(mol, options= dos)
        img.save('2D_Structure.png')
    
    def MolTo2DCharge(self,mol):
        AllChem.ComputeGasteigerCharges(mol)
        mol2=Chem.Mol(mol)
        for at in mol2.GetAtoms():
            lbl = '%.2f'%(at.GetDoubleProp("_GasteigerCharge"))
            at.SetProp('atomNote',lbl)
        img=Draw.MolToImage(mol2)
        img.save("2DMolCharge.png")

    def smi2conf(self, mol):
        '''Convert SMILES to rdkit.Mol with 3D coordinates'''
        if mol is not None:
            mol = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol)
            AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
            return mol
        else:
            return None
    
    def appearance(self):
        if self.check1.checkState()==2:
            return 'line'
        elif self.check2.checkState()==2:
            return 'stick'
        elif self.check4.checkState()==2:
            return 'cross'
        else:
            return 'sphere'
    
    def SMILES_ERROR(self):
        msg= QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please Enter Correct SMILES String !!!")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        x = msg.exec_()


    def visualize(self):
        SMILES = self.lineEdit.text()
        SMILES=SMILES.upper()
        try:
            mol = Chem.MolFromSmiles(SMILES)
            if mol is None:
                raise ValueError("Invalid SMILES string")
            conf = self.smi2conf(mol)
            if conf is None:
                raise ValueError("Failed to generate 3D conformer")
            style=self.appearance()
            viewer = self.MolTo3DView(conf, size=(500, 400), style=style)
            html = viewer._make_html()
            self.visualize_region.setHtml(html)
            self.MolTo2DImg(mol)
            self.tiny2D.setPixmap(QtGui.QPixmap('2D_Structure.png'))
            self.MolTo2DCharge(mol)
            self.tinyC2D.setPixmap(QtGui.QPixmap("2DMolCharge.png"))
            #Calculate average molecular weight
            Mw=round(Descriptors.MolWt(mol),4)
            formula=rdMolDescriptors.CalcMolFormula(mol)
            self.label2.setText(f"Formula: {formula}\nMw: {Mw} g/mol")
        except Exception as e:
            self.SMILES_ERROR()
            self.label2.setText(f"Error: {str(e)}")
            self.tiny2D.clear()
            self.tinyC2D.clear()
            self.visualize_region.setHtml("")
    
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
