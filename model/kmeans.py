from __future__ import print_function
import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale, normalize,StandardScaler
from collections import Counter
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt
import matplotlib.cm as cm







# #look for interpretability in the clusters.
# #ideally there is significant separation (eg standard dev from average of player set) on a subset of features
# #either use these features to define the cluster labels, or come up with own
#
# print "cluster centers:"
# print kmeans.cluster_centers_
#
# top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
# print "top features for each cluster:"
# for num, centroid in enumerate(top_centroids):
#     print "%d: %s" % (num, ", ".join(features[i] for i in centroid))


#dim reduction?
# the t-SNE dimensionality reduction algorithm?



def silhouette_analysis(X):
    range_n_clusters = [2,4,6,8,10,12,14,16,18,20]

    for n_clusters in range_n_clusters:
        # Create a subplot with 1 row and 2 columns
        # fig, (ax1, ax2) = plt.subplots(1, 2)
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(18, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        ax.set_xlim([-0.1, 1])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax.set_ylim([0, len(X) + (n_clusters + 1) * 10])

        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)

        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For n_clusters =", n_clusters,
            "The average silhouette_score is :", silhouette_avg)

        # Compute the silhouette scores for each sample

        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.spectral(float(i) / n_clusters)
            ax.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

            ax.set_title("The silhouette plot for the various clusters.")
            ax.set_xlabel("The silhouette coefficient values")
            ax.set_ylabel("Cluster label")

            # The vertical line for average silhouette score of all the values
            ax.axvline(x=silhouette_avg, color="red", linestyle="--")

            ax.set_yticks([])  # Clear the yaxis labels / ticks
            ax.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

            # 2nd Plot showing the actual clusters formed
        #     colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
        #     ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
        #         c=colors)
        #
        # # Labeling the clusters
        # centers = clusterer.cluster_centers_
        # # Draw white circles at cluster centers
        # ax2.scatter(centers[:, 0], centers[:, 1],
        #         marker='o', c="white", alpha=1, s=200)
        # #
        # # for i, c in enumerate(centers):
        # #     ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50)
        # #
        # # ax2.set_title("The visualization of the clustered data.")
        # # ax2.set_xlabel("Feature space for the 1st feature")
        # # ax2.set_ylabel("Feature space for the 2nd feature")

        plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

        plt.show()




def plot_k_sse(X, min_k, max_k):
    """Plots sse for values of k between min_k and max_k
    Args:
    - X - feature matrix
    - min_k, max_k - smallest and largest k to plot sse for
    """
    k_values = range(min_k, max_k+1)
    sse_values = []
    for k in k_values:
        clusters = k_means(X, k=k)
        sse_values.append(sse(clusters))
    plt.plot(k_values, sse_values)
    plt.xlabel('k')
    plt.ylabel('sum squared error')
    plt.show()


if __name__ == '__main__':
    #read in the aggregated/saved data into a df
    featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
    test = featurized_data[featurized_data.min_tot > 10]
    test_players = test[['player_id','display_name']]
    test.drop(['player_id','display_name','Unnamed: 0','min_tot'], inplace = True, axis = 1)
    #,'age','height','weight','season_exp','min_game'
    test.fillna(0, inplace = True)
    test = normalize(test)
    k_vals = [2,4,6,8,10,12,14,16]
    inertia_list = []
    for i in k_vals:
        KMeans_test = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
        precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
        KMeans_test.fit_transform(test)
        test_labels = KMeans_test.labels_
        test_players['cluster'] = test_labels

        s_score = silhouette_score(test, test_labels, metric='euclidean',sample_size=None)
        inertia_list.append(KMeans_test.inertia_)
        print('k_val: ',i)
        print('s_score: ',s_score)
        print('inertia: ',KMeans_test.inertia_)

    plt.plot(k_vals, inertia_list)
    plt.xlabel('k')
    plt.ylabel('sum of error')
    plt.show()
    # test_players.to_csv('~/capstone_project/data/cluster_test.csv')
