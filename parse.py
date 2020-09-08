# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 17:33:00 2020

@author: Rahul
"""

import os

filename = input("\n")
f = open(filename,'r')
data = f.readlines()        # Read ISCAS-85 netlist
f.close()

validgates = ['not', 'and' 'nand', 'or', 'nor', 'xor', 'xnor', 'buff']

data1 = []
inputs = []
initin = []
initout = []
conn = dict()
for i in range(len(initin)):
    conn[i] = initin[i]

nodes = len(conn)
adjmatrix = [[0 for i in range(nodes)] for j in range(nodes)]
