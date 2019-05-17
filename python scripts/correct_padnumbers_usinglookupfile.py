"""
Correct the column corresponding to the pad numbers.

Author: Gray Selby
"""
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab as py

NUMBEROFPADS = 10240
NUMBEROFTIMEBUCKETS = 517
NUMBEROFEVENTS = 74

def correct_padnumbers(lookuptable_filepath, run_filepath, corrected_filepath):
    lookup = pd.read_csv(lookuptable_filepath, usecols=[0,1,2,3,4],
        names=['CoBo','AsAd','AGET','Channel','pad_number'])
    CoBo = lookup['CoBo']
    AsAd = lookup['AsAd']
    AGET = lookup['AGET']
    Channel = lookup['Channel']
    pad_number = lookup['pad_number']

    print('Processing data...')

    #save the lookup table as a 2d numpy array called 'lookuparray'
    #Note: NOT in order based on pad number
    lookuparray = np.zeros(shape=(NUMBEROFPADS,5), dtype=int)
    #store the first 4 col of lookuplist lacking the pad number
    lookuparrayfirst4col = np.zeros(shape=(NUMBEROFPADS,4), dtype=int)
    for pad in range(NUMBEROFPADS):
        lookuparray[pad] = np.array([CoBo[pad], AsAd[pad], AGET[pad],
            Channel[pad], pad_number[pad]])

        lookuparrayfirst4col[pad] = lookuparray[pad,:4]

    #list of event names to extract data for each event from the h5 file
    events = []
    for i in range(1,75):
        events.append('get/'+str(i))

    #store h5 data in the 3d array 'dataarrayevent'
    dataarrayevent = np.zeros(shape=(NUMBEROFEVENTS,NUMBEROFPADS,NUMBEROFTIMEBUCKETS), dtype=int)
    dataarray = np.zeros(shape=(NUMBEROFPADS,NUMBEROFTIMEBUCKETS), dtype=int)
    with h5py.File(run_filepath, 'r') as f:
        for i in range(NUMBEROFEVENTS):
            dset = f[events[i]]
            dataarray = np.copy(dset)
            dataarrayevent[i] = dataarray

    #store the first 4 col of each event in the 3d array 'dataarrayeventfirst4col'
    dataarrayeventfirst4col = np.zeros(shape=(NUMBEROFEVENTS,NUMBEROFPADS,4), dtype=int)
    for i in range(NUMBEROFEVENTS):
        dataarrayeventfirst4col[i] = dataarrayevent[i,:,:4]

    print('Getting correct pad numbers...')

    
    # !!! Brute force/inefficient !!!
    #for each event (denoted by i) and for each lookuparrayfirst4col pad number (denoted by j) compare the lookuparrayfirst4col
    # values against the dataarrayeventfirst4col value (event denoted by i and pad number denoted by k)
    for event in range(NUMBEROFEVENTS):
        for lookup_pad in range(NUMBEROFPADS):                 #lookuparrayfirst4col pad numbers
            for eventdata_pad in range(NUMBEROFPADS):          #dataarrayeventfirst4col pad numbers
                #if the lookup values match the dataarray values
                if(np.array_equal(lookuparrayfirst4col[lookup_pad], dataarrayeventfirst4col[event][eventdata_pad])):
                    #set the dataarrayevent pad number value as the lookuparray pad number value
                    dataarrayevent[event][eventdata_pad][4] = lookuparray[lookup_pad][4]

    print('Creating corrected run file...')

    h5 = h5py.File(corrected_filepath, 'w')
    for i in range(NUMBEROFEVENTS):
        name = 'get/'+str(i+1)
        h5.create_dataset(name, data=dataarrayevent[i])
    h5.close()

if __name__ == '__main__':
    correct_padnumbers('flatlookup.csv', 'run_0210.h5', 'corrected_run_0210.h5')
