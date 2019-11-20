from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout
)
from InitWindow import InitWindow
from ControlsWidget import ControlsWidget
from FigureWidget import FigureWidget
from TableWidget import TableWidget
from KmeansModel import KmeansModel


class KmeansWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kmeans_model = KmeansModel()
        self.figure_widget = FigureWidget(self.kmeans_model)
        self.table_widget = TableWidget(self.kmeans_model)
        self.init_window = InitWindow(self)
        self.controls_widget = ControlsWidget(
            self.kmeans_model, self.figure_widget,
            self.table_widget, self.init_window
        )
        self.init_ui()

        self.init_window.init_kmeans_model_signal.connect(
            self.controls_widget.init_kmeans_model
        )

        # Showing windows
        self.showMaximized()
        self.init_window.show()

    def init_ui(self):
        'Setting up the layout of the main window'
        self.setWindowTitle('KmeansGui')
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_hbox = QHBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_hbox)

        self.main_hbox.addWidget(self.controls_widget, 10)
        self.main_hbox.addWidget(self.figure_widget, 50)
        self.main_hbox.addWidget(self.table_widget, 40)
