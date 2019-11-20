from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
)
from PyQt5.QtCore import pyqtSlot


class ControlsWidget(QWidget):
    def __init__(self, kmeans_model, figure_widget, table_widget, init_window):
        super().__init__()
        self.kmeans_model = kmeans_model
        self.figure_widget = figure_widget
        self.table_widget = table_widget
        self.init_window = init_window
        self.init_ui()

    def init_ui(self):
        self.main_vbox = QVBoxLayout()
        self.setLayout(self.main_vbox)

        self.next_btn = QPushButton('Next')
        self.reset_btn = QPushButton('Reset')
        self.main_vbox.addWidget(self.next_btn)
        self.main_vbox.addWidget(self.reset_btn)

        self.main_vbox.addStretch()

        # Connecting buttons with slots
        self.next_btn.clicked.connect(self.update)
        self.reset_btn.clicked.connect(self.show_init_window)

    @pyqtSlot(int, int, str)
    def init_kmeans_model(self, num_obs, num_clusters, config):
        self.kmeans_model.init(num_obs, num_clusters, config)
        self.figure_widget.update_plot()
        self.table_widget.init()
        self.table_widget.update()

    @pyqtSlot()
    def update(self):
        self.kmeans_model.update()
        self.figure_widget.update_plot()
        self.table_widget.update()

    @pyqtSlot()
    def show_init_window(self):
        self.init_window.show()
