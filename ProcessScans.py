# =============================================================================
# ProcessScans.py: Script to process the two pressure wave scans.
# Sean Z. Roberson
# October 31, 2023
# Take the two files Scan1_1031_8cm.csv and Scan2_1031_6cm.csv
# and extract the peaks, reshape, and plot the pressure wave.
# THe second column in the initial file can be discarded, but keep
# the original file for safekeeping.
# =============================================================================

import numpy as np
# import os
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
import tkinter as tk
import easygui

# This function will process the indicated file.
def getPeaks(f, shape):
    # f is the filename to process, and
    # shape is a tuple that represents the size of the output array.
    # Load the file, then remove the time column.
    # The LabView-generated arrays are tab delimited.
    (x_steps, y_steps) = shape
    A = np.array(np.loadtxt(f, delimiter='\t')[:,1], ndmin = 2)
    A = A.reshape(x_steps * y_steps, 10000)
    
    # Compute the peak-to-peak distances.
    highs = A.max(axis = 1)
    lows = A.min(axis = 1)
    peaks = np.array(highs - lows)
     
    # Now reshape to the dimensions in shape and take the transpose.
    peaks = peaks.reshape(shape).T
     
    # Flip every other column.
    peaks[:, 1::2] = peaks[::-1, 1::2]
     
     
    # Plot the field shape. Convert the distances to millimeters, and
    # make a meshgrid. Remember that the scan is done in increments of
    # 100 steps.
    x = 25.4 * np.arange(start = 0,
               stop = 0.025*(x_steps),
               step = 0.025)
    y = 25.4 * np.arange(start = 0,
               stop = 0.025*(y_steps),
               step = 0.025)
    X, Y = np.meshgrid(x, y)
     
    fig = plt.figure(dpi = 150, figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Major Axis Scan of Pressure Wave')
    ax.view_init(azim = -10)
    ax.plot_surface(X, Y, peaks, cmap = cm.coolwarm, edgecolor = 'none')
    ax.set_xlabel('Axis 1 Position (mm)')
    ax.set_ylabel('Axis 2 Position (mm)')
    ax.set_zlabel('Amplitude')
    plt.show()
       
    return peaks

# Execution in command line.
def main():
	# Define the shape to process.
	x_steps = int(sys.argv[2])
	y_steps = int(sys.argv[3])
	shape = (x_steps, y_steps)
	
	f = sys.argv[1]
	
	peaks = getPeaks(f, shape)
	
	root = tk.Tk()
	root.withdraw()
	
	# Prompt to save file.
	save_file = easygui.ynbox('Would you like to save the processed file?')
	
	if save_file:
		file_path=easygui.filesavebox(default='*.csv', filetypes=["*.csv"])
		if file_path:
			np.savetxt(file_path, peaks, delimiter=',')
			
	root.destroy()
	
if __name__ == "__main__":
	main()