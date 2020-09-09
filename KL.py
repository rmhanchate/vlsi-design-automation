import numpy as np
import random
import networkx as nx

def cut_size(n1, n2):
    rold = 0
    for i in n1:
        for j in n2:
            if A[i][j] == 1:
                rold = rold + 1
    return (rold)

def KLA(n1, n2):
    cs = []
    for i in range(1):
        cutsize, partition = best_swap(n1, n2)
        n1 = partition[0]
        n2 = partition[1]
        cs.append(cutsize)
				
				
				
				
    return(CutSize, partition)

def main():
	filename = input("\n")
	f = open(filename,'r')
	data = f.readlines()
	adjmat = []
	for i in data:
		temp = i.split()
		temp = [int(j) for j in temp]
		adjmat.append(temp)
	n = int(input("\n"))
	non = len(adjmat[0])
	al = [ i for i in range(non)]
