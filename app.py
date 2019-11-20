import sys
from PyQt5.QtWidgets import QApplication
from KmeansWindow import KmeansWindow
from PyQt5 import QtWidgets

app = QApplication(sys.argv)
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
kmeans_window = KmeansWindow()

sys.exit(app.exec_())
