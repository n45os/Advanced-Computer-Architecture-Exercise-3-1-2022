#!/usr/bin/python
import sys
import re
import os
import json
import types
import math
import StringIO
import subprocess as subp
from optparse import OptionParser


mcpat_bin = "mcpat"

class parse_node:
    def __init__(self,key=None,value=None,indent=0):
        self.key = key
        self.value = value
        self.indent = indent
        self.leaves = []
    
    def append(self,n):
        #print 'adding parse_node: ' + str(n) + ' to ' + self.__str__() 
        self.leaves.append(n)

    def get_tree(self,indent):
        padding = ' '*indent*2
        me = padding + self.__str__()
        kids = map(lambda x: x.get_tree(indent+1), self.leaves)
        return me + '\n' + ''.join(kids)
        
    def getValue(self,key_list):
        #print 'key_list: ' + str(key_list)
        if (self.key == key_list[0]):
            #print 'success'
            if len(key_list) == 1:
                return self.value
            else:
                kids = map(lambda x: x.getValue(key_list[1:]), self.leaves)
                #print 'kids: ' + str(kids) 
                return ''.join(kids)
        return ''        
        
    def __str__(self):
        return 'k: ' + str(self.key) + ' v: ' + str(self.value)

class parser:

    # def dprint(self,astr):
    #     if self.debug:
    #         print self.name,
    #         print astr

    def __init__(self, data_in):
        self.debug = False
        self.name = 'mcpat:mcpat_parse'
        
		buf = open(data_in)
  
  		self.root = parse_node('root',None,-1)
    
        trunk = [self.root]
        
        for line in buf:
            	   
            indent = len(line) - len(line.lstrip())
            equal = '=' in line
            colon = ':' in line
            useless = not equal and not colon
            items = map(lambda x: x.strip(), line.split('='))

            branch = trunk[-1]

            if useless: 
                #self.dprint('useless')
                pass 

            elif equal:
                assert(len(items) > 1)

                n = parse_node(key=items[0],value=items[1],indent=indent)
                branch.append(n)

                self.dprint('new parse_node: ' + str(n) )

            else:
                
                while ( indent <= branch.indent):
                    self.dprint('poping branch: i: '+str(indent) +\
                                    ' r: '+ str(branch.indent))
                    trunk.pop()
                    branch = trunk[-1]
                
                self.dprint('adding new leaf to ' + str(branch))
                n = parse_node(key=items[0],value=None,indent=indent)
                branch.append(n)
                trunk.append(n)
                
        
    def get_tree(self):
        return self.root.get_tree(0)

    def getValue(self,key_list):
        value = self.root.getValue(['root']+key_list) 
        assert(value != '')
        return value

#runs McPAT and gives you the total energy in mJs
def main():
    global opts
    usage = "usage: %prog [options] <mcpat output file> <gem5 stats file>"
    parser = OptionParser(usage=usage)
    parser.add_option("-q", "--quiet", 
        action="store_false", dest="verbose", default=True,
        help="don't print status messages to stdout")
    
    (opts, args) = parser.parse_args()
    if len(args) != 2:
        parser.print_help()
        sys.exit(1)
   
    energy = getEnergy(args[0], args[1])
    # print "energy is %f mJ" % energy
    

def getEnergy(mcpatoutputFile, statsFile):
    leakage, dynamic = readMcPAT(mcpatoutputFile)
    runtime = getTimefromStats(statsFile)
    energy = (leakage + dynamic)*runtime
    # print "leakage: %f W, dynamic: %f W and runtime: %f sec" % (leakage, dynamic, runtime)
    return energy*1000, leakage, dynamic, leakage+dynamic, runtime #mJ

def readMcPAT(mcpatoutputFile):
    
    # print "Reading simulation time from: %s" %  mcpatoutputFile
    p = parser(mcpatoutputFile)
    
    leakage = p.getValue(['Processor:', 'Total Leakage'])
    dynamic = p.getValue(['Processor:', 'Runtime Dynamic'])
    leakage = re.sub(' W','', leakage) 
    dynamic = re.sub(' W','', dynamic) 
    return (float(leakage), float(dynamic))
    

def getTimefromStats(statsFile):
    # if opts.verbose: print "Reading simulation time from: %s" %  statsFile
    F = open(statsFile)
    ignores = re.compile(r'^---|^$')
    statLine = re.compile(r'([a-zA-Z0-9_\.:+-]+)\s+([-+]?[0-9]+\.[0-9]+|[0-9]+|nan)')
    retVal = None
    for line in F:
        #ignore empty lines and lines starting with "---"  
        if not ignores.match(line):
            statKind = statLine.match(line).group(1)
            statValue = statLine.match(line).group(2)
            if statKind == 'sim_seconds':
                retVal = float(statValue)
        break	#no need to parse the whole file once the requested value has been found
    F.close()
    return retVal


if __name__ == '__main__':
    main()