from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton,
    QGridLayout, QWidget, QVBoxLayout, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class InitWindow(QMainWindow):
    '''
    Takes the number of observations, number of clusters
    and config (name of preset data)
    '''
    init_kmeans_model_signal = pyqtSignal(int, int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 300)
        self.setWindowTitle('Kmeans initialization')

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_vbox = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_vbox)

        self.params_grid = QGridLayout()
        self.main_vbox.addLayout(self.params_grid)

        self.num_obs_label = QLabel('Number of observations')
        self.num_obs_lineEdit = QLineEdit()
        self.num_clusters_label = QLabel('Number of clusters')
        self.num_clusters_lineEdit = QLineEdit()
        self.config_label = QLabel('Data')
        self.config_comboBox = QComboBox(self.main_widget)
        self.config_comboBox.addItem('3 clusters')
        self.config_comboBox.addItem('random')
        self.config_comboBox.addItem('squiggly cross')

        self.params_grid.addWidget(self.num_obs_label, 0, 0)
        self.params_grid.addWidget(self.num_obs_lineEdit, 0, 1)
        self.params_grid.addWidget(self.num_clusters_label, 1, 0)
        self.params_grid.addWidget(self.num_clusters_lineEdit, 1, 1)
        self.params_grid.addWidget(self.config_label, 2, 0)
        self.params_grid.addWidget(self.config_comboBox, 2, 1)

        self.bottom_hbox = QHBoxLayout(self.main_widget)
        self.main_vbox.addLayout(self.bottom_hbox)

        self.start_btn = QPushButton('Start', self.main_widget)
        self.cancel_btn = QPushButton('Cancel', self.main_widget)
        self.bottom_hbox.addWidget(self.start_btn)
        self.bottom_hbox.addWidget(self.cancel_btn)

        self.start_btn.clicked.connect(self.emit_init_kmeans_model_signal)
        self.cancel_btn.clicked.connect(self.close)

    @pyqtSlot()
    def emit_init_kmeans_model_signal(self):
        num_obs = int(self.num_obs_lineEdit.text())
        num_clusters = int(self.num_clusters_lineEdit.text())
        self.init_kmeans_model_signal.emit(
            num_obs, num_clusters, self.config_comboBox.currentText()
        )
        self.close()
