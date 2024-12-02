from PyQt5.QtWidgets import (
    QApplication, QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QScrollArea
)
from PyQt5.QtCore import Qt

class MainWindow(QDockWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main Dockable Window")
        

        container = QWidget()
        layout = QVBoxLayout(container)

        layout.addWidget(QLabel("This is a label"))
        layout.addWidget(QLineEdit("Editable text"))
        for i in range(20):
            layout.addWidget(QLabel(f'This is label{i}'))
        
        combo_box = QComboBox()
        combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        layout.addWidget(combo_box)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton("Button 1"))
        button_layout.addWidget(QPushButton("Button 2"))
        layout.addLayout(button_layout)

        container.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)


        self.setWidget(scroll_area)

        self.resize(200,200)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)

if __name__=="__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
