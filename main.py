# -*- coding: utf-8 -*-
import sys
import timeit
from ckt_sim import *
import matplotlib.pyplot as plt
import seaborn as sns

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
print('Library File Reading ... ', end = '')
sstalib = read_sstalib(lib)
print('completed')

# ATPG Team Function for Circuit Parse
print('circuit parsing ... ', end = '')
nodelist_test = circuit_parse_levelization(circuit)
print('completed')

# SSTA Analysis
print('SSTA Analysis... START!')
print('Circuit PDF Setting ...', end = '')
set_nodes(sstalib, nodelist_test) ##initiallize the content of every node.
print('completed')
print('SSTA MAX & SUM Calculating ...')
ckt_update(nodelist_test) ## update the content of every node as we parse through the circuit level by level.
print('SSTA MAX & SUM Calculating ... completed')
print('SSTA Analysis ...END')

##Reconvergent Algorithm
reconvergent_top(nodelist_test)

# End Time Counting
stop=timeit.default_timer()
elapsed_time = stop-start
print("Simulation Time: ",elapsed_time," seconds")

# STA analysis
print('STA analysis ... ', end = '')
find_mean(sstalib, nodelist_test)
print('completed')

# ###### Monte Carlo Analysis
print("monte carlo analysis....")
monte_carlo(sstalib, nodelist_test)
print("complete")


# Output Plot
plot_outputs(nodelist_test)  ##plot the delay distribution for output nodes.
print("simulation ends.")
