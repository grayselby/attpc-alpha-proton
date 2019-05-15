# Python Scripts

## correct_padnumbers_usinglookupfile.py
### This python script contains the function correct_padnumbers which takes as parameters a look up table file path, experiment run file path, and a corrected h5 file path. This was created because an error occurred while recording data from the 22Mg(alpha,proton) experiment where the original h5 run files did not include pad numbers. This file uses the experiments look up file to correct the h5 run file with the needed pad numbers.

## eventsToNumpyArrayh5.py
### This python script contains the function real_unlabeled_events which takes as parameters the desired projection (z0y or xy), a save file path, and prefix (file name). This was created to store event data in numpy arrays of the correct size as well as normalize charge represented by grey scale color in the images.

## embed_numpyArrayh5.py
### This python script contains the function imbed_image_data which takes as parameters an the h5 created by eventsToNumpyArrayh5, the number of events, the desired number of dimensions for the .tsv file, and the .tsv file path. This was created for use in TensorFlow's imbedding projector for feature clustering.

## eventNumpyArrayh5_toPNG.py
### This python script contains the function eventarrays_to_png which takes as parameters the h5 created by eventsToNumpyArrayh5 and the PNG file path without .png. This was created to save the grey scale plots of the event images.
