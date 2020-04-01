# -*- coding: utf-8 -*-

import re
from enum import Enum
from cread import cread
#from flr import flr
from classdef import node
from classdef import gtype
from classdef import ntype
from gate import GAND
from gate import GOR
from gate import GXOR
from gate import GNOT
from lev import lev
#from logicsim import logic_sim
"""
from dfs import dfs
from pfs import pfs
from faultdict_gen import faultdict_gen
from mini_faultlist_gen import mini_faultlist_gen
from equv_domain import equv_domain
from d_alg import *
"""
#from classdef import five_value
#from D_alg import imply_and_check
#__________________________________________________#
#________________main_test for cread_______________#
#__________________________________________________#

input_nodes = []
nodelist_test = cread('c17.ckt658',input_nodes)
Nnodes = len(nodelist_test)


#__________________________________________________#
#________________main_test for flr_________________#
#__________________________________________________#

#print ('before flr test')
#for i in range(len(nodelist_test)):
#    if nodelist_test[i].cpt == 1:
#        print (nodelist_test[i].num, 'cpt')
#flr(nodelist_test)


# print ('cpt sa0 test')
# for i in range(len(nodelist_test)):
#     if nodelist_test[i].cpt == 1:
#         print (nodelist_test[i].num,'cptSA0',nodelist_test[i].sa0)

# print ('cpt sa1 test')
# for i in range(len(nodelist_test)):
#     if nodelist_test[i].cpt == 1:
#         print (nodelist_test[i].num,'cptSA1',nodelist_test[i].sa1)

# print ('normal sa0 test')
# for i in range(len(nodelist_test)):
#     if nodelist_test[i].cpt != 1:
#         print (nodelist_test[i].num,'SA0',nodelist_test[i].sa0)

# print ('normal sa1 test')
# for i in range(len(nodelist_test)):
#     if nodelist_test[i].cpt != 1:
#         print (nodelist_test[i].num,'SA1',nodelist_test[i].sa1)

#__________________________________________________#
#________________main_test for lev_________________#
#__________________________________________________#
nodelist_order = lev(nodelist_test, Nnodes)
for i in nodelist_test:
  print('{}\t{}\t{}\t'.format(i.gtype, i.lev, i.num))

#__________________________________________________#
#_____________main_test for logic_sim______________#
#__________________________________________________#
# nodelist_order = lev(nodelist_test, Nnodes)
# logic_sim(nodelist_order)
# for i in nodelist_test:
#     print('{}\t{}\t'.format(i.num,i.value))

#__________________________________________________#
#_____________main_test for dfs&pfs________________#
#__________________________________________________#
# nodelist_order = lev(nodelist_test, Nnodes)
# logic_sim(nodelist_order)
# fault_list = dfs(nodelist_order, Nnodes)
# pfs('input.txt', nodelist_order,'full_fault_list.txt')
# print(fault_list)
# for i in nodelist_test:
#     print('{}\t{}\t{}'.format(i.num, i.faultlist_dfs, i.value))


#__________________________________________________#
#__________main_test for faultdict_gen_____________#
#__________________________________________________#
# dict_for_equv = faultdict_gen(input_nodes, nodelist_test)
# pfs('input.txt', nodelist_test, 'full_fault_list.txt')
# print (dict_for_equv)

#__________________________________________________#
#__________main_test for mini_faultlist_gen________#
#__________________________________________________#
#faultlist_afterflr = flr(nodelist_test)


#print(dict_for_equv_new)
# mini_faultlist_gen()


#__________________________________________________#
#__________main_test for equv and domain___________#
#__________________________________________________#
# dict_for_equv = faultdict_gen(input_nodes, nodelist_test)
# print(dict_for_equv)
#equv = equv_domain()
#print(equv[0]) #print equv
#print(equv[1]) #print domain

#__________________________________________________#
#__________D_algorithm_____________________________#
#__________________________________________________#
# nodelist_order = lev(nodelist_test, Nnodes)
# fault_node_num = 11
# fault_type = "sa1"
# fault_info = []
# #fault_node_class
# ## assign x to all the value of node and fault value to the fault node
# for i in range(len(nodelist_order)):
#     nodelist_order[i].value = five_value.X.value
#     if nodelist_order[i].num == fault_node_num:
#         if fault_type == "sa0":
#             nodelist_order[i].value = five_value.D.value
#             #fault_node_class = nodelist_order[i]
#             #fault_info.append(nodelist_order[i])
#             #fault_index = i
#             fault_index = i
#             fault_info.append(i)
#         elif fault_type == "sa1":
#             nodelist_order[i].value = five_value.D_BAR.value
#             #fault_node_class = nodelist_order[i]
#             #fault_index = i
#             #fault_info.append(nodelist_order[i])
#             fault_index = i
#             fault_info.append(i)
#         else:
#             print("operator error")

# #nodelist_order[0].value = 0
# if D_alg(nodelist_order,fault_index)==1:
#     print("D_alg SUCCESS")
# else:
#     print("D_alg FALIURE")
# #print(list_test)
# #print(len(d_froniter_list))

#__________________________________________________#
#_____________________PODEM________________________#
#__________________________________________________#


