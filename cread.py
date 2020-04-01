# -*- coding: utf-8 -*-

import re
from classdef import node
from classdef import gtype
from classdef import ntype


#__________________________________________________#
#_____________________Read_CKT_____________________#
#__________________________________________________#
def cread(c_name, input_nodes):
    f = open(c_name,'r')
    indx = 0
    nodelist = []
    nodedict = {}
    lines = f.readlines()
    for line in lines:
        linesplit = line.split()
        new_node = node()
        new_node.ntype = ntype(int(linesplit[0])).name
        new_node.num = int(linesplit[1])
        new_node.gtype = gtype(int(linesplit[2])).name
        
        if (ntype(int(linesplit[0])).value == 2):   #if BRCH --> unodes
            new_node.add_unodes(nodedict.get(int(linesplit[3])))
            new_node.fout = 1 
        else:                                       #if not BRCH --> fout
            new_node.fout = int(linesplit[3])

        if (ntype(int(linesplit[0])).value != 2):
            new_node.fin = int(linesplit[4])
            for i in range (int(linesplit[4])):
                new_node.add_unodes(nodedict.get(int(linesplit[5 + i])))
        else:
            new_node.fin = 1
        
        if ((ntype(int(linesplit[0])).value == 1) or (ntype(int(linesplit[0])).value == 2)):
            new_node.cpt = 1

        new_node.index = indx
        indx = indx + 1
        nodelist.append(new_node)
        nodedict.update({new_node.num: new_node})

    f.close()

    for i in range(len(nodelist)):
        if (nodelist[i].ntype != 'PI'):
            for j in range (nodelist[i].fin):
                nodelist[i].unodes[j].add_dnodes(nodelist[i])
        else:
            input_nodes.append(nodelist[i].num)
    return nodelist