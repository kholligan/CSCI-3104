# Name: Kevin Holligan
# Email: kevin.holligan@colorado.edu
# SUID: 810766403
#

import sys
import random
import time
import math
from nt import lstat
import numpy as np
import matplotlib.pyplot as plt
import pylab

# --------- Insertion Sort -------------
# Implementation of getPosition
# Helper function for insertionSort
def getPosition(rList, elt):
    # Find the position where element occurs in the list
    #
    for (i,e) in enumerate(rList):
        if (e >= elt):
            return i
    return len(rList)

# Implementation of Insertion Sort 
def insertionSort(lst):
    n = len(lst)
    retList = []
    for i in lst:
        pos = getPosition(retList,i)
        retList.insert(pos,i)    
    return retList

#------ Merge Sort --------------
def mergeSort(lst):
    # You can add additional utility functions to help you out.
    # But the function to do mergesort should be called mergeSort
    n = len(lst)
    leftList = []
    rightList = []
    #Check that the list is not empty
    if not lst:
        return
    #Base case, list is of size 1, return the list
    if n == 1:
        return lst
    else:
        q = math.floor(n / 2) #Divide in half
        leftList = mergeSort(lst[0:q]) #Recurse left half
        rightList = mergeSort(lst[q:]) #Recurse right half
        lst = merge(leftList, rightList) #Combine the sorted lists

    return lst

def merge(a,b):
    result=[]
    
    i = 0
    j = 0
    #Count through the two lists
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    #Once a list has finished, add all the remaining items of the other list
    if i < len(a):
        result.extend(a[i:])
    if j < len(b):
        result.extend(b[j:])
    
    return result

#------ Quick Sort --------------
def quickSort(lst):
    # You may add additional utility functions to help you out.
    # But the function to do quicksort should be called quickSort
    retList = []
    n = len(lst)
    #Base case of either an empty list or a list of 1 item
    if n <= 1:
        return lst
    #Get the partitioned lst and the index of the pivot
    q, lst = partition(lst)
    
    #Concatenate the left side recursive call, the pivot, and the right side recursive call
    retList = quickSort(lst[0:q]) + [lst[q]] + quickSort(lst[q+1:])
    
    return retList
    
def partition(lst):
    n = len(lst)
    #Set a random pivot
    pivotIndex = random.randrange(n)
    pivot = lst[pivotIndex]
    #Swap the pivot with position 0 in the list
    lst[0], lst[pivotIndex] = lst[pivotIndex], lst[0]
    #Start at i = 1, because pivot is position 0, i tracks the position to swap with
    i = 1
    
    #Traverse the list, swap items lower than pivot with i
    for j in range(1,n):
        if lst[j] <= pivot:
            lst[i], lst[j] = lst[j], lst[i]
            i += 1
    #Put the pivot in its position
    lst[0], lst[i-1] = lst[i-1], lst[0]
    
    return i - 1, lst    

# ------ Timing Utility Functions ---------

# Function: generateRandomList
# Generate a list of n elements from 0 to n-1
# Shuffle these elements at random

def generateRandomList(n):
   # Generate a random shuffle of n elements
   lst = list(range(0,n))
   random.shuffle(lst)
   return lst


def measureRunningTimeComplexity(sortFunction,lst):
    t0 = time.clock()
    sortFunction(lst)
    t1 = time.clock() # A rather crude way to time the process.
    return (t1 - t0)


# --- TODO

# Write code to extract average/worst-case time complexity
def complexityTest():
    
    f = open('complexityData.txt', 'wb+')
    
    isortPlot, isortMax, isortAverage = ([] for i in range(3))
    msortPlot, msortMax, msortAverage = ([] for i in range(3))
    qsortPlot, qsortMax, qsortAverage = ([] for i in range(3))
    x = []
    count = 1
    
    for i in range(0, 500, 5):
        #Store the x values for plotting
        x.append(i)
        for n in range(50):
            #Generate lists and store the time complexity in lists
            testList = generateRandomList(i)
            isortPlot.append(measureRunningTimeComplexity(insertionSort, testList))
            msortPlot.append(measureRunningTimeComplexity(mergeSort, testList))
            qsortPlot.append(measureRunningTimeComplexity(quickSort, testList))
        
        #Calculate max and average and store in lists
        isortMax.append(max(isortPlot))
        isortAverage.append(np.mean(isortPlot))
        
        msortMax.append(max(msortPlot))
        msortAverage.append(np.mean(msortPlot))
        
        qsortMax.append(max(qsortPlot))
        qsortAverage.append(np.mean(qsortPlot))
        
        
        f.write(bytes("iSort Test Case:, " + str(isortPlot).strip('[]') + '\n', 'UTF-8'))
        f.write(bytes("mSort Test Case:, " + str(msortPlot).strip('[]') + '\n', 'UTF-8'))
        f.write(bytes("qSort Test Case:, " + str(qsortPlot).strip('[]') + '\n', 'UTF-8'))
        #Clear the testLists for the next round of tests
        del isortPlot[:]
        del msortPlot[:]
        del qsortPlot[:]

    #print(str(qsortMax).strip('[]'))
    
    #Plot the output
    makePlot(x, isortMax, isortAverage, 'Insertion Sort')
    makePlot(x, msortMax, msortAverage, 'Merge Sort')
    makePlot(x, qsortMax, qsortAverage, 'Quick Sort')
    
    f.write(bytes("iSort Average:, " + str(isortAverage).strip('[]') + '\n', 'UTF-8'))
    f.write(bytes("iSort Max:, " + str(isortMax).strip('[]') + '\n', 'UTF-8'))
    
    f.write(bytes("mSort Average:, " + str(msortAverage).strip('[]') + '\n', 'UTF-8'))
    f.write(bytes("mSort Max:, " + str(msortMax).strip('[]') + '\n', 'UTF-8'))
    
    f.write(bytes("qSort Average:, " + str(qsortAverage).strip('[]') + '\n', 'UTF-8'))
    f.write(bytes("qSort Max:, " + str(qsortMax).strip('[]') + '\n', 'UTF-8'))
    
    f.close()
    

def makePlot(x, lstMax, lstAvg, plotTitle):
    plt.scatter(x, lstMax, color='r')
    plt.scatter(x, lstAvg, color='g')
    plt.title(plotTitle)
    plt.xlabel('Size of list')
    plt.ylabel('Time to sort')
    plt.ylim([0,0.005])
    plt.show()
            
complexityTest()
