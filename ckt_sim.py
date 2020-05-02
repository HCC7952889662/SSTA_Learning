from PDF import *
import math
import seaborn as sns
from cread import cread
from lev import lev
import scipy.stats
import itertools

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

## reconvergent algorithm top function
def reconvergent_top(nodelist_test):
    for i in nodelist_test:
        if(len(i.unodes)>1):    ##correlation occurs for multi-input gates
            DLi,DLo = gen_dep_list(i)       ###it generates the dependency lists for every input of 'i' node.
            depMax(i,DLi,DLo)       ##depMax algorithm for correction in i.total_dist

# Finding Dependency list for the inputs.
def gen_dep_list(i):
    ##find input that become 1 well before any other input arrives. We need to check similarity between every pair of inputs.
    dep_inputs = [] ##list of inputs that will contribute to output
    all_combos = list(itertools.combinations(i.unodes,2))   ##it generates the list of tuples, each of size 2 using nC2 for checking similarity between every pair of inputs of 'i' nodes
    for node in all_combos:
        print("node no. ",i.num," input combos are ",node[0].num,node[1].num)
        mu1=np.mean(node[0].total_dist.delay)
        mu2=np.mean(node[1].total_dist.delay)
        std1=np.std(node[0].total_dist.delay)
        std2=np.std(node[1].total_dist.delay)
        l1=len(node[0].total_dist.delay)
        l2=len(node[1].total_dist.delay)
        t= abs((mu1-mu2)/np.sqrt((std1**2/l1)+(std2**2/l2)))    ##if t-value is close to 0 then it means both inputs are arriving close to each other. So we have to consider them.
        if(t<=10):
            if node[0] not in dep_inputs:
                dep_inputs.append(node[0])
            if node[1] not in dep_inputs:
                dep_inputs.append(node[1])
    
    ##finding the dependency lists for every input in dep_inputs
    DLi = {}
    for j in dep_inputs:
        temp_list = []
        temp_list.append(j)     ### is it needed?
        dep_list(j,temp_list)
        DLi[j]=temp_list
    
    DLo = []
    if(i.fout>1):
        DLo.append(i)
    for j in dep_inputs:
        for v in DLi[j]:
            if v not in DLo:
                DLo.append(v)
    DLo.sort(key=lambda x: x.lev,reverse=True)      ##sort nodes in DLo in the decreasing order of levels
    # for x in DLo:
    #     print(x.num)
    return DLi,DLo

def dep_list(j,temp_list):  ## recursive function to find all the nodes on which input of 'i' node depends
    if(j.gtype=='IPT'):     ##find till IPT nodes.
        if j not in temp_list:
            temp_list.append(j)
        return
    else:
        for i in j.unodes:
            if i not in temp_list:
                temp_list.append(i)
            dep_list(i,temp_list)

##Algorithm depMax
def depMax(i,DLi,DLo):
    Ao = None       ###arrival time at the output of 'i' node
    L = []      ##list of all nodes 'v' that are connected to multiple inputs of 'i' node 
    mapping = {}        ##holds the mapping of 'v' to inputs nodes to which it is connected
    for v in DLo:   ##only those v's that are connected to more than 1 inputs are of interest.
        tmp_list = []
        for i_node in list(DLi.keys()):
            for j in DLi[i_node]:
                if(v.num==j.num):
                    tmp_list.append(i_node)
        if(len(tmp_list)>1):
            mapping[v]=tmp_list
            L.append(v)

    # for x in list(mapping.keys()):
    #     print("key is ",x.num)
    #     for y in mapping[x]:
    #         print("value ",y.num)
    if(len(L)==0):      ##if L for 'i'th node is empty there is no correlation between its inputs.
        return
    else:
        plt.figure()
        for v in L:
            print("reconvergent node is ",v.num)
            sub_dist = SUB(v,0,mapping)     ### A0-Av
            Aov = sub_dist #+ i.gate_dist        #Aov = A0 - Av
            
            for idx in range(1,len(mapping[v])):
                tmp_Aov = SUB(v,idx,mapping) #+ i.gate_dist     ## Ai-Av
                Aov = Aov.MAX(tmp_Aov) # find max among all Ai-Av
            
            if(Ao == None): ##if Ao is initiated for the first time
                Ao = Aov
            else:
                Ao = Ao.MAX(Aov+v.total_dist)       ###Aov+v.total_dist is done based on equation12 on page 611

        Ao = Ao + i.gate_dist   ##i.gate is added at end to improve run time.
        plt.plot(i.total_dist.delay,i.total_dist.pdf,'--')
        i.total_dist = Ao       ##i.total_dist is updated.
        plt.plot(i.total_dist.delay,i.total_dist.pdf)
        plt.show()
        
def SUB(v,idx,mapping):         # sub_dist = Aidx - Av
    mu_Ai = np.mean(mapping[v][idx].total_dist.delay)
    std_Ai = np.std(mapping[v][idx].total_dist.delay)
    mu_Av = np.mean(v.total_dist.delay)
    std_Av = np.std(v.total_dist.delay)
    mu_sub = mu_Ai - mu_Av      
    std_sub = np.sqrt(std_Ai**2 - std_Av**2)
    sub_dist = PDF(sample_dist,mu=mu_sub,sigma=std_sub)     ###Aidx-Av
    return sub_dist

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
            sns.scatterplot(i.total_dist.delay, i.total_dist.pdf, color='teal')
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
