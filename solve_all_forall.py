#! /usr/bin/env python
RUN = False
RUN = True

import os, re, sys

problems = "qbfae|qbfea"
limits = "" # "ulimit -t 1800; ulimit -m 3000;"
plannerCommand = "planners/m/M -Q"
output = ">"

def getDomain(problem):
    # print re.search(problems, problem).group(0)
    return re.search(problems, problem).group(0)

def qbfaeBounds(problem):
    # qbf__1a_5e_6c_0.pddl
    problem_info = problem.split("_")
    n_fowff = int(problem_info[1][:-1])
    n_clauses = int(problem_info[3][:-1])
    # print "N: " + str(n_clauses) + "   Nforall: " + str(n_fowff) + " bound1: " + str(pow(2,n_fowff)) + "*(" + str(n_clauses) + " + 9)"
    return (pow(2,n_fowff)*(n_clauses + 9) + 2,pow(2,n_fowff)*(n_clauses + 10) + 2)

def qbfeaBounds(problem):
    # qbf__1a_5e_6c_0.pddl
    # print problem.partition("_")
    n = int(re.search("\d+", problem).group(0))
    return (n + 5, n + 5)

def stepSize(bounds):
    return "-S 1" # fixed for now, try every step

def showBounds(bounds):
    return "-F " + str(bounds[0]) + " -T " + str(bounds[1])

def parallelInstances(bounds):
    # from stackoverflow:
    #def divisorGenerator(n):
    #    for i in range(1, n/2+1):
    #        if n % i == 0: yield i
    #    yield n

    n = bounds[1] - bounds[0]
    if n > 3:
        return "-A 4"
    else:
        return "-A " + str(n+1)

def solveProblems(list, file = None):
    # print list
    for problemFile in list:
        domain = getDomain(problemFile)
        domainFile = "problems-soforall/" + domain + "/" + domain + ".pddl"
        nameParts = problemFile.rpartition("/")
        solutionFile = "solutions-soforall/" + nameParts[0].partition("/")[2] + "/" + \
                       nameParts[2].rpartition(".")[0] + ".out"
    
        if domain == "qbfae":
            bounds = qbfaeBounds(problemFile)
        elif domain == "qbfea":
            bounds = qbfeaBounds(problemFile)
            continue
        else:
            raise ValueError
    
        command = " ".join([limits, plannerCommand, showBounds(bounds), \
                stepSize(bounds), parallelInstances(bounds), "\\\n",
                domainFile, "\\\n", problemFile, "\\\n",
                output, solutionFile])
        if RUN:
            prelude = "Solving " + problemFile + "...\n"
            epilogue = "Solved " + problemFile + ".\n"

            print command
                    # os.system(command)
            print epilogue
        else:
            file.write(command + "\n")

find = """find problems-soforall | grep .pddl | grep -v qbfae.pddl | grep -v qbfea.pddl"""

if __name__ == "__main__":
    
    # this should be split in two processes! fork
    pipe = os.popen(find)
    p0_fileList = []
    p1_fileList = []
    for index, file in enumerate(pipe):
        if index % 2:
            p0_fileList.append(file.rstrip())
        else:
            p1_fileList.append(file.rstrip())
    pipe.close()
    # print p0_fileList
    pid = os.fork()
    if pid:
        if RUN:
            solveProblems(p0_fileList)            
        else:
            a = open("p0.list", "w")
            solveProblems(p0_fileList, a)
            a.close()
        os.waitpid(pid, 0)
    else:
        if RUN:
            solveProblems(p1_fileList)
        else:
            b = open("p1.list", "w")
            solveProblems(p1_fileList, b)
            b.close()
        sys.exit(0)
