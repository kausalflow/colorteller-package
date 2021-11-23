import matplotlib.pyplot as plt

import seaborn as sns

sns.set_theme()


def distance_matrix(dist_mat, colors, ax=None, threshold=10):
    """Visualize distance matrix from a matrix of distance"""

    dist_mat_annot = []
    for dist_row in dist_mat:
        dist_row_annot = []
        for dist in dist_row:
            if dist <= threshold:
                dist_row_annot.append(f"{dist:.1f}")
            else:
                dist_row_annot.append(f">{threshold:.1f}")
        dist_mat_annot.append(dist_row_annot)

    chart_kws = dict(
        vmin=0,
        vmax=threshold,
        annot=dist_mat_annot,
        fmt="",
        xticklabels=colors,
        yticklabels=colors,
        square=True,
        linewidths=0.5,
    )
    if ax is None:
        ax = sns.heatmap(dist_mat, **chart_kws)
    else:
        sns.heatmap(dist_mat, ax=ax, **chart_kws)

    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, threshold])
    cbar.set_ticklabels(["0", f">{threshold:.1f}"], va="center")

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=45)

    plt.tight_layout()

    return ax


def noticable_matrix(noti_mat, colors, ax=None):
    """Visualize noticable matrix"""

    chart_kws = dict(
        vmin=0,
        vmax=1,
        cbar=False,
        annot=noti_mat,
        fmt="",
        xticklabels=colors,
        yticklabels=colors,
        square=True,
        linewidths=0.5,
    )
    if ax is None:
        ax = sns.heatmap(noti_mat, **chart_kws)
    else:
        sns.heatmap(noti_mat, ax=ax, **chart_kws)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=45)

    plt.tight_layout()

    return ax
