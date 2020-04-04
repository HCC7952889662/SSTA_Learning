from PDF import *
from main import nodelist_test

try:
    sstalib = read_sstalib("tech10nm.sstalib")
    
    for i in nodelist_test:
        if(i.gtype!='BRCH'):
            if(i.gtype=='IPT'):     ##initiating total_dist of nodes of type "IPT" 
                i.total_dist=PDF_generator(sstalib,i.gtype,50)    
            else:   ## All other gtype are gates (except BRCH)
                i.gate_dist=PDF_generator(sstalib,i.gtype,50)       ###every node gets its gate_dist distribution data except for BRCH
        
    for i in nodelist_test:
        if(i.gtype!='IPT'):
            if(i.gtype=='BRCH'):    ###For 'BRCH' type gates simply update their total_dist with whatever node they are connected to on input side.
                i.total_dist=i.unodes[0].total_dist
            else:
                max_of_inputs = (i.unodes[0].total_dist) ##1 input gates (NOT)
                if(len(i.unodes)>1):  ##for multi-input gates    
                    for k in range(0,len(i.unodes)-1):  ###find the max of all inputs.
                        max_of_inputs = (max_of_inputs).MAX(i.unodes[k+1].total_dist)      ##finding max of two inputs at a time
                        N = math.ceil(max_of_inputs.data['Data'].size/500)
                        (max_of_inputs).data_shrink_mode(N, mode='fast')    ##reducing the number of samples.

                i.total_dist = (i.gate_dist).SUM(max_of_inputs)     ##Adding Max_of_inputs with gate_distribution
                N = (i.total_dist.data['Data'].size/500)
                (i.total_dist).data_shrink_mode(10, mode='fast')    ##total delay distribution of gate after reducing samples.
        print('{}\t{}\t{}\t'.format(i.gtype, i.lev, i.num),"completed")
    
    
    # for i in list_output:
    #     for j in nodelist_test:
    #         if(int(i)==j.num):
    #             j.total_dist.plot()

    max_lvl=0
    for i in nodelist_test:     ##find the maximum level in the circuit to identify output nodes.
        if(i.lev>max_lvl):
            max_lvl=i.lev
    for i in nodelist_test:     ##plotting the distribution of output nodes.
        if(i.lev==max_lvl):
            print("showing plot for node",i.num)
            i.total_dist.plot()
    print("simulation ends.")
except IOError:
    print("error in the code")