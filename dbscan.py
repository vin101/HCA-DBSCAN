__author__ = 'Jinesh and Vinayak'
import copy
import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
#import pylab
import math
#from itertools import product
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
#import time
#import sys
#import decimal
#import scipy.spatial as spatial
#import collections
import itertools
epsilon = 1.8
min_points = 4.0  # float(sys.argv[3])


#points,neighbours,merging distance,position,flag,cluster_id,hot_cold
def dbscan():
    #Take input from file (Copy Paste from dbscan code) and sort acc. to x and  y axis
    #open the dataset
    file_name="spherical_6_2_modified.csv"
    i=open(file_name)
    lines=i.read().strip().split('\n')
    i.close()
    #initialize the list in which your dataset will be stored in the form of list
    dataset={}
    coord=[]
    dim_size=2#int(sys.argv[1]) #float(sys.argv[2])
    min_points=4.0#float(sys.argv[3])
    #Sort
    for i in range(dim_size):
        coord.append([])
    for i in lines:
        line=i.rstrip().split(',')
        temp=[]
        #extract x and y coordinates
        for j in line:
            temp.append(j.strip())
        #print temp
        #convert to float if the input is not numeric type
        for i in range(dim_size):
            temp[i]=float(temp[i])
            coord[i].append(temp[i])
        #can't use list as keys so converting to tuple
        temp=tuple(temp)
        #print len(dataset)
        #default not visited that's why 0
        dataset[temp]=0
    data=list(sorted(dataset.keys(), key=lambda t: t[0]))
    data=re_round(data)
    #print data
    start_box_coord=[]
    start_box_coord.append(round(min(coord[0]),2))#left most point in dataset(0)
    start_box_coord.append(round(max(coord[0]),2))#right most point in dataset(1)
    start_box_coord.append(round(max(coord[1]),2))#top most point in dataset(2)
    start_box_coord.append(round(min(coord[1]),2))#bottom most point in dataset(3)
    #print start_box_coord
    len_x=round(abs(start_box_coord[1]-start_box_coord[0]),2)#total length of x-axis
    len_y=round(abs(start_box_coord[2]-start_box_coord[3]),2)#total length of y-axis
    number_box_x=int(math.ceil(len_x/round((epsilon/math.sqrt(2)),2)))#epsilon/rt(2)=1.27
    number_box_y=int(math.ceil(len_y/round((epsilon/math.sqrt(2)),2)))
    len_x=number_box_x*round(epsilon/math.sqrt(2),2)
    len_y=number_box_y*round(epsilon/math.sqrt(2),2)
    #print len_x,len_y
    '''fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coord[0], coord[1], cmap=plt.hot())
    plt.plot([start_box_coord[0],start_box_coord[1],start_box_coord[1],start_box_coord[0],start_box_coord[0]], [start_box_coord[2],start_box_coord[2],start_box_coord[3],start_box_coord[3],start_box_coord[2]], 'r-')
    #plt.show()'''
    no_k_bands=number_box_x
    no_l_bands=number_box_y
    k_bands=[]
    l_bands=[]
    k_bands.append(start_box_coord[0]+round(epsilon/math.sqrt(2),2))
    l_bands.append(start_box_coord[3]+round(epsilon/math.sqrt(2),2))
    for i in range(1,no_k_bands):
        temp=k_bands[i-1]+round((epsilon/math.sqrt(2)),2)
        k_bands.append(round(temp,2))
    for j in range (1,no_l_bands):
        temp1=l_bands[j-1]+round((epsilon/math.sqrt(2)),2)
        l_bands.append(round(temp1,2))
    #print k_bands,l_bands
    #creating the boxes
    box_list= list ( itertools.product(k_bands,l_bands) )
    #print box_list
    #print(len(box_list))
    #0 for corner,1 for edge,2 for middle
    box_details={}
    merge_points=[]
    open_flag=0
    cluster_id = 0
    hot_cold = 0
    for i in range(8):
        merge_points.append((-999,-999))
    box_start_coord=[]
    box_start_coord.append(k_bands[0])
    box_start_coord.append(k_bands[number_box_x-1])
    box_start_coord.append(l_bands[number_box_y-1])
    box_start_coord.append(l_bands[0])
    #print box_start_coord
    #print start_box_coord
    for n in box_list:
        #print n
        if(n[0]==box_start_coord[0] or n[0]==box_start_coord[1] or n[1]==box_start_coord[2] or n[1]==box_start_coord[3]):
            #corner cases
            #print "####################################################################"
            if((n[0]== box_start_coord[0] and n[1]==box_start_coord[2])):
                #print "______________________________________________________"
                neighbour=re_round([(n[0]+round((epsilon/math.sqrt(2)),2),n[1]),(n[0]+round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2)),(n[0],n[1]+round((epsilon/math.sqrt(2)),2))])
                box_details[n]=[[],neighbour,merge_points,0,open_flag,cluster_id,hot_cold]#points,neighbours,merging distance,position,flag,cluster_id,hot_cold
            elif((n[0]==box_start_coord[1] and n[1]==box_start_coord[2])):
                #print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                neighbour=re_round([(n[0]-round((epsilon/math.sqrt(2)),2),n[1]),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]-round((epsilon/math.sqrt(2)),2)),(n[0],n[1]-round((epsilon/math.sqrt(2)),2))])
                box_details[n]=[[],neighbour,merge_points,0,open_flag,cluster_id,hot_cold]
            elif((n[0]==box_start_coord[1] and n[1]==box_start_coord[3])):
                #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
                neighbour=re_round([(n[0],n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2))])
                box_details[n]=[[],neighbour,merge_points,0,open_flag,cluster_id,hot_cold]
            elif((n[0]==box_start_coord[0] and n[1]==box_start_coord[3])):
                #print "-------------------------------------------------------"
                neighbour=re_round([(n[0],n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]+round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]+round((epsilon/math.sqrt(2)),2),n[1])])
                box_details[n]=[[],neighbour,merge_points,0,open_flag,cluster_id,hot_cold]
            else:#edge case
                if(n[0]==box_start_coord[0]):#left side
                    neighbour=re_round([(n[0],n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]-round((epsilon/math.sqrt(2)),2)),(n[0],n[1]-round((epsilon/math.sqrt(2)),2))])
                    box_details[n]=[[],neighbour,merge_points,1,open_flag,cluster_id,hot_cold]
                elif(n[1]==box_start_coord[2]):#top side
                    neighbour=re_round([(n[0]-round((epsilon/math.sqrt(2)),2),n[1]),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]-round((epsilon/math.sqrt(2)),2)),(n[0],n[1]-round((epsilon/math.sqrt(2)),2)),(n[0]+round((epsilon/math.sqrt(2)),2),n[1]-round((epsilon/math.sqrt(2)),2)),(n[0]+round((epsilon/math.sqrt(2)),2),n[1])])
                    box_details[n]=[[],neighbour,merge_points,1,open_flag,cluster_id,hot_cold]
                elif(n[0]==box_start_coord[1]):#right side
                    #print "jinesh"
                    neighbour=re_round([(n[0],n[1]+round((epsilon/math.sqrt(2)),2)),(n[0],n[1]-round((epsilon/math.sqrt(2)),2)),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]-round((epsilon/math.sqrt(2)),2))])
                    box_details[n]=[[],neighbour,merge_points,1,open_flag,cluster_id,hot_cold]
                else:#bottom side
                    #print "jinesh"
                    neighbour=re_round([(n[0]-round((epsilon/math.sqrt(2)),2),n[1]),(n[0]+round((epsilon/math.sqrt(2)),2),n[1]),(n[0],n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]+round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2))])
                    box_details[n]=[[],neighbour,merge_points,1,open_flag,cluster_id,hot_cold]
        else:
            neighbour=re_round([(n[0]-round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2)),(n[0],n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]+round((epsilon/math.sqrt(2)),2),n[1]+round((epsilon/math.sqrt(2)),2)),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]),(n[0]+round((epsilon/math.sqrt(2)),2),n[1]),(n[0]-round((epsilon/math.sqrt(2)),2),n[1]-round((epsilon/math.sqrt(2)),2)),(n[0],n[1]-round((epsilon/math.sqrt(2)),2)),(n[0]+round((epsilon/math.sqrt(2)),2),n[1]-round((epsilon/math.sqrt(2)),2))])
            box_details[n]=[[],neighbour,merge_points,2,open_flag,cluster_id,hot_cold]
    #for i in box_details.keys():
    #    print i," ke neighbours hai ---> ",box_details[i][1]
    '''k_bands.append(3.13)
    l_bands.append(3.07)
    v=list ( itertools.product(k_bands,l_bands) )
    print v
    l=[]
    p=[]
    for i in v:
        l.append(i[0])
        p.append(i[1])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coord[0], coord[1], cmap=plt.hot())
    plt.plot(l,p,'go')
    plt.show()'''
    count=0
    for j in data:
        #print j
        count=count+1
        #print coun
        #check for mode over here
        p=(j[0]-start_box_coord[0])
        q=(j[1]-start_box_coord[3])
        if p==0:
            p=1
        elif q==0:
            q=1
        else:
            p=p
            q=q
        mov_x=math.ceil(p/round((epsilon/math.sqrt(2)),2))
        mov_y=math.ceil(q/round((epsilon/math.sqrt(2)),2))
        a=(mov_x*round((epsilon/math.sqrt(2)),2))+start_box_coord[0]
        #print a
        b=(mov_y*round((epsilon/math.sqrt(2)),2))+start_box_coord[3]
        #print b
        a=re_round(a)
        b=re_round(b)
        #print  "point :", j
        #print "box:",a,b
        tp=box_details[a,b][0]
        #print "points already present:",tp
        check=box_details[a,b][4]
        #print "already visited:",check
        #print "box contents:",box_details
        if(not check):
            #print (a,b),j
            box_details[a,b][4]=1
            list_t=[]
            for _ in range(8):
                list_t.append(j)
            box_details[a,b][2]=copy.deepcopy(list_t)
        else:
            if(j[0]<box_details[a,b][2][3][0]):
                box_details[a, b][2][3]=j
            if(j[0]>box_details[a,b][2][4][0]):
                box_details[a, b][2][4]=j
            if(j[1]>box_details[a,b][2][1][1]):
                box_details[a, b][2][1]=j
            if(j[1]<box_details[a,b][2][6][1]):
                box_details[a, b][2][6]=j
            if (j[0]) < (box_details[a,b][2][0][0]) and (j[1]>box_details[a,b][2][0][1]):
                box_details[a, b][2][0]=j
            if j[0]>box_details[a,b][2][2][0] and j[1]>box_details[a,b][2][2][1]:
                box_details[a, b][2][2]=j
            if(j[0]<box_details[a,b][2][5][0] and j[1]<box_details[a,b][2][5][1]):
                box_details[a, b][2][5]=j
            if(j[0]>box_details[a,b][2][7][0] and j[1]<box_details[a,b][2][7][1]):
                box_details[a, b][2][7]=j
            '''
            #print box_details[a,b][2][0]
            box_details[a,b][2][1]=j
            box_details[a,b][2][2]=j
            box_details[a,b][2][3] = j
            box_details[a,b][2][4] = j
            box_details[a,b][2][5] = j
            box_details[a,b][2][6] = j
            box_details[a,b][2][7] = j
            check=0
            '''
        #print tp
        #print "box contents:",box_details
        #print "merging points:",box_details[a,b][2]
        tp.append(j)
        #print "current points:",tp
        box_details[a,b][0]=tp
        #print "points in box:",box_details[a,b][0]
        #print "box contents:",box_details
    print box_details
    #print data
    #for i in box_details.keys():
        #print i,box_details[i][0]
 #0=cold
    count=1
    for i in box_details.keys():
        clustering(box_details,i)
        box_details[i][5]=count
        count=count+1
def clustering(box_details,i):

            open_flag=box_details[i][4]
            hot_flag=box_details[i][6]
            if(open_flag and hot_flag):

                j=(i[0],i[1]+round(epsilon/math.sqrt(2),2))
                if(j in  box_details.keys()):
                    flag = check_up(i, box_details, j)
                    if (flag):
                        box_details[j][6] = 1  # hot
                        box_details[j][5] = box_details[i][5]
                        clustering(box_details, j)
                        # if condition for boundary boxes

                j= (i[0]+round(epsilon/math.sqrt(2),2),i[1]+round(epsilon/math.sqrt(2),2))
                if(j in box_details.keys()):
                    flag=check_up_right(i, box_details,j)
                    if(flag):
                        box_details[j][6]=1
                        box_details[j][5]= box_details[i][5]
                        clustering(box_details,j)


                j= (i[0]+round(epsilon/math.sqrt(2),2),i[1])
                if(j in box_details.keys()):
                    check_right(i, box_details,j)
                    if (flag):
                        box_details[j][6] = 1
                        box_details[j][5] = box_details[i][5]
                        clustering(box_details, j)


                j= (i[0]+round(epsilon/math.sqrt(2),2),i[1]-round(epsilon/math.sqrt(2),2))
                if (j in box_details.keys()):
                    check_down_right(i, box_details,j)
                    if (flag):
                        box_details[j][6] = 1
                        box_details[j][5] = box_details[i][5]
                        clustering(box_details, j)

                j= (i[0],i[1]-round(epsilon/math.sqrt(2),2))
                if (j in box_details.keys()):
                    check_down(i, box_details,j)
                    if (flag):
                        box_details[j][6] = 1
                        box_details[j][5] = box_details[i][5]
                        clustering(box_details, j)



                j= (i[0]-round(epsilon/math.sqrt(2),2),i[1]-round(epsilon/math.sqrt(2),2))
                if (j in box_details.keys()):
                    check_down_left(i,box_details,j)
                    if (flag):
                        box_details[j][6] = 1
                        box_details[j][5] = box_details[i][5]
                        clustering(box_details, j)

                j= (i[0]-round(epsilon/math.sqrt(2),2),i[1])
                if (j in box_details.keys()):
                    check_left(i, box_details,j)
                    if (flag):
                        box_details[j][6] = 1
                        box_details[j][5] = box_details[i][5]
                        clustering(box_details, j)


                j= (i[0]-round(epsilon/math.sqrt(2),2),i[1]+round(epsilon/math.sqrt(2),2))
                if (j in box_details.keys()):
                    check_top_left(i, box_details,j)
                    if (flag):
                        box_details[j][6] = 1
                        box_details[j][5] = box_details[i][5]
                        clustering(box_details, j)

            else:
                pass
def check_up(box_coord,box_details,check_box):
    flag=False
    top=box_details[box_coord][2][1]
    bottom=box_details[check_box][2][6]
    a = np.array(top)
    b = np.array(bottom)
    dist = numpy.linalg.norm(a - b)
    if(dist<epsilon and len(box_details[box_coord][0])>min_points):
        flag=True
    return flag






#round off
def re_round(li, _prec=2):
     try:
         return round(li, _prec)
     except TypeError:
         return type(li)(re_round(x, _prec) for x in li)

dbscan()
