#------------------------------------------------------------------------------
# Author: Khushboo Tekchandani

# Calculate the average degree of the network based on the mobility patterns.
# This calculation is done periodically and the average is calculated over the
# entire simulation time.

#------------------------------------------------------------------------------

#!/usr/bin/python

import os
import re
import math

numnodes = 10
trans_range = 250
count = 0
inst_avg = []
current_pos = []

# Parses a line to find the current position of a node
def parseline(line):
    words = line.split()
    if (len(words)>0):
        x = float(words[3].strip('(,'))
        y = float(words[4].strip(','))
        pos = (x,y)
        return pos

# Calculates the euclidean distance between two points
def calc_dist(x1,x2):
    dist = math.sqrt(math.pow((x1[0]-x2[0]),2)+math.pow((x1[1]-x2[1]),2))
    return dist

# Calculates the average degree of the network at the particular instance
def calc_inst_avg(current_pos):
    connections = 0
    for i in range(len(current_pos)):
        for j in range(i+1,len(current_pos)-1):
            dist = calc_dist(current_pos[i],current_pos[j])
            if (dist<=trans_range):
                connections+=1
    inst_avg = connections/numnodes
    return inst_avg


# Open the trace file to read it
f = open ('/home/khushboo/Summer_DSR/movement-trace.txt', 'r')
lines = f.read()
lines = lines.split('\n')       


for line in lines:
    words = line.split()

    # To get rid of any empty lines in the file
    if not words:
        continue

    # It is possible to have incomplete movement entries at an instance
    # Check that each time the input of entries start with node id 0 and end at
    # node id (numnodes-1)

    if (float(words[2])>0 and float(words[2])<=(numnodes-1)):
        current_pos.append(parseline(line))

    # As soon as we reach the entry for first node in the next iteration,
    # calculate the instantaneous average for the previous information

    elif(float(words[2]) == 0):

        # Check if the current_pos is an empty list. This will happen only
        # during the first iteration of movement information

        if not current_pos:
            continue
        else:
            avg = calc_inst_avg(current_pos)
            inst_avg.append(avg)
            del current_pos[:]
            current_pos.append(parseline(line))

# Find the overall average degree of the network over the entire simulation time
average_degree = sum(inst_avg)/len(inst_avg)
print average_degree

# Close the file
f.close()
