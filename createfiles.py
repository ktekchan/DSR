#------------------------------------------------------------------------------
# Author: Khushboo Tekchandani
# This is the main script to create traffic and movement files, to create the
# traces and to calculate the degree of the network.
#------------------------------------------------------------------------------


import os
import re
import math


# Delete existing input, traffic and movement scenario files
bashCommand = 'rm -rf input.txt cbr-test scen-test movement-trace.txt'
os.system(bashCommand)

# Create input file for the tcl script
filename = 'input.txt'
inputfile = open(filename, 'w')
inputfile.seek(0)

# Take input from user about various simulation parameters and add the required
# parameters to the input file

# The input file contains the following parameters in order.
# 1. Number of nodes
# 2. X dimension of the simulation area
# 3. Y dimension of the simulation area
# 4. Simulation time
# 5. Seed

print "Please enter the parameters for the simulation..."

numnodes = input('Enter number of nodes: ')
inputfile.write(str(numnodes)+'\n')

Xdim = input('Enter X dimension of the simulation area: ')
inputfile.write(str(Xdim)+'\n')

Ydim = input('Enter Y dimension of the simulation area: ')
inputfile.write(str(Ydim)+'\n')

simtime = input('Enter simulation time: ')
inputfile.write(str(simtime)+'\n')

seed = input('Enter seed value: ')
inputfile.write(str(seed)+'\n')

inputfile.close()

# Remaining parameters for the generating the traffic and movement scenario
# files

# Path for cbrgen.tcl and setdest
path = '/home/khushboo/ns-allinone-2.35/ns-2.35/indep-utils/cmu-scen-gen/'

# Traffic file
maxconnections = input('Enter maximum number of connections: ')
rate = input('Enter cbr rate: ')

arglist =' -type cbr -nn '+str(numnodes-1)+' -seed '+str(seed)+' -mc\
 '+str(maxconnections)+' -rate '+str(rate)+' > cbr-test'

print '\nGenerating traffic scenario file...\n'
bashCommand = 'ns '+path+'cbrgen.tcl'+arglist
os.system(bashCommand)

# Movement scenario file
print 'Enter parameters for movement scenario...\n'
maxspeed = input('Enter maximum speed of nodes: ')
pausetime = input('Enter pause time: ')

arglist = ' -v 1 -n '+str(numnodes)+' -p '+str(pausetime)+' -M '\
+str(maxspeed)+' -t '+str(simtime)+' -x '+str(Xdim)+' -y '+str(Ydim)+\
' > scen-test'

print 'Generating movement scenario file...\n'
bashCommand = path+'setdest/setdest'+arglist
os.system(bashCommand)

# Finally execute the wireless simulation
print 'Executing wireless simulation...\n'
bashCommand = 'ns wireless1.tcl'
os.system(bashCommand)

# Parse the trace file for movement traces
print 'Parsing trace file for movement traces...\n'
bashCommand = 'python parse-M.py'
os.system(bashCommand)

# Use this parsed file to calculate the average degree of the network
print 'Calculating average degree of the network...\n'
bashCommand = 'python degree.py'
os.system(bashCommand)

