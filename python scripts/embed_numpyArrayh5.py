"""
Imbed event numpy arrays for unsupervised learning. This script uses VGG16
pretrained layers with imagenet. It imbeds features and brings the
dimensionality down to a specified number. 50 dimensions is suggested.

Author: Gray Selby
"""

import tensorflow as tf
import numpy as np
import os
import h5py
from sklearn.decomposition import PCA

vgg = tf.keras.applications.VGG16(include_top = False, weights = 'imagenet')

def imbed_image_data(image_data_filepath, number_of_events,
    desired_num_dimensions, imbedded_filepath):

    with h5py.File(image_data_filepath, 'r') as image_array:
        images = image_array['images'][:]

    features = vgg.predict(images)

    features = features.reshape((number_of_events, -1))

    pca = PCA(n_components=desired_num_dimensions)
    features = pca.fit_transform(features)

    with open(imbedded_filepath, 'w') as imbedded:
        for data in features:
            data = [str(x) for x in data]
            imbedded.write('\t'.join(data) + '\n')

if __name__ == '__main__':
    #example:
    #imbed_image_data('new_hit_method_thresh50_images.h5', 74, 50,
    #    'new_hit_method_thresh50_embedded.tsv')
