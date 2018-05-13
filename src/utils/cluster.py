import os

src_folder = 'D:\\PycharmProjects\\manhattan_test_data\\warehouse_test\\StrawberryYogurt'

def get_clusters_by_name(fn_list, n_char):
    clusters = {}
    for fn in fn_list:
        fn = fn[0:n_char-1]
        if not fn in clusters.keys():
            clusters[fn] = []
        clusters[fn].append(fn)
    return clusters
    

for (dirpath,_,filenames) in os.walk(src_folder):

    image_filenames = []

    for filename in filenames:
        if filename.lower().endswith('.jpg'):
            image_filenames.append(filename)

    clusters = get_clusters_by_name(image_filenames, 37)
    cluster_length = 0
    for cluster in clusters:
        cluster_length += len(clusters[cluster])

    cluster_length = cluster_length/len(clusters.keys())

    print('Number of clusters: {}'.format( len(clusters.keys()) ))
    print('Avg length of of clusters: {}'.format(cluster_length))



