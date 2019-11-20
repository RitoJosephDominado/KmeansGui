from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
import pandas as pd
from PyQt5 import QtWidgets as qtw


class TableWidget(QTableWidget):
    def __init__(self, kmeans_model):
        super().__init__(1, 1)
        self.kmeans_model = kmeans_model
        self.setSizeAdjustPolicy(
            qtw.QAbstractScrollArea.AdjustToContents
        )

    def fix_size(self):
        num_rows = self.kmeans_model.num_obs
        num_columns = self.kmeans_model.num_clusters + 2
        self.setRowCount(num_rows)
        self.setColumnCount(num_columns)

    def init(self):
        self.fix_size()
        centroid_coords = zip(
            round(self.kmeans_model.centroid_df.x, 2),
            round(self.kmeans_model.centroid_df.y, 2)
        )
        centroid_items = [QTableWidgetItem(str(x)) for x in centroid_coords]
        centroid_colors = [QColor(*tuple(x * 255 for x in color_tuple))
                           for color_tuple in self.kmeans_model.color_list]

        self.setHorizontalHeaderLabels(['x', 'y'])

        for i in range(len(centroid_items)):
            centroid_items[i].setBackground(centroid_colors[i])
            self.setHorizontalHeaderItem(i + 2, centroid_items[i])

    def update(self):
        centroid_coords = list(zip(
            round(self.kmeans_model.centroid_df.x, 2),
            round(self.kmeans_model.centroid_df.y, 2)
        ))

        # centroid_items = [QTableWidgetItem(str(x)) for x in centroid_coords]
        # centroid_colors = [QColor(*tuple(x * 255 for x in color_tuple))
        #                    for color_tuple in self.kmeans_model.color_list]

        for i in range(len(centroid_coords)):
            self.horizontalHeaderItem(i + 2).setText(str(centroid_coords[i]))

        full_df = pd.concat(
            [self.kmeans_model.obs_df, self.kmeans_model.dist_df], axis=1
        )

        for row in range(full_df.shape[0]):
            for column in range(full_df.shape[1]):
                val = str(round(full_df.iloc[row, column], 2))
                item = QTableWidgetItem(val)
                self.setItem(row, column, item)

        obs_colors = [
            self.kmeans_model.color_list[i]
            for i in self.kmeans_model.cluster_series
        ]

        obs_colors2 = [
            tuple(color_tuple * 255 for color_tuple in x)
            for x in obs_colors
        ]

        obs_colors3 = [QColor(*i) for i in obs_colors2]

        for row in range(full_df.shape[0]):
            self.item(row, 0).setBackground(obs_colors3[row])
            self.item(row, 1).setBackground(obs_colors3[row])
