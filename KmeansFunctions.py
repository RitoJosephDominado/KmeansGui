import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_color_list(num_clusters):
    min_len = num_clusters // 3
    rem = num_clusters % 3
    splits = []
    for i in range(3):
        splits.append(min_len)

    for i in range(rem):
        splits[i] += 1

    ind1 = np.arange(0, splits[0])
    ind2 = np.arange(splits[0], splits[0] + splits[1])
    ind3 = np.arange(splits[0] + splits[1], num_clusters)

    red_vals = np.zeros(num_clusters)
    blue_vals = np.zeros(num_clusters)
    green_vals = np.zeros(num_clusters)

    red_vals[ind1] = np.linspace(1, 0.5, splits[0])
    red_vals[ind2] = np.linspace(0.5, 0, splits[1] + 1)[1:]
    red_vals[ind3] = np.linspace(0, 0.5, splits[2] + 1)[1:]

    blue_vals[ind1] = np.linspace(0, 0.5, splits[0])
    blue_vals[ind2] = np.linspace(0.5, 1, splits[1] + 1)[1:]
    blue_vals[ind3] = np.linspace(1, 0.5, splits[2] + 1)[1:]

    green_vals[ind1] = np.linspace(0.5, 1, splits[0])
    green_vals[ind2] = np.linspace(1, 0.5, splits[1] + 1)[1:]
    green_vals[ind3] = np.linspace(0.5, 0, splits[2] + 1)[1:]

    color_list = [
        (red_vals[i], blue_vals[i], green_vals[i])
        for i in range(num_clusters)
    ]
    return(color_list)


def create_scale_func(lim):
    def scale_func(a):
        b = a * (lim[1] - lim[0])/100 + lim[0]
        return(b)

    return(scale_func)


def init_obs_df(num_obs=50, config='3 clusters', xlim=[0, 100], ylim=[0, 100]):
    '''
    Creates a data frame with an x and y column,
    and a few possible preset configs
    '''
    translate_x = create_scale_func(xlim)
    translate_y = create_scale_func(ylim)

    if config == '3 clusters':
        clust1_num_obs = np.floor_divide(num_obs, 3)
        clust2_num_obs = np.floor_divide(num_obs, 3)
        clust3_num_obs = num_obs - clust1_num_obs - clust2_num_obs
        clust1 = pd.DataFrame({
            'x': np.random.normal(
                translate_x(30), translate_x(10) - xlim[0], clust1_num_obs
            ),
            'y': np.random.normal(
                translate_y(30), translate_y(10) - ylim[0], clust1_num_obs
            )
        })

        clust2 = pd.DataFrame({
            'x': np.random.normal(
                translate_x(70), translate_x(10) - xlim[0], clust2_num_obs
            ),
            'y': np.random.normal(
                translate_y(30), translate_y(10) - ylim[0], clust2_num_obs
            )
        })

        clust3 = pd.DataFrame({
            'x': np.random.normal(
                translate_x(50), translate_x(10) - xlim[0], clust3_num_obs
            ),
            'y': np.random.normal(
                translate_y(70), translate_y(10) - ylim[0], clust3_num_obs
            )
        })

        obs_df = pd.concat([clust1, clust2, clust3])
        obs_df = obs_df.reset_index(drop=True)

    elif config == 'random':
        obs_df = pd.DataFrame({
            'x': np.random.normal(
                translate_x(50),
                translate_x(10) - xlim[0], num_obs
            ),
            'y': np.random.normal(
                translate_y(50),
                translate_y(10) - ylim[0], num_obs
            )
        })

    elif config == 'squiggly cross':
        x1 = np.linspace(0.1, 0.9, int(num_obs/2))
        y1 = np.sin(6 * np.pi * x1)/22 + 0.5
        x2 = np.concatenate((x1, y1))
        y2 = np.concatenate((y1, x1))
        x3 = x2 * (xlim[1] - xlim[0]) + xlim[0]
        y3 = y2 * (ylim[1] - ylim[0]) + ylim[0]

        x_rand_range = int((xlim[1] - xlim[0])/20)
        y_rand_range = int((ylim[1] - ylim[0])/20)

        x4 = x3 + np.random.randint(-x_rand_range, x_rand_range, num_obs)
        y4 = y3 + np.random.randint(-y_rand_range, y_rand_range, num_obs)
        obs_df = pd.DataFrame({
            'x': x4, 'y': y4
        })

    return(obs_df)


def init_centroid_df(num_clusters, xlim=[0, 100], ylim=[0, 100]):
    '''
    Creates a set of centroids given a set of observations.
    Takes the min and max x and y to get the bounds
    '''
    centroid_df = pd.DataFrame({
        'x': np.random.uniform(xlim[0], xlim[1], num_clusters),
        'y': np.random.uniform(ylim[0], ylim[1], num_clusters)
    })

    return(centroid_df)


def calc_dist_df(obs_df, centroid_df):
    'Calculates the distances between each observation and each centroid'
    num_clusters = len(centroid_df.x)
    num_obs = len(obs_df.x)
    dist_df = pd.DataFrame(
        np.zeros((num_obs, num_clusters)),
        columns=centroid_df.index
    )

    for i in centroid_df.index:
        x_diff = centroid_df.loc[i, 'x'] - obs_df['x']
        y_diff = centroid_df.loc[i, 'y'] - obs_df['y']
        dist_df.loc[:, i] = np.sqrt(x_diff**2 + y_diff**2)

    return(dist_df)


def calc_cluster_series(obs_df=None, centroid_df=None, dist_df=None):
    if(dist_df is None):
        dist_df = calc_dist_df(obs_df, centroid_df)

    cluster_series = dist_df.idxmin(axis=1)
    return(cluster_series)


# def calc_centroid_df(obs_df, cluster_series):
#    'Gets the mean of each cluster and returns these as the new centroids'
#    cluster_indices = cluster_series.unique()
#    centroid_df = pd.DataFrame(columns=['x', 'y'])
#
#    for i in cluster_indices:
#        centroid_df.loc[i, 'x'] = np.mean(obs_df[cluster_series == i].x)
#        centroid_df.loc[i, 'y'] = np.mean(obs_df[cluster_series == i].y)
#
#    return(centroid_df)

def calc_centroid_df(obs_df, cluster_series, num_clusters):
    'Gets the mean of each cluster\'s x and y coordinates to get the new\
        centroids'
    centroid_df = pd.DataFrame(np.zeros((num_clusters, 2)))
    centroid_df.columns = ['x', 'y']

    for i in range(num_clusters):
        centroid_df.loc[i, 'x'] = np.mean(obs_df[cluster_series == i].x)
        centroid_df.loc[i, 'y'] = np.mean(obs_df[cluster_series == i].y)

    return(centroid_df)


def plot_kmeans_state(
        obs_df, centroid_df,
        cluster_series, color_list, xlim=None, ylim=None):

    plt.scatter(
        obs_df.x, obs_df.y,
        alpha=0.4,
        c=[color_list[i] for i in cluster_series]
    )

    plt.scatter(
        centroid_df.x, centroid_df.y,
        marker='P', alpha=0.8, s=150, edgecolors='k',
        c=color_list
    )
    if(xlim is not None):
        plt.xlim(xlim)

    if(ylim is not None):
        plt.ylim(ylim)
