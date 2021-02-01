# -*- coding: utf-8 -*-
"""
Created on Sun Oct  25 23:45:46 2020

@author: Rahul
"""

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import random
import math

def interconnects_length(wires, coordinates):
    
    wire_length = 0
    for k, v in wires.items():
        start_point = coordinates[k]
        
        for i in v:
            end_point = coordinates[i]
            wire_length = wire_length + abs(start_point[0] - end_point[0]) + abs(start_point[1] - end_point[1])
            
    return wire_length

def pinout_assign(max_x, max_y, pinouts, coordinates):
    
    pinout_empty_coordinates=[]
    for i in range(0, max_x, max_x - 1) :
        for j in range(0, max_y, 10):
            c = [i, j]
            if c not in pinout_empty_coordinates:
                pinout_empty_coordinates.append(c)
            
    for i in range(0, max_y, max_y - 1) :
        for j in range(0, max_x, 10):
            c=[j, i]
            if c not in pinout_empty_coordinates:
                pinout_empty_coordinates.append(c)
                
    input_coordinates={}
    for i in pinouts:
        input_coordinates[i] = random.choice(pinout_empty_coordinates)
        pinout_empty_coordinates.remove(input_coordinates[i])
    
    for k, v in input_coordinates.items():
        coordinates[k]=v
        
    return pinout_empty_coordinates, input_coordinates, pinout_empty_coordinates, coordinates

def moving_block(l_coordinates, l_max_x, l_max_y, l_occupied_coordinates, pinouts, gates):
    
    end = 1
    while(end):
        x = 0
        while(x==0):
            b = random.choice(list(l_coordinates))
            x = 1
            if b in pinouts:
                x = 0
        
        lst = l_coordinates[b]
        l_coordinates.pop(b)
        l_occupied_coordinates = occupied_coordinates_gen(l_coordinates, gates)
        l_max_x, l_max_y = boundaries(l_coordinates, gates)
        l_coordinates[b] = lst
        empty_coordinates = empty_coordinates_gen(int(l_max_x), int(l_max_y), l_occupied_coordinates)
        c = random.choice(empty_coordinates)
        l_coordinates[b] = c
        end = 0

    return l_coordinates


def empty_coordinates_gen(max_x, max_y, occupied_coordinates):
    
    all_coordinates=[]
    for i in range(7, max_x - 6, 7):
        for j in range(7, max_y - 6, 7):
            all_coordinates.append([i, j])
            
    t_occupied_coordinates=[]
    for i in occupied_coordinates:
        t_occupied_coordinates.append(tuple(i))
    t_occupied_coordinates = tuple(t_occupied_coordinates)
    
    t_all_coordinates=[]
    for i in all_coordinates:
        t_all_coordinates.append(tuple(i))
    t_all_coordinates = tuple(t_all_coordinates)
            
    t_res = list(set(t_all_coordinates) - set(t_occupied_coordinates))
    res=[]
    for i in t_res:
        res.append(list(i))
        
    return res


def exchange_blocks(l_coordinates, pinouts):
    
    k1 = 0
    k2 = 0
    while(k1 == 0 and k2 == 0):
        key1, key2 = random.sample(list(l_coordinates), 2)
        k1 = 1
        k2 = 1
        if key1 in pinouts:
            k1, k2 = 0, 0
        if key2 in pinouts:
            k1, k2 = 0, 0
    l_coordinates[key1], l_coordinates[key2] = l_coordinates[key2], l_coordinates[key1]
    
    return l_coordinates

    
def boundaries(l_coordinates, l_gates, pinouts):
    
    l_max_x, l_max_y = 0, 0
    for k, v in l_coordinates.items():
        if k not in pinouts:
            if(v[0]>=l_max_x - l_gates[k][0]):
                l_max_x = v[0]+l_gates[k][0]
            if(v[1]>=l_max_y - l_gates[k][1]):
                l_max_y = v[1]+l_gates[k][1]
            
    return l_max_x + 7, l_max_y + 7


def occupied_coordinates_gen(coordinates, gates):
    
    occupied_coordinates=[]
    for k, v in coordinates.items():
        occupied_coordinates.append(v)
    
    return occupied_coordinates


def save_dict_to_file(dic, file_name):
    
    f = open(file_name,'w')
    f.write(str(dic))
    f.close()

def load_dict_from_file(file_name):
    
    f = open(file_name,'r')
    data = f.read()
    f.close()
    return eval(data)

def main():

    coordinates = load_dict_from_file('floorplan_coord.txt')
    gates = load_dict_from_file('gates.txt')
    inputs = load_dict_from_file('inputs_coord.txt')
    outputs = load_dict_from_file('outputs_coord.txt')
    wires=load_dict_from_file('wires.txt')
    
    pinouts=[]
    for i in outputs:
        pinouts.append(i)
    for i in inputs:
        pinouts.append(i)
    
    y = 0
    end = 1
    i = 0
    
    while(end):
        increment = 0
        lst=[]
        for k, v in coordinates.items():
            if(v[1]==y):
                lst.append(k)
                increment = 1
        
        
        if(increment==1):
            i = i + 1
            for k1, v1 in coordinates.items():
                if k1 in lst:
                    v1[1]=i*7
                elif(y<v1[1]):
                    v1[1]=v1[1]+7
            y = y + 7
            
                   
        y = y + 1
        max_x, max_y = boundaries(coordinates, gates, pinouts)
        if(y>max_y):
            end = 0
    
    x = 0      
    end = 1
    i = 0     
    while(end):
        increment = 0
        lst=[]
        for k, v in coordinates.items():
            if(v[0]==x):
                lst.append(k)
                increment = 1
        
        if(increment==1):
            i = i + 1
            for k1, v1 in coordinates.items():
                if k1 in lst:
                    v1[0]=i*7
                elif(x<v1[0]):
                    v1[0]=v1[0]+7
            x = x + 7
            
        x = x + 1
        max_x, max_y = boundaries(coordinates, gates, pinouts)
        if(x>max_x):
            end = 0   
            
    occupied_coordinates = occupied_coordinates_gen(coordinates, gates)
    max_x, max_y = boundaries(coordinates, gates, pinouts)
    pinout_empty_coordinates, input_coordinates, pinout_empty_coordinates, coordinates = pinout_assign(max_x, max_y, pinouts, coordinates)
        
    x=[]
    y=[]
    a = 1
    T = 400000
    new_coordinates = coordinates
    new_area = max_x*max_y
    new_max_x, new_max_y = max_x, max_y
    new_occupied_coordinates = occupied_coordinates
    
    wire_length = interconnects_length(wires, coordinates)
    new_cost = new_area + wire_length
    min_cost = new_cost
    x1 = new_cost
    print(" Initial cost=",new_cost)
    
    while(T>0.1):
        i = 0
        while(i<5*len(coordinates)):
            i = i + 1
            m = random.choice([1, 2])
            if(m==1):
                t_coordinates = moving_block(new_coordinates, new_max_x, new_max_y, new_occupied_coordinates, pinouts, gates)
            elif(m==2):
                t_coordinates = exchange_blocks(coordinates, pinouts)
            
            t_max_x, t_max_y = boundaries(t_coordinates, gates, pinouts)
            t_area = t_max_x*t_max_y
            t_occupied_coordinates = occupied_coordinates_gen(new_coordinates, gates)
            
            t_wire_length = interconnects_length(wires, t_coordinates)
            t_cost = t_area + t_wire_length
            
            if(t_cost<new_cost):
                new_coordinates = t_coordinates
                new_max_x, new_max_y = boundaries(new_coordinates, gates, pinouts)
                new_area = new_max_x*new_max_y
                new_wire_length = t_wire_length
                new_cost = new_area + new_wire_length
                new_occupied_coordinates = t_occupied_coordinates
                
                if(min_cost>new_cost):
                    best_max_x, best_max_y = new_max_x, new_max_y
                    min_cost = new_cost
                    save_dict_to_file(new_coordinates,'placement_coord.txt')
    
            else:
                r = random.randrange(0, 1)
                if(r<math.exp((-(t_cost - new_cost)/T))):
                    new_cost = t_cost
                    new_coordinates = t_coordinates
                    new_occupied_coordinates = t_occupied_coordinates
            
            if(len(y)>1):
                if(y[-1]!=new_cost):
                    y.append(new_cost)
                    x.append(a)
                    a = a + 1
            else:
                y.append(new_cost)
                x.append(a)
                a = a + 1
            
        T = 0.85*T 
    
    coordinates = load_dict_from_file('placement_coord.txt')
    
    print("\n Final cost=",min_cost)
    x2 = min_cost
    print("\n The Final Cost is",100*(x1 - x2)/x1,"% less than that of Initial cost")
    pinout_empty_coordinates, input_coordinates, pinout_empty_coordinates, coordinates = pinout_assign(best_max_x, best_max_y, pinouts, coordinates)
    save_dict_to_file(coordinates,'placement_coord.txt')
    plt.figure(figsize=(10, 6), dpi = 80)  
    plt.plot(x, y) 
    plt.xlabel('Iteration') 
    plt.ylabel('Cost') 
    plt.title('Cost graph') 
    plt.savefig("Placement_Cost_vs_Iteraions.png",dpi = 1000)
    plt.show()
    
    save_dict_to_file(pinouts,'pinouts.txt')
    
    plt.figure(figsize=(best_max_x/15, best_max_y/15))
    currentAxis = plt.gca()
    plt.xlim([0, best_max_x])
    plt.ylim([0, best_max_y])
    plt.title('Final Placement') 
    number_of_colors = 72
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(8)])
                 for i in range(number_of_colors)]
    j = 0
    for i in coordinates:
      if i in pinouts:
          a = coordinates[i][0]
          b = coordinates[i][1]
          currentAxis.add_patch(Rectangle(( a, b),1, 1, alpha = 1, fc='black'))
          plt.text(a, b + 1.5 ,i, fontsize = 3)
      else:
          a = coordinates[i][0]
          b = coordinates[i][1]
          currentAxis.add_patch(Rectangle(( a, b),float(gates[i][0]),float(gates[i][1]),alpha = 0.6, fc = color[j],ec="black",lw = 0.5))
          plt.text(a + 0.15, b + 0.15 ,i, fontsize = 3)
          j+=1 
      
    plt.savefig("Final_Placement.png",dpi = 1000)
    plt.show()


if __name__ == '__main__':
    main()
