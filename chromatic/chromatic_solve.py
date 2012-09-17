#! /usr/bin/env python
import os, re, sys, datetime

limits = "ulimit -t 1800; ulimit -m 3000;"
plannerCommand = "../planners/m/M -Q"
output = ">"
positiveIndicator = "PLAN FOUND" 
negativeIndicator = "NOT FOUND"

def corresponding_k(x, n):
    if x == 1:
        return "(k zero)"
    else:
        return "(k obj" + str(x-1) + ")"
    # k max never happens, trivial

def kcoBounds(problem):
    n = int(re.search("\d+", problem).group(0))
    #return (n + 5, n + 5)
    return (2*n+5, 3*n+6)

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

def solveChromatic(problemFile):
    domain = "kcolorability"
    domainFile = "kcolorability.pddl"

    n = int(re.search("\d+", problemFile).group(0))
    bounds = kcoBounds(problemFile)
    
    for iteration in range(1, n):
        problemFile = problemFile.rpartition("_")[0] + "_" + str(iteration) + ".pddl"
        solutionFile = "solutions/" + problemFile.rpartition(".")[0] + ".out"
    
        command = " ".join([limits, plannerCommand, showBounds(bounds), \
                stepSize(bounds), parallelInstances(bounds), "\\\n",
                domainFile, "\\\n", problemFile, "\\\n",
                output, solutionFile])

        prelude = "Attempting chromatic number = " + str(iteration) + ", " +\
                  str(datetime.datetime.now()) + "..."

        print prelude
        print command
        os.system(command)

        # check if there was a plan for this iteration
        file = open(solutionFile, "r")
        contents = file.read()
        file.close()
        
        if contents.find(positiveIndicator) != -1:
            print "Solved!"
            return "Chromatic number: %d" %(iteration)
        elif contents.find(negativeIndicator) == -1:
            return """The planner has been unable to continue.
                      Chromatic number so far: %d""" %(iteration)

        print "No plan for iteration %d" %(iteration)

        # no need to go to nth iteration, trivially true
        if iteration == n-1:
            return "Chromatic number: %d" %n

        # preparation for the next iteration
        newProblem = problemFile.rpartition("_")
        file = open(problemFile, "r")
        contents = file.read()
        file.close()

        current_k = corresponding_k(iteration, n)
        contents = contents.replace(current_k, current_k + "\n\t\t" +\
                                    corresponding_k(iteration+1, n))

        newProblemFile = problemFile.rpartition("_")[0] + "_" +\
                         str(iteration + 1) + ".pddl"

        newfile = open(newProblemFile, "w")
        newfile.write(contents)
        newfile.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: chromatic_solve problem."
        raise SystemExit()

    problem = sys.argv[1]
    print solveChromatic(problem)
