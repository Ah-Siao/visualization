from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save File Example")
        self.setGeometry(100, 100, 400, 300)

        # Add a button to trigger the Save File dialog
        button = QPushButton("Save File")
        button.clicked.connect(self.save_file_dialog)

        layout = QVBoxLayout()
        layout.addWidget(button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_file_dialog(self):
        # Create a QFileDialog instance
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save File")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)  # Set the dialog mode to Save
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters(["Text Files (*.txt)", "All Files (*)"])

        # set default directory
        #file_dialog.setDirectory("absolute_path")
        # set default name 
        file_dialog.selectFile("default_name.txt")
        file_dialog.setModal(False)
        file_dialog.show()
        
        if file_dialog.exec_():  # Open the dialog and check if the user clicked OK
            file_path = file_dialog.selectedFiles()[0]  # Get the selected file path
            print(f"File to save: {file_path}")
            # Save your content to the file
            with open(file_path, 'w') as file:
                file.write("Your content here")

# Run the application
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
