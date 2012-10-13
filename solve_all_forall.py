#! /usr/bin/env python
RUN = False
RUN = True

import os, re, sys

problems = "qbfae|qbfea"
limits = "ulimit -t 5400; ulimit -m 3000;"
plannerCommand = "planners/m/M"
output = ">"

def getDomain(problem):
    # print re.search(problems, problem).group(0)
    return re.search(problems, problem).group(0)

def qbfaeBounds(problem):
    # qbf__1a_5e_6c_0.pddl
    problem_info = problem.split("_")
    n_soforall = int(problem_info[1][:-1])
    n_clauses = int(problem_info[3][:-1])
    # print "N: " + str(n_clauses) + "   Nforall: " + str(n_soforall) + " bound1: " + str(pow(2,n_soforall)) + "*(" + str(n_clauses) + " + 9)"
    return (pow(2,n_soforall)*(n_clauses + 9) + 2,pow(2,n_soforall)*(n_clauses + 10) + 2)

def qbfeaBounds(problem):
    # qbf__5e_1a_6c_0.pddl
    # print problem.partition("_")
    problem_info = problem.split("_")
    n_soforall = int(problem_info[2][:-1])
    n_clauses = int(problem_info[3][:-1])
    return (pow(2,n_soforall)*(n_clauses + 8) + 3,pow(2,n_soforall)*(n_clauses + 8) + 4)

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
        else:
            raise ValueError
    
        submit_file = open("condor_submits/" + nameParts[2].rpartition(".")[0] + ".submit", "w")
        submit_file.write("# Experiment " + problemFile + "\n\n")
        
        submit_file.write("executable = /home-users/nlipo/blai/Aldo/dct-planning/planners/m/M\n")
        submit_file.write("universe = vanilla\n")
        submit_file.write("#Requirements = Memory >= 1928\nInitialDir = /home-users/nlipo/blai/Aldo\n")
        submit_file.write("should_transfer_files = YES\n" +\
                          "when_to_transfer_output = ON_EXIT \n" +\
                           "transfer_input_files = \\\n" +\
                           "/home-users/nlipo/blai/Aldo/dct-planning/" + problemFile + ",\\\n"+\
                           "/home-users/nlipo/blai/Aldo/dct-planning/" + domainFile + "\n\n")
        submit_file.write("arguments = -Q -t 5400 " + " ".join([showBounds(bounds), \
                          stepSize(bounds), parallelInstances(bounds),
                          domain + ".pddl", nameParts[2], "\n"]) + \
                          "output = /home-users/nlipo/blai/Aldo/dct-planning/" + solutionFile + "\n" +\
                          "queue")
        
        # ##
        # ## Experiment: task46
        # ##
        # ## where trials in { 10, 50, 100, 500, 1000, 5000, 10000 }, par = 0.5, nexp = 10%
        # ##
        # 
        # 
        # #executable   = /home-users/nlipo/blai/learning-depth-first-search-read-only/race/race
        # executable    = /home-users/nlipo/blai/Aldo/example.sh
        # universe  = vanilla
        # #Requirements = Memory >= 1928
        # InitialDir    = /home-users/nlipo/blai/Aldo
        # should_transfer_files = YES
        # when_to_transfer_output   = ON_EXIT
        # #transfer_input_files = \
        # #/home-users/nlipo/blai/learning-depth-first-search-read-only/race/tracks/barto-small.track,\
        # #/home-users/nlipo/blai/learning-depth-first-search-read-only/race/tracks/barto-big.track
        # 
        # #arguments = -D 0.5 -h 11 -s 0 -p 0.7 barto-big.track min-min aot-value 10 50 0.5 5
        # arguments = -lR
        # output = output.1
        # queue
        # arguments = -lR
        # output = output.2
        # queue

        
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
