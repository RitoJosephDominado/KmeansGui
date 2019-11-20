import KmeansFunctions as kf


class KmeansModel:
    def __init__(self):
        pass

    def init(self, num_obs, num_clusters, config):
        self.step = 0
        self.num_obs = num_obs
        self.num_clusters = num_clusters
        self.config = config
        self.obs_df = kf.init_obs_df(self.num_obs, self.config)
        self.centroid_df = kf.init_centroid_df(self.num_clusters)
        self.dist_df = kf.calc_dist_df(self.obs_df, self.centroid_df)
        self.cluster_series = kf.calc_cluster_series(dist_df=self.dist_df)
        self.color_list = kf.get_color_list(self.num_clusters)

    def update(self):
        self.step += 1
        self.centroid_df = kf.calc_centroid_df(
            self.obs_df, self.cluster_series, self.num_clusters
        )
        self.dist_df = kf.calc_dist_df(self.obs_df, self.centroid_df)
        self.cluster_series = kf.calc_cluster_series(dist_df=self.dist_df)

    def init_obs_df(self):
        pass

    def init_centroid_df(self):
        pass
