# -*- coding: utf-8 -*-
import sys
import timeit
from ckt_sim import *

#__________________________________________________#
#________________main_test for SSTA________________#
#__________________________________________________#

# Figure Setting
sns.set(color_codes=True,style="white")
# settings for seaborn plot sizes
sns.set(rc={'figure.figsize':(6,6)})

# Input from command line arguments
lib = sys.argv[1]
circuit = sys.argv[2]

# Timer Setting
start=timeit.default_timer()

# Read data from Library File to set up the Gate PDFs
sstalib = read_sstalib(lib)

# ATPG Team Function for Circuit Parse
nodelist_test = circuit_parse_levelization(circuit)

# SSTA Analysis
set_nodes(sstalib, nodelist_test) ##initiallize the content of every node.
ckt_update(nodelist_test) ## update the content of every node as we parse through the circuit level by level.


# End Time Counting
stop=timeit.default_timer()
elapsed_time = stop-start
print("Simulation Time: ",elapsed_time," seconds")

# STA analysis
find_mean(sstalib, nodelist_test)

# Output Plot
plot_outputs(nodelist_test)  ##plot the delay distribution for output nodes.
print("simulation ends.")
