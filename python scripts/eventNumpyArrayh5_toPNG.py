"""
This file takes event numpy arrays and saves them as .png files.

Author: Gray Selby
"""

import matplotlib
import numpy as np
import pytpc
import matplotlib.pyplot as plt
import h5py

def eventarrays_to_png(image_data_filepath, png_filepath_dont_include_png):

    with h5py.File(image_data_filepath,'r') as f:
        images = f['images'][:]

    for i, image in enumerate(images):
        plt.imshow(image)
        plt.savefig(png_filepath_dont_include_png+str(i+1)+'.png', format='PNG')

if __name__ == '__main__':
    #example:
    #eventarrays_to_png('new_hit_method_thresh50_images.h5',
    #    '/home/selby/attpc-alpha-alpha/newMethodThresh50/eventthresh50')
