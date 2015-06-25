#------------------------------------------------------------------------------
# Author: Khushboo Tekchandani

# Parse the trace file to get the Movement traces into a new file
#------------------------------------------------------------------------------


import os
import re

# Open the trace file to read it
f = open ('/home/khushboo/Summer_DSR/wireless1-out.tr', 'r')
f1 = open ('/home/khushboo/Summer_DSR/movement-trace.txt', 'r+')

lines = f.read()
lines = lines.split('\n')

# Parse the lines starting with M (indicating movement trace) and copy them to a
# new file
for line in lines:
    if line.startswith('M'):
        f1.write(line)
        f1.write('\n')


# Close the files
f.close()
f1.close()

