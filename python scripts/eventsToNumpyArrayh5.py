"""
Generate images of ATTPC events for CNN.

Author: Gray Selby
"""
import math
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
import os
import pytpc
from random import shuffle

def _average(lst):
    return sum(lst) / len(lst)

def _l(a):
    return 0 if a == 0 else math.log10(a)

# Threshold charge value used to determine a 'hit' on a pad if
# the max - min of the trace is greater than
THRESHOLD = 50
# The number of pads in the AT-TPC
NUMBEROFPADS = 10240
# The number of time buckets the window spans
WINDOWSIZE = 50

def real_unlabeled_events(projection, save_path, prefix):
    print('Processing data...')
    data = []

    events = pytpc.HDFDataFile('corrected_run_0210.h5', 'r')
    for x, event in enumerate(events):
        # Get pytpc xyzs
        xyzs = event.xyzs(peaks_only=True, return_pads=True,
            baseline_correction=False, cg_times=False)

        event_trace = np.ndarray(NUMBEROFPADS, dtype=object)
        # Get the events trace across each pad
        with h5py.File('corrected_run_0210.h5', 'r') as f:
            dset = f['get/'+str(x+1)]
            trace = dset[:,10:510]    #works better when you exclude start and end
            TRACELENGTH = len(trace[0])
            for i in range(NUMBEROFPADS):
                y = np.zeros(TRACELENGTH)
                pad_number = dset[i,4]
                current_pad = trace[i]
                for j in range(TRACELENGTH):
                    y[j] = current_pad[j]
                event_trace[pad_number] = y

        hit_peaks = []
        for i in range(NUMBEROFPADS):
            trace = event_trace[i]
            trace_max = np.amax(trace)
            trace_average = _average(trace)
            charge = trace_max - trace_average
            peak_time = np.argmax(trace)
            #move window across trace
            for timebucket in range(25,475):
                firstvalue = trace[timebucket-25]
                middlevalue = trace[timebucket]
                lastvalue = trace[timebucket+25]
                average_first_last = (firstvalue+lastvalue)*0.5
                peakheight = middlevalue - average_first_last
                if peakheight > THRESHOLD:  #  time     charge   padnumber
                    hit_peaks.append([peak_time, charge, i])
                    break
        np.asarray(hit_peaks)
        HITPEAKSLENGTH = len(hit_peaks)

        # Merge pytpc xyzs array with correct charge values
        plot_points = np.zeros(shape=(HITPEAKSLENGTH,4))
        for i in range(HITPEAKSLENGTH):
            hitpeaks_padnum = hit_peaks[i][2]
            for j in range(NUMBEROFPADS):
                xyzs_padnum = xyzs[j][4]
                if(hitpeaks_padnum == xyzs_padnum):
                    plot_points[i][0] = xyzs[j][0]       #x
                    plot_points[i][1] = xyzs[j][1]       #y
                    plot_points[i][2] = hit_peaks[i][0]   #time
                    plot_points[i][3] = hit_peaks[i][1]   #charge

        data.append(plot_points)

    # Take the log of charge data
    log = np.vectorize(_l)

    for event in data:
        event[:,3] = log(event[:,3])

    # Normalize
    max_charge = np.array(list(map(lambda x: x[:, 3].max(),data))).max()

    for e in data:
        for point in e:
            point[3] = point[3] / max_charge


    print('Making images...')

    # Make numpy set
    images = np.empty((len(data), 128, 128, 3), dtype=np.uint8)

    for i, event in enumerate(data):
        e = event
        if projection == 'zy':
            x = e[:, 2] #actually z (time)
            y = e[:, 1]
            charge = e[:, 3]
        elif projection == 'xy':
            x = e[:, 0]
            y = e[:, 1]
            charge = e[:, 3]
        else:
            raise ValueError('Invalid projection value.')
        fig = plt.figure(figsize=(1, 1), dpi=128)
        if projection == 'zy':
            plt.xlim(0.0, 512)
        if projection == 'xy':
            plt.xlim(-275.0, 275.0)
        plt.ylim((-275.0, 275.0))
        plt.axis('off')
        #cmap='gray_r' the _r inverts greyscale so high charge is black
        #while low charge is white
        plt.scatter(x, y, s=0.6, c=charge, cmap='gray_r')
        fig.canvas.draw()
        eventData = np.array(fig.canvas.renderer._renderer, dtype=np.uint8)
        eventData = np.delete(eventData, 3, axis=2)
        images[i] = eventData
        plt.close()

    print('Saving file...')

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    filename = os.path.join(save_path, prefix + 'images.h5')

    #save to HDF5 file
    h5 = h5py.File(filename, 'w')
    h5.create_dataset('images', data=images)
    #h5.create_dataset('max_charge', data=np.array([max_charge]))
    h5.close()

if __name__ == '__main__':
    real_unlabeled_events('xy','./','new_hit_method_thresh50_')
