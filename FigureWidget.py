
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg\
    as FigureCanvas
import matplotlib.pyplot as plt


class FigureWidget(FigureCanvas):
    def __init__(self, kmeans_model):
        self.kmeans_model = kmeans_model
        self.fig = plt.figure()
        super().__init__(self.fig)

        self.ax = self.fig.add_subplot(111)
        # self.ax.scatter([1, 2, 3], [6, 4, 7])

    def update_plot(self):
        self.ax.cla()
        self.ax.scatter(
            self.kmeans_model.obs_df.x, self.kmeans_model.obs_df.y,
            alpha=0.4,
            c=[
                self.kmeans_model.color_list[i]
                for i in self.kmeans_model.cluster_series
            ]
        )
        self.ax.scatter(
            self.kmeans_model.centroid_df.x, self.kmeans_model.centroid_df.y,
            marker='P', alpha=0.8, s=150, edgecolors='k',
            c=self.kmeans_model.color_list
        )
        self.fig.canvas.draw()
