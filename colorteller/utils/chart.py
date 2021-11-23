import matplotlib.pyplot as plt

import seaborn as sns; sns.set_theme()


def distance_matrix(dist_mat, ax=None):
    """Visualize distance matrix from a matrix of distance
    """
    if ax is None:
        ax = sns.heatmap(dist_mat)
    else:
        sns.heatmap(dist_mat, ax=ax)

    return ax


def noticable_matrix(noti_mat, ax=None):
    """Visualize noticable matrix
    """
    if ax is None:
        ax = sns.heatmap(noti_mat, vmin=0, vmax=1)
    else:
        sns.heatmap(noti_mat, ax=ax, vmin=0, vmax=1)

    return ax