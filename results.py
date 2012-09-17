#! /usr/bin/env python
import os
from sys import argv

positiveIndicator = "PLAN FOUND" 
negativeIndicator = "NOT FOUND"

positives = 0
negatives = 0
solved = 0
unsolved = 0

def classify(solution):
    global positives, negatives, solved, unsolved
    file = open(solution, "r")
    string = file.read()
    file.close()
    if string.find(positiveIndicator) != -1:
        positives += 1
        solved += 1 
        return "SOLVED+ " + solution.rpartition("/")[2].rpartition(".")[0]\
                + " " + solution
    elif string.find(negativeIndicator) != -1:
        negatives += 1
        solved += 1
        return "SOLVED- " + solution.rpartition("/")[2].rpartition(".")[0]\
                + " " + solution
    else:
        unsolved += 1
        return "FAILED " + solution.rpartition("/")[2].rpartition(".")[0]\
                + " " + solution

find = "find %s -name *.out" %(argv[1])

#results = {}
#results["sat"] = {}
#results["sat"]["satisfiable"] = {}
#results["sat"]["unsatisfiable"] = {}
#for key in results["sat"]:
#    results["sat"][key]["218"] = {}
#    results["sat"][key]["275"] = {}
#    results["sat"][key]["325"] = {}
#
#results["ham"] = {}
#results["col"] = {}
#results["cli"] = {}
#results["mat"] = {}

results = []
pipe = os.popen(find)
for file in pipe:
#    classify(file.rstrip().rpartition("/")[2])
    results.append(classify(file.rstrip()))
pipe.close()

print "\n".join(results)
print "Total problems: %d, solved: %d, positives: %d, negatives: %d, unsolved: %d"\
        %(solved+unsolved, solved, positives, negatives, unsolved)
