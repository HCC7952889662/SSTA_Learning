from PDF import *
from main import nodelist_test
import math

def set_nodes(nodelist_test):
    for i in nodelist_test:
        if(i.gtype!='BRCH'):
            if(i.gtype=='IPT'):     ##initiating total_dist of nodes of type "IPT" 
                i.total_dist=PDF_generator(sstalib,i.gtype,samples,sample_dist)    
            else:   ## All other gtype are gates (except BRCH)
                i.gate_dist=PDF_generator(sstalib,i.gtype,samples,sample_dist)       ###every node gets its gate_dist distribution data except for BRCH

def ckt_update(nodelist_test):
    for i in nodelist_test:
        if(i.gtype!='IPT'):
            if(i.gtype=='BRCH'):    ###For 'BRCH' type gates simply update their total_dist with whatever node they are connected to on input side.
                i.total_dist=i.unodes[0].total_dist
            else:
                max_of_inputs = (i.unodes[0].total_dist) ##1 input gates (NOT or BUFF)
                if(len(i.unodes)>1):  ##for multi-input gates    
                    for k in range(0,len(i.unodes)-1):  ###find the max of all inputs.
                        max_of_inputs = (max_of_inputs).MAX(i.unodes[k+1].total_dist)      ##finding max of two inputs at a time
                        
                ##Adding Max_of_inputs with gate_distribution
                i.total_dist = (i.gate_dist)+(max_of_inputs)
        print('{}\t{}\t{}\t'.format(i.gtype, i.lev, i.num),"completed")

def plot_outputs(nodelist_test):
    total_plots=0
    rows=0
    cols=0
    for i in nodelist_test:     ##plotting the distribution of output nodes.
        if(i.ntype=="PO"):
            total_plots = total_plots + 1
    if(total_plots>=4):
        cols = 4 
    else:
        cols=total_plots
    rows = rows + math.ceil(float(total_plots)/4)
    plt.figure()
    plt.subplot2grid((rows,cols),(0,0),colspan=cols)
    r=0
    c=0 
    for i in nodelist_test:     ##plotting the distribution of output nodes.
        if(i.ntype=="PO"):
            plt.subplot2grid((rows,cols),(r,c))
            plt.title("plot for node %i"%(i.num))
            plt.xlabel('Delay(ns)')
            plt.ylabel('Probability')
            sns.lineplot(i.total_dist.delay, i.total_dist.pdf, color='black')
            c = c+1
            if(c==4):
                r = r+1
                c=0
    # plt.tight_layout()
    plt.subplots_adjust(wspace=0.5,hspace=0.7)
    plt.savefig('output_delay_dist.pdf')
    plt.show()
    # for i in nodelist_test:     ##plotting the distribution of output nodes.
    #     if(i.num==16):
    #         i.total_dist.plot()
    #         plt.title("plot for node %i"%(i.num))
    #         plt.show()
   
try:
    sstalib = read_sstalib("tech10nm.sstalib")
    
    set_nodes(nodelist_test) ##initiallize the content of every node.

    ckt_update(nodelist_test) ## update the content of every node as we parse through the circuit level by level.
    
    plot_outputs(nodelist_test)  ##plot the delay distribution for output nodes.
    
    print("simulation ends.")
except IOError:
    print("error in the code")
