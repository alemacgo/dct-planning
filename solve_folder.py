#! /usr/bin/env python
RUN = False
RUN = True

import os, re, sys

problems = "hamiltonian|sat|coloring|matching|clique|kcolorability"
limits = "ulimit -t 1800; ulimit -m 4096;"
plannerCommand = "./M -Q"
output = ">"

#! huh? doesn't work here
def getDomain(problem):
    return re.search(problems, problem).group(0)

def satBounds(problem):
    n = int(re.search("\d+", problem).group(0))
    return (n + 5, n + 5)

def hamBounds(problem):
    n = int(re.search("\d+", problem).group(0))
    return (n + 3, n + 9)

def colBounds(problem):
    n = int(re.search("\d+", problem).group(0))
    return (2*n + 3, 2*n + 5)

def cliBounds(problem):
    n = int(re.search("\d+", problem).group(0))
    return (2*n + 4, 3*n + 6)

def matBounds(problem):
    n = int(re.search("\d+", problem).group(0))
    return (3*n + 4, 3*n + 5)

def kcoBounds(problem):
    n = int(re.search("\d+", problem).group(0))
    return (2*n + 4, 3*n + 7) # revisar!

def stepSize(bounds):
    return "-S 1" # fixed for now, try every step

def showBounds(bounds):
    return "-F " + str(bounds[0]) + " -T " + str(bounds[1])

def parallelInstances(bounds):
    n = bounds[1] - bounds[0]
    if n > 3:
        return "-A 4"
    else:
        return "-A " + str(n+1)

def solveProblems(list, file = None):
    solution_folder = "solutions-" + folder.rpartition("/")[0].rpartition("/")[2] + "/"
    os.system("mkdir -p " + solution_folder)
    #! careful with this setting! domain-dependent
    domain = "kcolorability"
    for problemFile in list:
        domainFile = "problems/" + domain + "/" + domain + ".pddl"
        problemName = problemFile.rpartition("/")[2].rpartition(".")[0]
        solutionFile = solution_folder + problemName + ".out"
    
        if domain == "sat":
            bounds = satBounds(problemFile)
        elif domain == "hamiltonian":
            bounds = hamBounds(problemFile)
        elif domain == "coloring":
            bounds = colBounds(problemFile)
        elif domain == "clique":
            bounds = cliBounds(problemFile)
        elif domain == "matching":
            bounds = matBounds(problemFile)
        elif domain == "kcolorability":
            bounds = kcoBounds(problemFile)
        else:
            raise ValueError
    
        command = " ".join([limits, plannerCommand, showBounds(bounds), \
                stepSize(bounds), parallelInstances(bounds), "\\\n",
                domainFile, "\\\n", problemFile, "\\\n",
                output, solutionFile])
        if RUN:
            prelude = "Solving " + problemFile + "...\n"
            epilogue = "Solved " + problemFile + ".\n"

            print prelude
            os.system(command)
            print epilogue
        else:
            file.write(command + "\n")

if __name__ == "__main__":
    folder = sys.argv[1]
    find = "find " + folder + """ -name *.pddl |\
             grep -v hamiltonian.pddl |\
             grep -v sat.pddl |\
             grep -v coloring.pddl |\
             grep -v matching.pddl |\
             grep -v clique.pddl|\
             grep -v kcolorability.pddl"""

    pipe = os.popen(find)

    p0_fileList = []
    p1_fileList = []
    for index, file in enumerate(pipe):
        if index % 2:
            p0_fileList.append(file.rstrip())
        else:
            p1_fileList.append(file.rstrip())
    pipe.close()

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
