#! /usr/bin/env python
from sys import argv
import math, random
import builtin_predicates as bp

def listDiff(a,b):
    for i in b:
        a.remove(i)
    return a

def generate_random_e(n, p):
    random.seed(seed)
    s, s2 = [], []
    e_set = set()
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            r = random.random()
            x = " node" + str(i)
            y = " node" + str(j)
            if r <= (p/100) and (x, y) not in e_set:
                # print "IN"
                s.append("(e" + x + y + ")")
                # s2.append(";(not_e" + x + y + ")")
                e_set.add((x, y))
                e_set.add((y, x))
    return (s, s2)

if len(argv) != 6:
    print "usage: ./generator path problem_name nvers prob seed"
    exit(0)
                
# argv[1] = path of the static problem
# argv[2] = problem_name
num_vert = int(argv[3]) # argv[3] = number of vertices
p = float(argv[4]) # argv[4] = probability
seed = int(argv[5]) #Seed

pddl_file = open(argv[1] + argv[2] + ".pddl", "w")

pddl_file.write("(define (problem a)\n")
pddl_file.write("\t(:domain n3coloring)\n")
pddl_file.write("\t(:objects\n")

for i in range(1,num_vert + 1):
    pddl_file.write("\t\tnode"+ str(i)+"\n")
pddl_file.write("\t)\n")

    
pddl_file.write("\t(:init\n\t\t(begin)\n")
for i in range(1,num_vert + 1):
    pddl_file.write("\t\t(node node"+ str(i)+")\n")
pddl_file.write("\t\t(node_min node" + str(1) + ")\n")
pddl_file.write("\t\t(node_max node" + str(num_vert) + ")\n")
pddl_file.write("".join(["\t\t(node_suc node" + str(t[0]) + " node" + str(t[1]) +")\n" for t in zip (range(1,num_vert), range(2,num_vert + 1))]))

for i in range(1,num_vert + 1):
    pddl_file.write("\t\t(not_r node"+ str(i)+")\n")
    pddl_file.write("\t\t(not_g node"+ str(i)+")\n")    
    
e_fluents, difference = generate_random_e(num_vert, p)

se_fluents = "\t\t" + "\n\t\t".join(e_fluents)

pddl_file.write(se_fluents)

pddl_file.write("\n\t)\n\t(:goal (holds_goal)\n\t)\n)")  
