# -*- coding: utf-8 -*-
"""
Created on Mon Oct  12 16:50:57 2020

@author: Rahul
"""

import random
import math
import time
import matplotlib 
import matplotlib.pyplot as plt 
from parse import netadj85

def check_if_done(polish_exp_temp, inorder, done, done_index):
    
    for i in range(len(done)):
        if (polish_exp_temp[i] in inorder):
            done_index = i + 1
        else:
            break

    return done_index

def post_to_inorder(polish_exp_temp,operators,operands):

    inorder = []
    num_stack = []
    char_stack = []
    num = 1
    done = [0]*len(polish_exp_temp)
    done_index = 0

    i = 0
    while(len(inorder)<len(polish_exp_temp)):

        x = polish_exp_temp[i]

        if( (x in operands) and (num == 1) ):
            inorder.append(x)
            num = 0
            i = check_if_done(polish_exp_temp,inorder,done,done_index)
            del num_stack[:]
            del char_stack[:]
        elif((x in operands) and (num == 0) ):
            num_stack.append(x)
            i = i + 1

        elif((x in operators) and ((len(num_stack) - 1) == (len(char_stack)))):
            inorder.append(x)
            num = 1
            i = check_if_done(polish_exp_temp,inorder,done,done_index)
            if(len(num_stack)>0):
                inorder.append(num_stack[0])
                num = 0
                i = check_if_done(polish_exp_temp,inorder,done,done_index)

            del num_stack[:]
            del char_stack[:]

        elif((x in operators) and ((len(num_stack) - 1) != (len(char_stack)))):
            char_stack.append(x)
            i = i + 1

    return inorder

class TreeNode:
    
    def __init__(self, x):
        
        self.val = x
        self.left = None
        self.right = None
        self.coord = None
        self.dim = None

class Solution:
    
    def buildTree(self, inorder, postorder):
        
        if not inorder or not postorder:
            return None
        
        root = TreeNode(postorder.pop())
        inorderIndex = inorder.index(root.val)

        root.right = self.buildTree(inorder[inorderIndex+1:], postorder)
        root.left = self.buildTree(inorder[:inorderIndex], postorder)

        return root

def get_coord(root, block_sizes, combined_size,combined_size_list, polish_exp_temp, co_ord, operands):

    if(root.val in operands):
        co_ord[root.val - 1] = root.coord

    if(root.left == None and root.right == None):
        return co_ord

    if(root.val[0] == 'H'):
        root.left.coord = root.coord
        root.right.coord = [root.coord[0], root.coord[1] + combined_size[polish_exp_temp.index(root.left.val)][1]]

        co_ord = get_coord(root.left, block_sizes, combined_size,combined_size_list, polish_exp_temp, co_ord, operands)
        co_ord = get_coord(root.right, block_sizes, combined_size, combined_size_list, polish_exp_temp, co_ord, operands)

    if(root.val[0] == 'V'):
        root.left.coord = root.coord
        root.right.coord = [root.coord[0] + combined_size[polish_exp_temp.index(root.left.val)][0], root.coord[1]]

        co_ord = get_coord(root.left, block_sizes, combined_size,combined_size_list, polish_exp_temp, co_ord, operands)
        co_ord = get_coord(root.right, block_sizes, combined_size,combined_size_list, polish_exp_temp, co_ord, operands)    

    return co_ord

def area_coord(polish_exp_temp, block_sizes):
    
    operands = []
    operators = ['H','V']
    for i in polish_exp_temp:
        if i in operators:
            continue
        else:
            operands.append(i)
        
    no_of_blocks = len(operands)
    co_ord = [0]*no_of_blocks
    stack = []
    size = []
    combined_size = []
    combined_size_list = []
    vcount = 0
    hcount = 0
    updated_operators = []
    updated_pol_exp = polish_exp_temp[:]
    i = 0
    while(i < len(polish_exp_temp)):
    
        if (polish_exp_temp[i] in operands):
            stack.append(block_sizes[(polish_exp_temp[i]-1)])
                
        elif (polish_exp_temp[i] in operators and polish_exp_temp[i] == 'V'):
            right = stack.pop()
            left = stack.pop()
            arr = vertical(left,right)
            size = arr[:]
            stack.append(arr[:])
            combined_size_list.append('V' + str(vcount))
            combined_size.append(arr)
            updated_operators.append(('V' + str(vcount)))
            updated_pol_exp[i] = 'V' + str(vcount)
            vcount = vcount + 1
            
        elif (polish_exp_temp[i] in operators and polish_exp_temp[i] == 'H'):
            top = stack.pop()
            bottom = stack.pop()
            arr = horizontal(top,bottom)
            size = arr[:]
            stack.append(arr[:])
            combined_size_list.append('H' + str(hcount))
            combined_size.append(arr)
            updated_operators.append(('H' + str(hcount)))
            updated_pol_exp[i] = 'H' + str(hcount)
            hcount = hcount + 1
        
        i = i+1
    
    final_combined_size = [0]*len(polish_exp_temp)

    for i in range(len(polish_exp_temp)):
        if(polish_exp_temp[i] in operands):
            final_combined_size[i] = block_sizes[polish_exp_temp[i] - 1]
        else:
            final_combined_size[i] = combined_size[combined_size_list.index(updated_pol_exp[i])]

    area = size[0]*size[1]
    inorder = post_to_inorder(updated_pol_exp, updated_operators, operands)
    yet_another_pol = updated_pol_exp[:]

    root = Solution().buildTree( inorder, yet_another_pol)
    root.dim = size[:]
    root.coord = [0,0]
    co_ord = [[0,0]]*len(polish_exp_temp)
    co_ord = get_coord(root, block_sizes, final_combined_size, combined_size_list, updated_pol_exp, co_ord, operands)

    return area,co_ord,size

def vertical(L,R):
    
    L_new = L[:]
    R_new = R[:]
    dim = []
    dim.append(L_new[0]+R_new[0])
    dim.append(max(L_new[1],R_new[1]))
    
    return dim

def horizontal(L,R):
    
    L_new = L[:]
    R_new = R[:]
    dim = []
    dim.append(max(L_new[0],R_new[0]))
    dim.append(L_new[1]+R_new[1])

    return dim

def input_func(filename):
    
    f = open(filename,'r')
    data = f.readlines()
    adj_matrix = []

    for i in data:
        temp = i.split()
        temp = [int(j) for j in temp]
        adj_matrix.append(temp)
    
    return adj_matrix

def move1(polish_exp):

    polish_exp_temp = polish_exp[:]
    len_exp = len(polish_exp_temp)
    
    operator = ['H','V']
    operators = []
    operands = []
    for i in polish_exp_temp:
        if i in operator:
            operators.append(i)
        else:
            operands.append(i)
    
    rand_no = random.randint(0,len(operands)-1)
    no1 = operands[rand_no]
    if (rand_no == len(operands)-1):
        no2 = operands[rand_no-1]
    else:
        no2 = operands[rand_no+1]
        
    for j in range(len_exp):
        if (polish_exp_temp[j] == no1):
            loc1 = j
        if (polish_exp_temp[j] == no2):
            loc2 = j    
            
    polish_exp_temp[loc1] = no2
    polish_exp_temp[loc2] = no1
            
    return polish_exp_temp

def move2(polish_exp):

    polish_exp_temp = polish_exp[:]
    len_chain = []
    loc = []
    i = 0

    while(i<len(polish_exp_temp)):

        if(polish_exp_temp[i] == 'V' or polish_exp_temp[i] == 'H' ):
            loc.append(i)
            len_chain.append(1)
            i = i +1

            if(i == len(polish_exp_temp) ):
                break
            while(polish_exp_temp[i] == 'V' or polish_exp_temp[i] == 'H' ):
                len_chain[len(loc) - 1] = len_chain[len(loc) - 1] + 1
                i = i + 1
                if(i == len(polish_exp_temp) ):
                    break
        else:
            i = i + 1

    len_loc = len(loc)
    rand_loc = 0

    if(len_loc>1):
        rand_loc = random.randint(0, len_loc-1)

    i = loc[rand_loc]
    while (i < (loc[rand_loc] + len_chain[rand_loc] )):
        if(polish_exp_temp[i] == 'V'):
            polish_exp_temp[i] = 'H'
        elif(polish_exp_temp[i] == 'H'):
            polish_exp_temp[i] = 'V'
        i = i + 1

    return polish_exp_temp

def move3(polish_exp):
    
    polish_exp_temp = polish_exp[:]
    len_exp = len(polish_exp_temp)

    operator = ['H','V']
    operand = range(1,len_exp+1)
    adjacent = []
    location = []

    for i in range(len_exp-1):
        temp_arr = []
        if(polish_exp_temp[i] in operator and polish_exp_temp[i+1] in operand):
            temp_arr.append(polish_exp_temp[i])
            temp_arr.append(polish_exp_temp[i+1])
            adjacent.append(temp_arr)
            location.append(i)
        elif(polish_exp_temp[i] in operand and polish_exp_temp[i+1] in operator):
            temp_arr.append(polish_exp_temp[i])
            temp_arr.append(polish_exp_temp[i+1])
            adjacent.append(temp_arr)
            location.append(i)

    len_adj = len(adjacent)
    rand_no = 0
    if(len_adj>1):
        rand_no = random.randint(0,len(adjacent)-1)
    
    swap_loc = location[rand_no]
    temp = polish_exp_temp[swap_loc]
    polish_exp_temp[swap_loc] = polish_exp_temp[swap_loc + 1]
    polish_exp_temp[swap_loc + 1] = temp

    return polish_exp_temp,swap_loc

def balloting_prop(polish_exp,swap_loc):

    operator = ['H','V']
    alp_count = 0
    num_count = 0
    i = 0
    flag = 0
    
    while(i < len(polish_exp)):
        if polish_exp[i] in operator:
            alp_count = alp_count + 1
        else:
            num_count = num_count + 1

        if (alp_count < num_count):
            i = i+1
        else:
            flag = 1

            return 1

    if (flag == 1):
        
        return 1
    
    return 0

def normality_prop(polish_exp):

    polish_exp_temp = polish_exp[:]
    len_exp = len(polish_exp_temp)
    
    for check in range(len_exp-1):
        if((polish_exp_temp[check] == 'H' and polish_exp_temp[check+1] == 'H') or 
           (polish_exp_temp[check] == 'V' and polish_exp_temp[check+1] == 'V')):
            return 1
            
    return 0

def move(polish_expression):

    polish_exp_temp = polish_expression[:]
    move_no = random.randint(1,3)

    if(move_no == 1):
        polish_exp_temp1 = move1(polish_exp_temp)
    elif (move_no == 2):
        polish_exp_temp1 = move2(polish_exp_temp)
    else:
        polish_exp_temp1, swap_loc = move3(polish_exp_temp)
        while (balloting_prop(polish_exp_temp1,swap_loc) == 1 
               or normality_prop(polish_exp_temp1) == 1):
            polish_exp_temp1, move_no = move3(polish_exp_temp)
    
    return polish_exp_temp1, move_no

def wirelength(adj_matrix, block_dimensions, node_coord):
    
    weight = 0
    n = len(adj_matrix[0])
    
    for i in range(n):

        x1 = node_coord[i][0] + (block_dimensions[i][0])/2
        y1 = node_coord[i][1] + (block_dimensions[i][1])/2

        for j in range(n):
            if(adj_matrix[i][j] !=0):
                x2 = node_coord[j][0] + (block_dimensions[j][0])/2
                y2 = node_coord[j][1] + (block_dimensions[j][1])/2
                dist = math.sqrt((x2-x1)**2 + (y2 - y1)**2)
                weight = weight + dist*adj_matrix[i][j]

    return weight

def cost_func_param(adj_matrix):
    
    cost_param = 0.5
    
    return cost_param

def cost_func(polish_expression, block_dimensions, adj_matrix):
    
    area, block_coord, size = area_coord(polish_expression[:], block_dimensions)
    wirelen = wirelength(adj_matrix, block_dimensions, block_coord)
    cost_param = cost_func_param(adj_matrix)
    cost = 12*area + cost_param*wirelen + 1.2*(size[1] - size[0])*(size[1] - size[0])

    return cost,size, area, block_coord
    
def annealing(adj_matrix, blocks, block_dimensions, noded):
    
    node_list_size = len(adj_matrix[0])
    len_pol_exp = 2*node_list_size - 1
    polish_expression = []
    
    j = 0
    for i in range(len_pol_exp):
        if (i%2 == 0 and i != 0 and i != 1 and i <= len_pol_exp//2):
            polish_expression.append('V')
        elif (i%2 == 0 and i != 0 and i != 1):
            polish_expression.append('H')
        elif (i == 0 or i == 1):
            polish_expression.append(i+1)
            j = 3
        else:
            polish_expression.append(j)
            j = j+1

    pol_exp_temp = polish_expression[:]
    loop = 0
    init_temp_arr = []
    cost_temp = 0
    size_temp = 0
    best_size = 0
    coord_temp = []

    while(loop < 5):

        pol_exp_temp, move_no = move(pol_exp_temp)

        cst, size, area_temp, coord_temp = cost_func(pol_exp_temp, block_dimensions, adj_matrix)
        init_temp_arr.append(cst)
        loop = loop + 1
    
    nd = dict()
    for i in range(len(noded)):
        nd[i] = noded[i][0][:-3]
    pol_exp = list()
    for i in range(len(pol_exp_temp)):
        if type(pol_exp_temp[i]) is not str:
            pol_exp.append(nd[pol_exp_temp[i]-1])
        else:
            pol_exp.append(pol_exp_temp[i])
    
    print("\n Initial Polish Expression ", pol_exp)
    print("\n Initial Size " + str(area_temp) +  " = "+ str(size[0]) +  "x" +str(size[1]))
    
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    nd = dict()
    for i in range(len(noded)):
        nd[i] = noded[i][0][:-3]
    number_of_colors = len(pol_exp_temp)
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]    

    for i in range(len(pol_exp_temp)):
        if type(pol_exp_temp[i]) is not str:
            if(pol_exp_temp[i] < ((len(pol_exp_temp) + 1)/2)):
                rect = matplotlib.patches.Rectangle((coord_temp[pol_exp_temp[i]-1][0], 
                                                     coord_temp[pol_exp_temp[i]-1][1]), 
                                                    block_dimensions[pol_exp_temp[i]-1][0], 
                                                    block_dimensions[pol_exp_temp[i]-1][1], 
                                                    facecolor = colors[i], edgecolor = '000000',
                                                    label = nd[pol_exp_temp[i]-1]) 

                ax.add_patch(rect) 
                ax.text(coord_temp[pol_exp_temp[i]-1][0] + 0.5, 
                        coord_temp[pol_exp_temp[i]-1][1] + 1,
                        nd[pol_exp_temp[i]-1], fontsize = 6)
    plt.xlim([0, size[0]+10]) 
    plt.ylim([0, size[1]+10]) 
    plt.title('Initial Floorplanning') 
    plt.savefig("Initial_Floorplanning",dpi=1000)
    plt.show()
        
    i = 0
    sum = 0
    while(i<4):
        sum = sum + abs(init_temp_arr[i+1] - init_temp_arr[i])
        i = i+1
        
    avg_cost = sum/4
    initial_temperature = -avg_cost/math.log(0.9)
        
    print ("\n Initial Temperature calculated:",initial_temperature)
    
    tempfact = 0.9995
    temperature = initial_temperature
    temp_iteration = 1
    
    polish_exp = polish_expression[:]
    polish_exp_temp = polish_exp[:]
    reject = 0
    temp_reject = 0
    
    cost, size, best_area, best_coord  = cost_func(polish_exp, block_dimensions,adj_matrix) # Initial cost (at t=0)
    cost_temp = 0
    size_temp = 0
    best_size = size
    best_cost = cost 
    best_polish_exp = polish_exp_temp[:]
    N = len(adj_matrix[0])
    no_of_moves = 0
    uphill  = 0
    arealist=[]
    costlist=[]
    
    timeout = time.time() + 3600
    while(temperature > (initial_temperature/75000) and time.time()<timeout): # Until the temperature reaches 0.5, keep iterating

        polish_exp_temp , move_no = move(polish_exp_temp)
        no_of_moves = no_of_moves + 1

        cost_temp, size_temp, area_temp, coord_temp = cost_func(polish_exp_temp, block_dimensions,adj_matrix)
        costlist.append(cost_temp)
        if(cost < best_cost):
            best_cost = cost
            best_size = size
            best_polish_exp = polish_exp[:]
            best_area = area_temp
            arealist.append(area_temp)
            best_coord = coord_temp[:]

        delta_cost = cost_temp - cost


        if(delta_cost <= 0):
            cost = cost_temp
            size = size_temp
            polish_exp = polish_exp_temp[:]
            reject = 0
            temp_reject = 0
        elif (math.exp(-(delta_cost/temperature)) > random.uniform(0,1)):
            cost = cost_temp
            size = size_temp
            polish_exp = polish_exp_temp[:]
            reject = 0
            temp_reject = 0
            uphill = uphill + 1
        else:
            reject = reject + 1
        if(uphill > N or no_of_moves>2*N):
                
            uphill = 0
            no_of_moves = 0
            temp_reject = temp_reject + 1
            temperature = temperature*math.pow(tempfact,temp_iteration) 
            temp_iteration = temp_iteration + 1 
    plt.figure(figsize=(16,9))
    plt.plot(arealist)
    plt.xlabel('Accepted temperature')
    plt.ylabel('Area')
    plt.show()
    plt.figure(figsize=(16,9))
    plt.plot(costlist)
    plt.xlabel('Iterations')
    plt.ylabel('Cost')
    plt.savefig("Floorplanning_Cost_vs_Iterations.png",dpi=1000)
    plt.show()

    return best_polish_exp, best_area, best_coord, best_size, temperature
    
def main():
    
    print ("\n Enter the name of the file containing the required netlist")
    filename = input(" ")
    
    nodes, adj_matrix = netadj85(filename)
    
    block_dim = dict()
    block_dim.update({'not': [1,3]})
    block_dim.update({'and': [3,3]})
    block_dim.update({'nand': [2,3]})
    block_dim.update({'nor': [2,3]}) 
    block_dim.update({'or': [3,2]})
    block_dim.update({'xnor': [3,3]})
    block_dim.update({'buff': [1,2]})
    block_dim.update({'xor': [3,4]})
    
    block_names = range(1,len(nodes)+1)
    block_dimensions = [0]*len(adj_matrix[0])
    
    noded = dict()
    gates = list()
    for i in range(len(nodes)):
        noded[i] = nodes[i]
        gates.append(nodes[i][1])
    
    j = 0
    for i in gates:
        block_dimensions[j] = [0, 0]
        # Consider random block dimensions for simplicity
        block_dimensions[j][0] = random.randint(1, 4)
        block_dimensions[j][1] = random.randint(1, 4)
        j = j+1
        
    best_polish_exp, best_area, best_coord, best_size, final_temperature = annealing(adj_matrix, block_names, block_dimensions, noded)    
    
    nd = dict()
    for i in range(len(noded)):
        nd[i] = noded[i][0][:-3]
    
    gates = dict()
    j = 0
    for i in nd.values():
        gates[i] = block_dimensions[j]
        j += 1
    f = open("gates.txt",'w')
    f.write(str(gates))
    f.close()
    
    pol_exp = list()
    for i in range(len(best_polish_exp)):
        if type(best_polish_exp[i]) is not str:
            pol_exp.append(nd[best_polish_exp[i]-1])
        else:
            pol_exp.append(best_polish_exp[i])
    
    f = open("inputs.txt",'r')
    data = f.readlines()
    f.close()
    inputs = dict()
    for i in range(len(data)):
        inputs[data[i].split("\n")[0][:-3]] = [0, i+30]
    f = open("inputs_coord.txt",'w')
    f.write(str(inputs))
    f.close()
    
    f = open("outputs.txt",'r')
    data = f.readlines()
    f.close()
    outputs = dict()
    for i in range(len(data)):
        outputs[data[i].split("\n")[0][:-3]] = [i+35, 0]
    f = open("outputs_coord.txt",'w')
    f.write(str(outputs))
    f.close()
    
    coordinates = dict()
    coordinates.update(inputs)
    coordinates.update(outputs)
    for i in range(len(best_polish_exp)):
        if type(best_polish_exp[i]) is not str:
            coordinates[pol_exp[i]] = best_coord[best_polish_exp[i]-1]
    f = open("floorplan_coord.txt",'w')
    f.write(str(coordinates))
    f.close()
    
    print("\n Best Polish Expression: ", pol_exp)
    print("\n Best Size: " + str(best_area) +  " = "+ str(best_size[0]) +  "x" +str(best_size[1]))
    print("\n Final Temperature: ", final_temperature)
    
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
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
                                                    facecolor = colors[i], edgecolor = '000000',
                                                    label = nd[best_polish_exp[i]-1])
                ax.add_patch(rect) 
                ax.text(best_coord[best_polish_exp[i]-1][0] + 0.5, 
                        best_coord[best_polish_exp[i]-1][1] + 1,
                        nd[best_polish_exp[i]-1], fontsize = 6)
    plt.xlim([0, best_size[0]+10]) 
    plt.ylim([0, best_size[1]+10]) 
    plt.title('Final Floorplanning') 
    plt.savefig("Final_Floorplanning",dpi=1000)
    plt.show()

if __name__ == '__main__':
    main()
