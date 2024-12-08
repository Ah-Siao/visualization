from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget, QListWidget


class AutoResizeTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adjustHeight()
        self.textChanged.connect(self.adjustHeight)

    def adjustHeight(self):
        document_height = self.document().size().height()
        self.setFixedHeight(document_height + 10)


class AutoResizeListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adjustHeight()
        self.model().rowsInserted.connect(self.adjustHeight)
        self.model().rowsRemoved.connect(self.adjustHeight)

    def adjustHeight(self):
        total_height = self.sizeHintForRow(
            0) * self.count() + 2 * self.frameWidth()
        self.setFixedHeight(total_height)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.list_widget = AutoResizeListWidget()
        self.list_widget.addItems(["Item 1", "Item 2", "Item 3"])
        layout.addWidget(self.list_widget)

        self.text_edit = AutoResizeTextEdit()
        self.text_edit.setPlaceholderText("Type here...")
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.setWindowTitle("Auto Resize QListWidget Example")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
