import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QStackedWidget, QLabel, QSizePolicy, QListWidgetItem
)
from DBSearch import DatabaseSearchWidget
from PyQt5.QtGui import QIcon


class DatabaseWidgetA(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("A", self))
        layout.addWidget(QLabel("Search or Display for A"))
        self.setLayout(layout)


class DatabaseWidgetB(QWidget):
    def __init__(self,configs ,parent=None):
        super().__init__(parent)
        self.init_ui(configs)

    def init_ui(self,configs):
        self.configs=configs
        layout = QVBoxLayout()
        layout.addWidget(QLabel("B"))
        layout.addWidget(QLabel("Search or Display for B"))
        layout.addWidget(QLabel(f'configs:{self.configs}'))
        self.setLayout(layout)


class DatabaseWidgetC(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("C", self))
        layout.addWidget(QLabel("Search or Display for C"))
        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self,Bconfigs):
        self.Bconfigs=Bconfigs
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Database Viewer with QListWidget Navigation")
        self.setGeometry(100, 100, 1200,800)

        # Main layout
        main_layout = QHBoxLayout(self)

        # Left-side navigation with QListWidget
        self.list_widget = QListWidget()
        self.list_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Add navigation items
        self.list_widget.addItem(QListWidgetItem(QIcon('./dbpng/analysis.png'),"A"))
        self.list_widget.addItem(QListWidgetItem(QIcon('./dbpng/analysis2.png'),"B"))
        self.list_widget.addItem(QListWidgetItem(QIcon('./dbpng/mp.png'),"C"))
        self.list_widget.setCurrentRow(0)  # Default to the first widget
        self.list_widget.setStyleSheet("""
                    QListWidget {
                        background-color: #f0f0f0;
                        border:none;
                    }
                    QListWidget::item {
                        padding: 10px;
                    }
                    QListWidget::item:selected {
                        background-color: #0078d7;
                        color: white;
                    }
                """)

        main_layout.addWidget(self.list_widget)

        # Right-side stacked widget
        self.stacked_widget = QStackedWidget(self)

        # Add database widgets to the QStackedWidget
        self.db_a = DatabaseSearchWidget(db_path='test_database.db')
        self.db_b = DatabaseWidgetB(configs=self.Bconfigs)
        self.db_c = DatabaseWidgetC()

        self.stacked_widget.addWidget(self.db_a)
        self.stacked_widget.addWidget(self.db_b)
        self.stacked_widget.addWidget(self.db_c)

        main_layout.addWidget(self.stacked_widget)

        # Connect QListWidget selection to QStackedWidget
        self.list_widget.currentRowChanged.connect(self.switch_widget)

    def switch_widget(self, index):
        """Switch to the widget corresponding to the selected index."""
        self.stacked_widget.setCurrentIndex(index)


Bconfigs='testBconfig'

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow(Bconfigs='testBconfig')
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
