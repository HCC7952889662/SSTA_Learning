from PDF_exp_version import *
import math
import seaborn as sns
from cread import cread
from lev import lev

# Library Read Function : return a Dict
def read_sstalib(filename):
    sstalib = {}
    infile = open(filename)
    count = 0
    #condition on cell form to how to read it.
    for line in infile:
        if line != "":
            if re.match(r'^#', line):
                pass
            else:
                line_syntax =  re.match(r'cell (.*):',line, re.IGNORECASE)
                if line_syntax:
                    gate = line_syntax.group(1)
                    count+=1

                line_syntax = re.match(r'.*form = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    form = line_syntax.group(1)
                    count += 1

                line_syntax = re.match(r'.*mu = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    mu = float(line_syntax.group(1))
                    count += 1

                line_syntax = re.match(r'.*sigma = (.*)', line, re.IGNORECASE)
                if line_syntax:
                    sigma = float(line_syntax.group(1))
                    count += 1

                if count == 4:
                    sstalib[gate] = {'form': form, 'mu': mu, 'sigma': sigma}
                    count = 0
    # it should return an object of Dict
    #{'IPT': {'form': 'normal', 'mu': '2', 'sigma': '0.5'},  'NOT': {'form': 'normal', 'mu': '4', 'sigma': '0.5'},
    # 'NAND': {'form': 'normal', 'mu': '6', 'sigma': '0.8'}, 'AND': {'form': 'normal', 'mu': '6.5', 'sigma': '0.8'},
    # 'NOR': {'form': 'normal', 'mu': '7', 'sigma': '0.8'},  'OR': {'form': 'normal', 'mu': '7.5', 'sigma': '0.8'},
    # 'XOR': {'form': 'normal', 'mu': '12', 'sigma': '1.5'}, 'BUFF': {'form': 'normal', 'mu': '2.5', 'sigma': '0.5'},
    # 'XNOR': {'form': 'normal', 'mu': '12', 'sigma': '1.5'}}
    return sstalib

# PDF Generating function
def PDF_generator(sstalib, gate, sample_dist):
    return PDF(sample_dist = sample_dist, mu = sstalib[gate]['mu'], sigma = sstalib[gate]['sigma'])

# Call ATPG team Function for circuit parse
def circuit_parse_levelization(filename):
    input_nodes = []
    nodelist_test = cread(filename,input_nodes)
    Nnodes = len(nodelist_test)
    nodelist_order = lev(nodelist_test, Nnodes)
    return(nodelist_test)

# STA Time analysis
def set_means(sstalib, nodelist_test):
    for i in nodelist_test:
        if(i.gtype!='BRCH'):
            if(i.gtype=='IPT'):     ##initiating total_dist of nodes of type "IPT" 
                i.total_mean=sstalib['IPT']['mu']   
            else:   ## All other gtype are gates (except BRCH)
                i.gate_mean=sstalib[i.gtype]['mu']

def means_update(nodelist_test):
    for i in nodelist_test:
        if(i.gtype!='IPT'):
            if(i.gtype=='BRCH'):    ###For 'BRCH' type gates simply update their total_dist with whatever node they are connected to on input side.
                i.total_mean=i.unodes[0].total_mean
            else:
                max_of_inputs_means = (i.unodes[0].total_mean)##1 input gates (NOT or BUFF)
                if(len(i.unodes)>1):  ##for multi-input gates    
                    for k in range(0,len(i.unodes)-1):  ###find the max of all inputs.
                        max_of_inputs_means = (max_of_inputs_means) if(max_of_inputs_means>i.unodes[k+1].total_mean) else (i.unodes[k+1].total_mean)      ##finding max of two inputs at a time
                i.total_mean= (i.gate_mean)+max_of_inputs_means ##Adding Max_of_inputs with gate_distribution

def find_mean(sstalib, nodelist_test):
    set_means(sstalib, nodelist_test)
    means_update(nodelist_test)
    #for i in nodelist_test:     
    #   if(i.ntype=="PO"):
    #      print("Mean value of node %i using STA method is %f"%(i.num,i.total_mean))
    #return

def set_nodes(sstalib, nodelist_test):
    for i in nodelist_test:
        if(i.gtype!='BRCH'):
            if(i.gtype=='IPT'):     ##initiating total_dist of nodes of type "IPT" 
                i.total_dist=PDF_generator(sstalib,i.gtype,sample_dist)
            else:   ## All other gtype are gates (except BRCH)
                i.gate_dist=PDF_generator(sstalib,i.gtype,sample_dist)       ###every node gets its gate_dist distribution data except for BRCH

# SSTA Time analysis
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
                        
                i.total_dist = (i.gate_dist)+(max_of_inputs) ##Adding Max_of_inputs with gate_distribution
        print('{}\t{}\t{}\t'.format(i.gtype, i.lev, i.num),"completed")
        #if(i.num==int(sys.argv[1])):
        #    plt.figure()
        #    plt.title("plot for node %i"%(i.num))
        #    plt.xlabel('Delay(ns)')
        #    plt.ylabel('Probability')
        #    sns.lineplot(i.total_dist.delay, i.total_dist.pdf, color='teal')
        #    plt.show()
        #    return

def plot_outputs(nodelist_test):
    total_plots=0
    rows=0
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
            plt.title("STA mu of node %i : %f"%(i.num,i.total_mean))
            plt.suptitle("plots for output nodes") # %i"%(i.num))
            #plt.title("plot for node %i"%(i.num))
            plt.xlabel('Delay(ns)')
            plt.ylabel('Probability')
            sns.lineplot(i.total_dist.delay, i.total_dist.pdf, color='teal')
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
   
#try:
    #start=timeit.default_timer()

    #sstalib = read_sstalib(sys.argv[1])

    #nodelist_test = circuit_parse_levelization(sys.argv[2])
    #set_nodes(nodelist_test) ##initiallize the content of every node.

    #ckt_update(nodelist_test) ## update the content of every node as we parse through the circuit level by level.

    #stop=timeit.default_timer()
    #elapsed_time = stop-start
    #print("Simulation Time: ",elapsed_time," seconds")
    #find_mean(nodelist_test)
    #plot_outputs(nodelist_test)  ##plot the delay distribution for output nodes.
    #print("simulation ends.")

#except IOError:
    #print("error in the code")


