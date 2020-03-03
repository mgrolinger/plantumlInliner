#!/usr/bin/python

import re
import sys
import os
import argparse

class PUMLInliner:
    def __init__(self, outputfilename):
        self.output = open(outputfilename, 'w') 
        # output @startuml -> outputfile
        self.output.write("@startuml\n")

        # Merken zum Ersetzen von z.B. $BASE_PATH
        self.variables = {}
        # set to remember already imported files that either clutter the inlined file
        # or the can lead to errors due to !final functions being defined multiple times
        self.alreadyIncludedFiles = set()
        self.counterOpenFiles = 0

    # this recursive function will read a file
    def readFile(self, basepath, filename ):
        self.counterOpenFiles = self.counterOpenFiles + 1
        # log which file is currently processed
        self.output.write("'--> !include "+filename+"\n")
        # replace variables in path such as $BASE_PATH/path/to/file.iuml
        for key, value in self.variables.items():
            basepath = basepath.replace(key,value)
            filename = filename.replace(key,value)
            
        # combine both to the absolute path    
        completeFile = os.path.normpath(basepath + filename)
        
        # open the file read only
        input = open(completeFile, 'r')
        # read in the lines
        Lines = input.readlines()
        # process line by line
        # iregex to gnore existing @startuml and @enduml from inlined files
        startEndPuml = re.compile(r'(\@startuml|\@enduml)') 
        for line in Lines: 
            # ignoriere @startpuml | @endpuml
            se = startEndPuml.search(line.strip())
            if se:
                continue

            # variable find, search if a variable is defined in the line
            self.variables.update(self.findVariable(line))
            #search another  include
            processed = self.processSubsequentInclude(line, basepath, filename, self.alreadyIncludedFiles)
            # the current line was no include, thus we save it to the output
            if processed is True:
                self.output.write(line.rstrip())
                self.output.write("\n")

        self.counterOpenFiles = self.counterOpenFiles - 1
        if self.counterOpenFiles == 0:
            self.closeFile()                


    def findVariable(self,currentLine):
        v = {}
        # regex to find !$variables definitions that could be used in !include paths
        variableFinder = re.compile(r'(\!)(\$.*)(\=)(.*)') 
        # variable find, search if a variable is defined in the line
        vf = variableFinder.search(currentLine.strip())
        # if found
        if vf:
            # save the variable into the map; key = variable name, value = variable value
            v[vf.group(2).strip()] = vf.group(4).strip().replace("'","")
        return v


    def processSubsequentInclude(self, currentLine, basepath, filename, alreadyIncludedFiles):
        #search another  include
        # regex for !include file but not !include <>
        anotherInclude = re.compile(r'(^\!include )([^\<].*)')
        ai = anotherInclude.search(currentLine.strip())
        if ai:
            fileN = ai.group(2)
            path = os.path.dirname(basepath+fileN)+"/"
            fn = fileN.split("/")
            curFile = fn[len(fn)-1]
            cFP = fileN.replace("../","")
            if cFP in alreadyIncludedFiles:
                print(cFP + " already included.\n")
            else:
                print("cFP: "+cFP+", curFile: "+curFile)
                alreadyIncludedFiles.add(cFP)
                self.readFile(path, curFile)
            return False        
        else:
            return True

    
    def closeFile(self):
        self.output.write("'-------------------------------")
        self.output.write("\n@enduml")
        self.output.close() 

#Parse args from console   
parser = argparse.ArgumentParser()
parser.add_argument("--path")
parser.add_argument("--input")
parser.add_argument("--output")
args = parser.parse_args()

# inline file into outputfile
i = PUMLInliner(args.output)
i.readFile(args.path, args.input)
