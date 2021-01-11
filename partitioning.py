# -*- coding: utf-8 -*-
"""
Created on Fri Sep  25 15:26:05 2020

@author: Rahul
"""

import numpy as np
import random
import networkx as nx
from parse import netadj85
import matplotlib.pyplot as plt

def cut_size(n1, n2, A):
    
    count = 0
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] == 1:
                if (i in n1 and j in n2) or (i in n2 and j in n1):
                    count+=1
    return (count)

def bestswap(n1 ,n2, A, pairs):
    
    mark = []
    partition = []
    cut_s = []
    while(len(mark) != pairs-1):
        r_best, ij, part = [], [], []
        r_old = cut_size(n1, n2, A)
        for i in range(len(n1)):
            for j in range(len(n2)):
                if ([n1[i],n2[j]] not in mark and ([n2[j],n1[i]] not in mark)):
                    n11, n22 = n1.copy(), n2.copy()
                    n11[i] = n2[j]
                    n22[j] = n1[i]
                    del_R = r_old - cut_size(n11, n22, A)
                    r_best.append(del_R)
                    part.append([n11, n22])
                    ij.append([n11[i],n22[j]])
        a = np.argmax(r_best)
        c_part = part[a]
        partition.append(c_part)
        mark.append(ij[a])
        cut_s.append(cut_size(c_part[0], c_part[1], A))
        n1, n2 = c_part[0], c_part[1]
        
    return(cut_s[np.argmin(cut_s)], partition[np.argmin(cut_s)])
    
def kernighanlin(n1, n2, A, pairs):
    
    cs = []
    for i in range(1):
        CutSize, partition = bestswap(n1, n2, A, pairs)
        n1 = partition[0]
        n2 = partition[1]
        cs.append(CutSize)
        if len(cs) >= 10:
            ts = cs[-5:]
            if (ts[0]==ts[1]==ts[2]==ts[3]==ts[4]):
                break
            
    return(CutSize, partition)

def for_pos(p, count1, positions):
    
    n=len(p)
    p1,p2,p3,p4 = p[0:n//4],p[n//4:n//2],p[n//2:3*n//4],p[3*n//4:]
    count2=0
    for i in p1:
        positions[i]=[count1,count2]
        count1+=1
        count2+=1
    for j in p2:
        positions[j]=[count1,count2]
        count1-=1
        count2+=1
    for k in p3:
        positions[k]=[count1,count2]
        count1-=1
        count2-=1
    for l in p4:
        positions[l]=[count1,count2]
        count1+=1
        count2-=1
        
    return positions

def main():
        
    print ("Enter the name of the file containing the required netlist: ")
    filename = input("\n")
    
    nodes, A = netadj85(filename)
    
    noded = dict()
    for i in range(len(nodes)):
        noded[i] = nodes[i]
    
    n = len(A[0])
    v = [ i for i in range(n)]
    random.shuffle(v)
    cut = int(n/2)
    n1, n2 = np.sort(v[:cut]), np.sort(v[cut:])
    pairs = len(n1)*len(n2)
    n11 = [0]*len(n1)
    n22 = [0]*len(n2)
    j = 0
    for i in n1:
    	n11[j] = nodes[i][0]
    	j = j+1
    j = 0
    for i in n2:
    	n22[j] = nodes[i][0]
    	j = j+1
    
    print("\nInitial Cut size is : {}".format(cut_size(n1, n2, A)))
    print("Initial Partition 1 : {}".format(n11))
    print("Initial Partition 2 : {}".format(n22))
    
    c, p = kernighanlin(n1, n2, A, pairs)
    p11, p22 = np.sort(p[0]), np.sort(p[1])
    p1 = [0]*len(p11)
    p2 = [0]*len(p22)
    j = 0
    for i in p11:
    	p1[j] = nodes[i][0]
    	j = j+1
    j = 0
    for i in p22:
    	p2[j] = nodes[i][0]
    	j = j+1
    
    print("Final Cut size is : {}".format(c))
    print("Final Partition 1 : {}".format(p1))
    print("Final Partition 2 : {}".format(p2))
    
    nd = dict()
    for i in range(len(noded)):
        nd[i] = noded[i][0][:-3]
        
    G = nx.from_numpy_matrix(np.asarray(A))
    for n in G.nodes():
        G.nodes[n]['color'] = 'y' if n in p11 else 'g'
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    positions = dict()
    positions = for_pos(p11, 5, positions)
    positions = for_pos(p22, 30, positions)
    nx.draw_networkx(G, positions, with_labels=True, node_color=colors, 
                     labels=nd)
    plt.savefig("Initial_Partitoning.png",dpi = 1000)
    plt.show()
    
    G = nx.from_numpy_matrix(np.asarray(A))
    for n in G.nodes():
        G.nodes[n]['color'] = 'y' if n in n1 else 'g'
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    positions = dict()
    positions = for_pos(n1, 5, positions)
    positions = for_pos(n2, 30, positions)
    nx.draw_networkx(G, positions, with_labels=True, node_color=colors, 
                     labels=nd)
    plt.savefig("Final_Partioning.png",dpi = 1000)
    plt.show()
    
if __name__ == '__main__':
    main()
