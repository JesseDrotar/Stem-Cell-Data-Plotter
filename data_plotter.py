#!/usr/bin/python
#This program accepts in .csv cell data and produces appropriate line plots


import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
from collections import OrderedDict
from itertools import cycle
from matplotlib.backends.backend_pdf import PdfPages

#Sets up a new pdf document that will contain the plots
pp = PdfPages('multipage.pdf')

filename = sys.argv[1]

with open(filename, 'r') as f:
    reader = csv.reader(f, delimiter='\t')

	#Skips the headings of the data file
    next(reader)

    my_dict = dict()

    my_dict_control = dict()

	#Builds dictionary of all time points of C2 values for each well of the plate.
	#Key value being the well_ID
	#my_dict_control has the same structure however has C3 control values in place of C2 values.
    for rows in reader:
        if rows[0] in my_dict:
            my_dict[rows[0]].append(rows[2])
            my_dict_control[rows[0]].append(rows[3])
        else:
            my_dict[rows[0]] = [rows[2]]
            my_dict_control[rows[0]] = [rows[3]]

sorted_dict = {}
sorted_control_dict = {}

sorted_dict = collections.OrderedDict(sorted(my_dict.items()))

sorted_control_dict = collections.OrderedDict(sorted(my_dict_control.items()))

final_dict = {}
final_control_dict = {}

for j in sorted_dict.keys():
    if len(sorted_dict[j]) != 9:
        pass
    else:
        final_dict[j] = sorted_dict[j]

for x in sorted_control_dict.keys():
    if len(sorted_control_dict[x]) != 9:
        pass
    else:
        final_control_dict[x] = sorted_control_dict[x]

final_sorted_dict = {}
final_sorted_control_dict = {}

final_sorted_dict = collections.OrderedDict(sorted(final_dict.items()))

final_sorted_control_dict = collections.OrderedDict(sorted(final_control_dict.items()))

key_list = list(final_sorted_dict.keys())

#Builds a pdf plot of all the wells and their control values, limits each plot to 7 wells per figure.
with PdfPages('haiting.pdf') as pdf:
    key_start = 0
    key_end = 7
    for x in range(57):
        fig = plt.figure(figsize=(20, 10))

        ax = fig.add_subplot(111)

        ax.set_color_cycle(
            ['red', 'red', 'green', 'green', 'blue', 'blue', 'black', 'black', 'yellow', 'yellow', '#BE33FF', '#BE33FF',
             '#33FCFF', '#33FCFF'])

        for key in key_list[key_start:key_end]:
            y_val = np.array(final_sorted_dict[key])
            y_val_control = np.array(final_sorted_control_dict[key])
            x_val = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

            plt.plot(x_val, y_val, marker='o', linestyle='solid', linewidth=2, label=key)
            plt.plot(x_val, y_val_control, marker='o', linestyle='dashed', linewidth=2, label=key)

            plt.title("Cells")

            plt.ylabel("Median C2")
            plt.xlabel("Time ID")
            ax.legend(loc='lower right', bbox_to_anchor=(1, 0), ncol=7, fontsize=10)
        # plt.show()

        key_start = key_start + 7
        key_end = key_end + 7

        pdf.savefig()
        plt.close()

