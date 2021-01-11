# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 17:33:00 2020

@author: Rahul
"""

def netadj85(filename):
    
    f = open(filename,'r')
    data = f.readlines()
    f.close()
    
    validgates = ['not', 'and', 'nand', 'or', 'nor', 'xor', 'xnor', 'buff']
    
    data1 = []
    for i in range(len(data)):
        line = data[i].split(" ")
        if (line[0] == "*"):
            continue
        elif (len(line) > 3):
            if (data[i].split(" ")[:-1][2] in validgates and 
                data[i].split(" ")[:-1][0] != '\t'):
                temp = data[i+1].split("\t")[1:-1]
                temp.append(data[i+1].split("\t")[-1].split("\n")[0])
                data1.append(data[i].split(" ")[:-1] + temp)
            elif (data[i].split(" ")[0][:1] != '\t'):
                data1.append(data[i].split(" ")[:-1])
    
    inputs = []
    outputs = []
    initin = []
    initout = []
    nodes = []
    
    wires = dict()
    for i in range(len(data1)):
        if (data1[i][2] == 'inpt'):
            inputs.append(data1[i][1])
        elif (data1[i][2] in validgates):
            temp = []
            k = data1[i][-1*int(data1[i][4]):]
            for j in k:
                if (data1[int(j)-1][1][-3:] == 'fan'):
                    temp.append(data1[int(j)-1][3])
                    if data1[i][1][:-3] not in wires:
                        wires[data1[i][1][:-3]] = [data1[int(j)-1][3][:-3]]
                    else:
                        wires[data1[i][1][:-3]].append(data1[int(j)-1][3][:-3])
                elif (data1[int(j)-1][1][-3:] == 'gat'):
                    temp.append(data1[int(j)-1][1])
                    if data1[i][1][:-3] not in wires:
                        wires[data1[i][1][:-3]] = [data1[int(j)-1][1][:-3]]
                    else:
                        wires[data1[i][1][:-3]].append(data1[int(j)-1][1][:-3])
            initin.append(temp)
            initout.append(data1[i][1])
            nodes.append(list([data1[i][1], data1[i][2], len(k)]))
    
    inverse = dict() 
    for key in wires: 
        for item in wires[key]:
            if item not in inverse: 
                inverse[item] = [key] 
            else: 
                inverse[item].append(key)
    wires = inverse
    
    flatten_list = lambda y:[x for a in y for x in flatten_list(a)] if type(y) is list else [y]
    l = flatten_list(initin)
    for value in initout:
        if value not in l:
            outputs.append(value)
    
    conn = dict()
    for i in range(len(initin)):
        conn[i] = initin[i]
    
    no_of_nodes = len(conn)
    adj_mat = [[0 for i in range(no_of_nodes)] for j in range(no_of_nodes)]
    
    for value in initout:
        indx = initout.index(value)
        for node in conn:
            if value in conn[node]:
                adj_mat[node][indx] = 1
                adj_mat[indx][node] = 1
    
    f = open("adj_mat.txt", 'w')
    for i in range(len(adj_mat[0])):
        for j in range(len(adj_mat[0])):
            f.write(str(adj_mat[i][j]))
            f.write(" ")
        f.write("\n")
    f.close()
    
    f = open("nodes.txt", 'w')
    for i in nodes:
    	f.write(str(i))
    	f.write("\n")
    f.close()
    
    f = open("inputs.txt", 'w')
    for i in inputs:
    	f.write(str(i))
    	f.write("\n")
    f.close()
    
    f = open("outputs.txt", 'w')
    for i in outputs:
    	f.write(str(i))
    	f.write("\n")
    f.close()
    
    f = open("wires.txt", 'w')
    f.write(str(wires))
    f.close()
    
    return nodes, adj_mat
