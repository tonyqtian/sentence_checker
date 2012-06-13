'''
Created on Jun 8, 2012

@author: Tony
'''
filename = '../data/CLEC_corpus.dat'
input =  open(filename, 'r')

filename = '../data/CLEC_error.dat'
err_output =  open(filename, 'w')

filename = '../data/CLEC_noerr.dat'
noerr_output =  open(filename, 'w')

for line in input:
    if line.count('['):
        err_output.write(line)
    else:
        if line.count('<') == 0:
            noerr_output.write(line)
    