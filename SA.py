import random
import math
import time
import matplotlib 
import matplotlib.pyplot as plt 
from parse import netadj

def annealing(adj_matrix, blocks, block_dimensions):
	node_list_size = len(adjmat[0])
	len_pol_exp = 2*node_list_size - 1
	polish_expression = []
	j = 0
	for i in range(len_pol_exp):
		if (i%2 == 0 and i != 0 and i != 1):
			polish_expression.append('V')
		elif (i == 0 or i == 1):
			polish_expression.append(i+1)
			j = 3
		else:
			polish_expression.append(j)
			j = j+1

	init_temp = []
	cost_temp = 0
	size_temp = 0
	best_size = 0
	coord_temp = []
	
	### Code remaining to be done
	
	return best_polish_expression, best_area, best_coordinates, best_size


nodes, adjmat = netadj(filename)
block_dim = dict()
block_dim.update({'not': [1,1]})
block_names = range(1,len(nodes)+1)
block_dimensions = [0]*len(adjmat[0])

j = 0
for i in nodes:
	block_dimensions[j] = block_dim[i]
	j = j+1
	
# simulated annealing algorithm
best_polish_expression, best_area, best_coordinates, best_size = annealing(adj_mat, block_names, block_dimensions)    

print(best_polish_exp)
fig = plt.figure() 

number_of_colors = len(best_polish_exp)
colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
		 for i in range(number_of_colors)]    

for i in range(len(best_polish_exp)):
    if type(best_polish_exp[i]) is not str:
    	if(best_polish_exp[i] < ((len(best_polish_exp) + 1)/2)):
    		rect = matplotlib.patches.Rectangle((best_coord[best_polish_exp[i]-1][0], 
    									best_coord[best_polish_exp[i]-1][1]), 
    								   block_dimensions[best_polish_exp[i]-1][0], 
    								   block_dimensions[best_polish_exp[i]-1][1], 
    								   color = colors[i], edgecolor = 'black') 
    		ax.add_patch(rect) 
plt.xlim([0, best_size[0]]) 
plt.ylim([0, best_size[1]]) 
plt.show()
