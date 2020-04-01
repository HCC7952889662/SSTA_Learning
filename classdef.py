# -*- coding: utf-8 -*-
from numpy import uint64
from enum import Enum

#__________________________________________________#
#_____________________CLASSDEF_____________________#
#__________________________________________________#

class five_value(Enum): 
   ZERO = 0
   ONE = 15
   D = 12
   D_BAR = 3
   X = 9

class gtype(Enum):
    IPT = 0
    BRCH = 1
    XOR = 2
    OR = 3
    NOR = 4
    NOT = 5
    NAND = 6
    AND = 7

class ntype(Enum):
    GATE = 0
    PI = 1
    FB = 2
    PO = 3
 


class node:
	
	def __init__(self):
		self.value = None
		self.num = None
		self.lev = None
		self.gtype = None
		self.ntype = None
		self.unodes = []
		self.dnodes = []
		self.fin = None
		self.fout = None
		self.cpt = 0
		self.sa0 = 0
		self.sa1 = 0
		self.index = 0
		self.faultlist_dfs = []
		self.parallel_value = 0
	def add_unodes(self, unode):
		self.unodes.append(unode)
	def add_dnodes(self, dnode):
		self.dnodes.append(dnode)
	def add_faultlist(self, fault):
		self.faultlist_dfs.append(fault)
	def clear_faultlist(self):
		self.faultlist_dfs.clear()
	def copy_faultlist(self, faultlist):
		faultlist_dfs = faultlist.copy()
