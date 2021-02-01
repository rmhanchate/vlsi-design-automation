# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 07:06:50 2020

@author: Rahul
"""

import os
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from timeit import default_timer as timer

start = timer()

def save_dict_to_file(dic, file_name):
    
    f = open(file_name,'w')
    f.write(str(dic))
    f.close()

def load_dict_from_file(file_name):
    
    f = open(file_name,'r')
    data = f.read()
    f.close()
    
    return eval(data)

def boundaries(llayer_coordinates, llayer_gates, pinouts):
    
    llayer_max_x, llayer_max_y = 0, 0
    for k, v in llayer_coordinates.items():
        if k not in pinouts:
            if(v[0]>=llayer_max_x - llayer_gates[k][0]):
                llayer_max_x = v[0]+llayer_gates[k][0]
            if(v[1]>=llayer_max_y - llayer_gates[k][1]):
                llayer_max_y = v[1]+llayer_gates[k][1]
            
    return llayer_max_x + 7, llayer_max_y + 7

def retrace(source_lee, target_lee, path_num, i):
    
    i = i - 1
    p = target_lee
    path=[]
    h, v = 0, 1
    
    while(p != source_lee):
        path.insert(0, p)
        m1=[p[0]+1, p[1]]
        m2=[p[0]-1, p[1]]
        m3=[p[0],p[1]+1]
        m4=[p[0],p[1]-1]
        lst={}
        x = 0
        
        for j in path_num[i]:
            x+=1
            if((j==m1 or j==m2 )):
                lst[12]=j
                
            elif((j==m3 or j==m4 )):
                lst[34]=j
            
            if(len(lst)==2):
                i = i - 1
                if(h==1):
                    p = lst[12]
                    h, v = 1, 0
                    break
                elif(v==1):
                    p = lst[34]
                    h, v = 0, 1
                    break
            elif(x==len(path_num[i])):
                i = i - 1
                for key, value in lst.items():
                    if(key==12):
                        p = value
                        h, v = 1, 0
                        break
                    elif(key==34):
                        p = value
                        h, v = 0, 1
                        break
                
    path.insert(0, source_lee)      
    
    return path

def layer_separation(path, target_num, metal1, metal2, m12c):

    i = 1
    while(i<len(path)-1):
        if(path[i][1]==path[i - 1][1]):
            if(i==1 and path[i][0]>path[i - 1][0]):
                try:
                    metal1[2].append(path[i - 1])
                except KeyError:
                    metal1[2]=[]
                    metal1[2].append(path[i - 1])
            
            if(i==1):
                if(target_num!=1 and path[i][0]<path[i - 1][0]):
                    try:
                        m12c[6].append(path[i - 1])
                    except KeyError:
                        m12c[6]=[] 
                        m12c[6].append(path[i - 1])

                elif(target_num!=1 and path[i][0]>path[i - 1][0]):
                    try:
                        m12c[4].append(path[i - 1])
                    except KeyError:
                        m12c[4]=[] 
                        m12c[4].append(path[i - 1])
            
            if(path[i][1]==path[i + 1][1]):
                try:
                    metal1[2].append(path[i])
                except KeyError:
                    metal1[2]=[]
                    metal1[2].append(path[i])
                    
            elif(path[i][0]>path[i - 1][0] and path[i][1]>path[i + 1][1]):
                try:
                    m12c[6].append(path[i])
                except KeyError:
                    m12c[6]=[]
                    m12c[6].append(path[i])
                    
            elif(path[i][0]>path[i - 1][0] and path[i][1]<path[i + 1][1]):
                try:
                    m12c[3].append(path[i])
                except KeyError:
                    m12c[3]=[]
                    m12c[3].append(path[i])

            elif(path[i][0]<path[i - 1][0] and path[i][1]<path[i + 1][1]):
                try:
                    m12c[4].append(path[i])
                except KeyError:
                    m12c[4]=[]
                    m12c[4].append(path[i])

            elif(path[i][0]<path[i - 1][0] and path[i][1]>path[i + 1][1]):
                try:
                    m12c[5].append(path[i])
                except KeyError:
                    m12c[5]=[]
                    m12c[5].append(path[i])
             
            if(i==len(path)-2 and path[i][1]>path[i + 1][1]):
                try:
                    metal2[1].append(path[i + 1])
                except KeyError:
                    metal2[1]=[]
                    metal2[1].append(path[i + 1])

            elif(i==len(path)-2 and path[i][0]>path[i + 1][0]):
                try:
                    metal1[2].append(path[i + 1])
                except KeyError:
                    metal1[2]=[]
                    metal1[2].append(path[i + 1])
        
        elif(path[i][0]==path[i - 1][0]):
            if(i==1 and path[i][1]>path[i - 1][1] and target_num==1):
                try:
                    metal2[1].append(path[i - 1])
                except KeyError:
                    metal2[1]=[]
                    metal2[1].append(path[i - 1])
            if(i==1):
                if(target_num!=1 and path[i][1]<path[i - 1][1]):
                    try:
                        m12c[5].append(path[i - 1])
                    except KeyError:
                        m12c[5]=[] 
                        m12c[5].append(path[i - 1])
                elif(target_num!=1 and path[i][1]>path[i - 1][1]):
                    try:
                        m12c[3].append(path[i - 1])
                    except KeyError:
                        m12c[3]=[] 
                        m12c[3].append(path[i - 1])
                    
            if(path[i][0]==path[i + 1][0]):
                try:
                    metal2[1].append(path[i])
                except KeyError:
                    metal2[1]=[]  
                    metal2[1].append(path[i])

            elif(path[i][0]>path[i + 1][0] and path[i][1]>path[i - 1][1]):
                try:
                    m12c[6].append(path[i])
                except KeyError:
                    m12c[6]=[] 
                    m12c[6].append(path[i])

            elif(path[i][0]>path[i + 1][0] and path[i][1]<path[i - 1][1]):
                try:
                    m12c[3].append(path[i])
                except KeyError:
                    m12c[3]=[]
                    m12c[3].append(path[i])

            elif(path[i][0]<path[i + 1][0] and path[i][1]<path[i - 1][1]):
                try:
                    m12c[4].append(path[i])
                except KeyError:
                    m12c[4]=[]
                    m12c[4].append(path[i])

            elif(path[i][0]<path[i + 1][0] and path[i][1]>path[i - 1][1]):
                try:
                    m12c[5].append(path[i])
                except KeyError:
                    m12c[5]=[]
                    m12c[5].append(path[i])
                
            if(i==len(path)-2 and path[i][1]>path[i + 1][1]):
                try:
                    metal2[1].append(path[i + 1])
                except KeyError:
                    metal2[1]=[]  
                    metal2[1].append(path[i + 1])

            elif(i==len(path)-2 and path[i][0]>path[i + 1][0]):
                try:
                    metal1[2].append(path[i + 1])
                except KeyError:
                    metal1[2]=[]
                    metal1[2].append(path[i + 1])
                    
        i = i + 1

    return metal1, metal2, m12c

def wave_propagation(source_lee, target_lee, t_m1_bc, t_m2_bc):
    
    if(source_lee[0]>target_lee[0]):
        rt_b = source_lee[0]+10
        lt_b = target_lee[0]-10
    else:
        rt_b = target_lee[0]+10
        lt_b = source_lee[0]-10            
    
    if(source_lee[1]>target_lee[1]):
        ur_b = source_lee[1]+10
        lr_b = target_lee[1]-10
    else:
        ur_b = target_lee[1]+10
        lr_b = source_lee[1]-10
                    
    path_num={}
    i = 0
    target='false'
    while(target=='false' and i<=(ur_b - lr_b + rt_b - lt_b - 1)):
        if(i==0):
            path_num[i]=[]
            if(len(source_lee)>2):
                for s1 in source_lee:
                    path_num[i].append(s1)                
            else:
                path_num[i].append(source_lee)
                
        path_num[i + 1]=[]
        for k in path_num[i]:
            n=[k[0]+1, k[1]]
            if(n[0]>=lt_b and n[1]>=lr_b and n[0]<=rt_b and n[1]<=ur_b):
                if(n==target_lee):
                    target='true'
                    break
                if n not in t_m1_bc:
                    path_num[i + 1].append(n)
                    t_m1_bc.append(n)

            n=[k[0]-1, k[1]]
            if(n[0]>=lt_b and n[1]>=lr_b and n[0]<=rt_b and n[1]<=ur_b):
                if(n==target_lee):
                    target='true'
                    break
                if n not in t_m1_bc:
                    path_num[i + 1].append(n)
                    t_m1_bc.append(n)
        
            n=[k[0],k[1]+1]
            if(n[0]>=lt_b and n[1]>=lr_b and n[0]<=rt_b and n[1]<=ur_b):
                if(n==target_lee):
                    target='true'
                    break
                if n not in t_m2_bc:
                    path_num[i + 1].append(n)
                    t_m2_bc.append(n)

            n=[k[0],k[1]-1]
            if(n[0]>=lt_b and n[1]>=lr_b and n[0]<=rt_b and n[1]<=ur_b):
                if(n==target_lee):
                    target='true'
                    break
                if n not in t_m2_bc:
                    path_num[i + 1].append(n)
                    t_m2_bc.append(n)
            
        i+=1   
        
    return path_num, target, i

def routing(connection_wire, t_m1_bc, t_m2_bc, target_num, metal1, metal2, m12c, pins, pinouts): 
    
    d_min = float('inf')  
    
    if(target_num==1):
        for i in pins[connection_wire[0]]:
            for j in pins[connection_wire[1]]:
                d = abs(i[0]-j[0])+abs(i[1]-j[1])
                if(d<d_min):
                    source_lee, target_lee = i, j
                    d_min = d
    else:
        for i in connection_wire[0]:
            for j in pins[connection_wire[1]]:
                d = abs(i[0]-j[0])+abs(i[1]-j[1])
                if(d<d_min):
                    source_lee, target_lee = i, j
                    d_min = d     
    path_num, target, i = wave_propagation(source_lee, target_lee, t_m1_bc, t_m2_bc)
    
    if(target=='true'):
        path = retrace(source_lee, target_lee, path_num, i)
        path_num={}
        metal1, metal2, m12c = layer_separation(path, target_num, metal1, 
                                                metal2, m12c)
        for v1 in pins.values():
            if source_lee in v1:
                if connection_wire[0] not in pinouts:
                    v1.remove(source_lee)
            elif target_lee in v1:
                if connection_wire[1] not in pinouts:
                    v1.remove(target_lee)
        
        return metal1, metal2, m12c, target, path
    
    else:
        metal1={}
        metal2={}
        m12c={}
        path=[]
        
        return metal1, metal2, m12c, target, path
    
def main():
    
    pinouts = load_dict_from_file('pinouts.txt')
    coordinates = load_dict_from_file('placement_coord.txt')
    gates = load_dict_from_file('gates.txt')
    wires = load_dict_from_file('wires.txt')
    
    max_x, max_y = boundaries(coordinates, gates, pinouts)    
    cost = max_x*max_y
    blocked_coordinates=[]
    
    for i in coordinates:
        if i not in pinouts:
            j = gates[i][0]
            while(j>=0):
                k = gates[i][1]
                while(k>=0):
                    c=[coordinates[i][0]+j, coordinates[i][1]+k]
                    if c not in blocked_coordinates:
                        blocked_coordinates.append(c)
                    k = k - 1
                j = j - 1
        else:
            blocked_coordinates.append(coordinates[i])
    
    save_dict_to_file(blocked_coordinates,'blocked_coordinates.txt')  
    blocked_coordinates=[] 
         
    m1_bc = load_dict_from_file('blocked_coordinates.txt')
    save_dict_to_file(m1_bc,'m1_bc.txt')
    
    m2_bc = load_dict_from_file('blocked_coordinates.txt')
    save_dict_to_file(m2_bc,'m2_bc.txt')
    
    m3_bc = load_dict_from_file('blocked_coordinates.txt')
    save_dict_to_file(m3_bc,'m3_bc.txt')
    
    m4_bc = load_dict_from_file('blocked_coordinates.txt')
    save_dict_to_file(m4_bc,'m4_bc.txt')
    
    
    pins={}
    
    for i in coordinates:
        if i not in pinouts:
            pins[i]=[]
            for j in range(coordinates[i][0]+1, coordinates[i][0]+gates[i][0]):
                c=[j, coordinates[i][1]]
                pins[i].append(c)
            for j in range(coordinates[i][1]+1, coordinates[i][1]+gates[i][1]):
                c=[coordinates[i][0],j]
                pins[i].append(c)
            for j in range(coordinates[i][0]+1, coordinates[i][0]+gates[i][0]):
                c=[j, coordinates[i][1]+gates[i][1]]
                pins[i].append(c)
            for j in range(coordinates[i][1]+1, coordinates[i][1]+gates[i][1]):
                c=[coordinates[i][0]+gates[i][0],j]
                pins[i].append(c)
        else:
            pins[i]=[]
            pins[i].append(coordinates[i])
            
    save_dict_to_file(pins,'pins.txt')
    wires = dict(sorted(wires.items(), key = lambda i: -len(i[1])))
    wires1={}
    path1=[]
    m1_interconnects={}
    m2_interconnects={}
    m12c_interconnects={}
    for k, v in wires.items():
        pins = load_dict_from_file('pins.txt')
        t_m1_bc = load_dict_from_file('m1_bc.txt')
        t_m2_bc = load_dict_from_file('m2_bc.txt')
        target_num = 1
        for i in v:
            if(target_num==1):
                connection_wire=[k, i]
                metal1={}
                path1=[]
                metal2={}
                m12c={}
                metal1, metal2, m12c, target, path = routing(connection_wire, t_m1_bc, 
                                                             t_m2_bc, target_num, 
                                                             metal1, metal2, m12c,
                                                             pins, pinouts)
                target_num+=1
                t1_m1_bc = load_dict_from_file('m1_bc.txt')
                t1_m2_bc = load_dict_from_file('m2_bc.txt')
                for k1, v1 in metal1.items():
                    for v2 in v1:
                        t1_m1_bc.append(v2)
                                            
                for k1, v1 in metal2.items():
                    for v2 in v1:
                        t1_m2_bc.append(v2)
                                            
                for k1, v1 in m12c.items():
                    for v2 in v1:
                        t1_m1_bc.append(v2)
                        t1_m2_bc.append(v2)
                save_dict_to_file(t1_m1_bc,'t1_m1_bc.txt')
                save_dict_to_file(t1_m2_bc,'t1_m2_bc.txt')
                        
            elif(target=='true'):
                if(len(path)>2):
                    path.pop(0)
                    path.pop(-1)
                for x in path:
                    path1.append(x)
                connection_wire=[path1, i]
                t2_m1_bc = load_dict_from_file('t1_m1_bc.txt')
                t2_m2_bc = load_dict_from_file('t1_m2_bc.txt')
                metal1, metal2, m12c, target, path = routing(connection_wire, t2_m1_bc, 
                                                             t2_m2_bc, target_num, 
                                                             metal1, metal2, m12c,
                                                             pins, pinouts)
                for k1, v1 in metal1.items():
                    for v2 in v1:
                        t1_m1_bc.append(v2)
                                            
                for k1, v1 in metal2.items():
                    for v2 in v1:
                        t1_m2_bc.append(v2)
                                            
                for k1, v1 in m12c.items():
                    for v2 in v1:
                        t1_m1_bc.append(v2)
                        t1_m2_bc.append(v2)
                save_dict_to_file(t1_m1_bc,'t1_m1_bc.txt')
                save_dict_to_file(t1_m2_bc,'t1_m2_bc.txt')
                
        if(target=='true'):
            save_dict_to_file(pins,'pins.txt')
            for k, v in metal1.items():
                for v1 in v:
                    m1_bc.append(v1)
                    try:
                        m1_interconnects[k].append(v1)
                    except KeyError:
                        m1_interconnects[k]=[]
                        m1_interconnects[k].append(v1)
                    
            for k, v in metal2.items():
                for v1 in v:
                    m2_bc.append(v1)
                    try:
                        m2_interconnects[k].append(v1)
                    except KeyError:
                        m2_interconnects[k]=[]
                        m2_interconnects[k].append(v1)
                    
            for k, v in m12c.items():
                for v1 in v:
                    m1_bc.append(v1)
                    m2_bc.append(v1)
                    try:
                        m12c_interconnects[k].append(v1)
                    except KeyError:
                        m12c_interconnects[k]=[]
                        m12c_interconnects[k].append(v1)
    
            save_dict_to_file(m1_bc,'m1_bc.txt')
            save_dict_to_file(m2_bc,'m2_bc.txt')
        else:
            wires1[k]=v
                   
    wires1 = dict(sorted(wires1.items(), key = lambda i: -len(i[1])))
    wires2={}
    m3_interconnects={}
    m4_interconnects={}
    m34c_interconnects={}
    for k, v in wires1.items():
        pins = load_dict_from_file('pins.txt')
        t_m3_bc = load_dict_from_file('m3_bc.txt')
        t_m4_bc = load_dict_from_file('m4_bc.txt')
        target_num = 1
        for i in v:
            if(target_num==1):
                connection_wire=[k, i]
                metal3={}
                path1=[]
                metal4={}
                m34c={}
                
                metal4, metal4, m34c, target, path = routing(connection_wire, t_m3_bc, 
                                                             t_m4_bc, target_num, 
                                                             metal3, metal4, m34c,
                                                             pins, pinouts)
                target_num+=1
                t1_m3_bc = load_dict_from_file('m3_bc.txt')
                t1_m4_bc = load_dict_from_file('m4_bc.txt')
                for k1, v1 in metal3.items():
                    for v2 in v1:
                        t1_m3_bc.append(v2)
                                            
                for k1, v1 in metal4.items():
                    for v2 in v1:
                        t1_m4_bc.append(v2)
                                            
                for k1, v1 in m34c.items():
                    for v2 in v1:
                        t1_m3_bc.append(v2)
                        t1_m4_bc.append(v2)
                save_dict_to_file(t1_m3_bc,'t1_m3_bc.txt')
                save_dict_to_file(t1_m4_bc,'t1_m4_bc.txt')
                        
            elif(target=='true'):
                if(len(path)>2):
                    path.pop(0)
                    path.pop(-1)
                for x in path:
                    path1.append(x)
                connection_wire=[path1, i]
                t2_m3_bc = load_dict_from_file('t1_m3_bc.txt')
                t2_m4_bc = load_dict_from_file('t1_m4_bc.txt')
                metal3, metal4, m34c, target, path = routing(connection_wire, t2_m3_bc, 
                                                             t2_m4_bc, target_num, 
                                                             metal3, metal4, m34c,
                                                             pins, pinouts)
                for k1, v1 in metal3.items():
                    for v2 in v1:
                        t1_m3_bc.append(v2)
                                            
                for k1, v1 in metal4.items():
                    for v2 in v1:
                        t1_m4_bc.append(v2)
                                            
                for k1, v1 in m34c.items():
                    for v2 in v1:
                        t1_m3_bc.append(v2)
                        t1_m4_bc.append(v2)
                save_dict_to_file(t1_m3_bc,'t1_m3_bc.txt')
                save_dict_to_file(t1_m4_bc,'t1_m4_bc.txt')
                
        save_dict_to_file(pins,'pins.txt') 
        if(target=='true'):
            for k, v in metal3.items():
                for v1 in v:
                    m3_bc.append(v1)
                    try:
                        m3_interconnects[k].append(v1)
                    except KeyError:
                        m3_interconnects[k]=[]
                        m3_interconnects[k].append(v1)
                    
            for k, v in metal4.items():
                for v1 in v:
                    m4_bc.append(v1)
                    try:
                        m4_interconnects[k].append(v1)
                    except KeyError:
                        m4_interconnects[k]=[]
                        m4_interconnects[k].append(v1)
                    
            for k, v in m34c.items():
                for v1 in v:
                    m3_bc.append(v1)
                    m4_bc.append(v1)
                    try:
                        m34c_interconnects[k].append(v1)
                    except KeyError:
                        m34c_interconnects[k]=[]
                        m34c_interconnects[k].append(v1)
    
            save_dict_to_file(m3_bc,'m3_bc.txt')
            save_dict_to_file(m4_bc,'m4_bc.txt')
        else:
            wires2[k]=v
            
    if(len(wires2)==0):
        print("\n Routing is completed")
    else:
        print("\n Routing is incomplete with ",len(wires2),"nets remaining.")
    
    for k, v in m1_interconnects.items():
        cost = cost + len(v)
    for k, v in m2_interconnects.items():
        cost = cost + len(v)
    for k, v in m3_interconnects.items():
        cost = cost + len(v)
    for k, v in m4_interconnects.items():
        cost = cost + len(v)
    for k, v in m12c_interconnects.items():
        cost = cost + 3*len(v)
    for k, v in m34c_interconnects.items():
        cost = cost + 3*len(v)
    print("\n Total cost =",cost)
    end = timer()
    print("\n Time taken=",end - start,"seconds")
    
    plt.figure(figsize=(max_x/15, max_y/15))
    currentAxis = plt.gca()
    plt.xlim([0, max_x])
    plt.ylim([0, max_y])
    plt.title('Final Routing') 
    number_of_colors = 72
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(8)])
                 for i in range(number_of_colors)]
    j = 0
    
    for  k, v in m1_interconnects.items():
        for i in v:
            a = i[0]
            b = i[1]
            currentAxis.add_patch(Rectangle(( a, b + 0.3),1, 0.4, 
                                            alpha = 1, fc='blue'))
        
    for  k, v in m2_interconnects.items():
        for i in v:
            a = i[0]
            b = i[1]
            currentAxis.add_patch(Rectangle(( a + 0.3, b),0.4, 1, 
                                            alpha = 1, fc='red'))
        
    for k, v in m12c_interconnects.items():
        for i in v:
            a = i[0]
            b = i[1]
            
            if(k==3):
                currentAxis.add_patch(Rectangle(( a, b + 0.3),0.5, 0.4, 
                                                alpha = 1, fc='blue'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.5),0.4, 0.5, 
                                                alpha = 1, fc='red'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.3),0.4, 0.4, 
                                                alpha = 1, fc='orange',
                                                ec="black",lw = 0.25))
            elif(k==4):
                currentAxis.add_patch(Rectangle(( a + 0.5, b + 0.3),0.5, 0.4, 
                                                alpha = 1, fc='blue'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.5),0.4, 0.5, 
                                                alpha = 1, fc='red'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.3),0.4, 0.4, 
                                                alpha = 1, fc='orange',
                                                ec="black",lw = 0.25))
            elif(k==5):
                currentAxis.add_patch(Rectangle(( a + 0.5, b + 0.3),0.5, 0.4, 
                                                alpha = 1, fc='blue'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b),0.4, 0.5, 
                                                alpha = 1, fc='red'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.3),0.4, 0.4, 
                                                alpha = 1, fc='orange',
                                                ec="black",lw = 0.25))
            elif(k==6):
                currentAxis.add_patch(Rectangle(( a, b + 0.3),0.5, 0.4, 
                                                alpha = 1, fc='blue'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b),0.4, 0.5, 
                                                alpha = 1, fc='red'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.3),0.4, 0.4, 
                                                alpha = 1, fc='orange',
                                                ec="black",lw = 0.25))
    
    for  k, v in m3_interconnects.items():
        for i in v:
            a = i[0]
            b = i[1]
            currentAxis.add_patch(Rectangle(( a, b + 0.3),1, 0.4, 
                                            alpha = 1, fc='yellow'))
            
    for  k, v in m4_interconnects.items():
        for i in v:
            a = i[0]
            b = i[1]
            currentAxis.add_patch(Rectangle(( a + 0.3, b),0.4, 1, 
                                            alpha = 1, fc='green'))
    
    for k, v in m34c_interconnects.items():
        for i in v:
            a = i[0]
            b = i[1]
            
            if(k==3):
                currentAxis.add_patch(Rectangle(( a, b + 0.3),0.5, 0.4, 
                                                alpha = 1, fc='yellow'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.5),0.4, 0.5, 
                                                alpha = 1, fc='green'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.3),0.4, 0.4, 
                                                alpha = 1, fc='violet',
                                                ec="black",lw = 0.25))
            elif(k==4):
                currentAxis.add_patch(Rectangle(( a + 0.5, b + 0.3),0.5, 0.4, 
                                                alpha = 1, fc='yellow'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.5),0.4, 0.5, 
                                                alpha = 1, fc='green'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.3),0.4, 0.4, 
                                                alpha = 1, fc='violet',
                                                ec="black",lw = 0.25))
            elif(k==5):
                currentAxis.add_patch(Rectangle(( a + 0.5, b + 0.3),0.5, 0.4, 
                                                alpha = 1, fc='yellow'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b),0.4, 0.5, 
                                                alpha = 1, fc='green'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.3),0.4, 0.4, 
                                                alpha = 1, fc='violet',
                                                ec="black",lw = 0.25))
            elif(k==6):
                currentAxis.add_patch(Rectangle(( a, b + 0.3),0.5, 0.4, 
                                                alpha = 1, fc='yellow'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b),0.4, 0.5, 
                                                alpha = 1, fc='green'))
                currentAxis.add_patch(Rectangle(( a + 0.3, b + 0.3),0.4, 0.4, 
                                                alpha = 1, fc='violet',
                                                ec="black",lw = 0.25))
                
    for i in coordinates:
        if i not in pinouts:
            a = coordinates[i][0]
            b = coordinates[i][1]
            currentAxis.add_patch(Rectangle((a, b), float(gates[i][0]), 
                                            float(gates[i][1]),alpha = 0.6, 
                                            fc = color[j],ec="black",lw=0.5))
            plt.text(a + 0.15, b + 0.15 ,i, fontsize=3)
            j+=1 
        else:
            a=coordinates[i][0]
            b=coordinates[i][1]
            currentAxis.add_patch(Rectangle((a, b),1, 1, alpha=1, fc='black'))
            plt.text(a, b + 1 ,i, fontsize = 3)
        
    plt.savefig("Final_Routing.png", dpi = 1000)
    plt.show()
    
    os.remove("blocked_coordinates.txt")
    os.remove("m1_bc.txt")
    os.remove("m2_bc.txt")
    os.remove("m3_bc.txt")
    os.remove("m4_bc.txt")
    os.remove("t1_m1_bc.txt")
    os.remove("t1_m2_bc.txt")
    os.remove("t1_m3_bc.txt")
    os.remove("t1_m4_bc.txt")


if __name__ == '__main__':
    main()
