#! /usr/bin/env python
from sys import argv
import math, random
import builtin_predicates as bp

def generateRandomInput(n, p):
    random.seed(seed)
    s = []
    for i in range(1,n+1):
        for j in range(1,n+1):
            for k in range(1,n+1):
                x = random.random()
                if x <= p:
                    s.append("(t" + bp.name(i, n) +\
                            bp.name(j, n) + bp.name(k, n) + ")")
    return s
                
if len(argv) != 6:
    print "usage: ./generator path problem_name nvers prob seed"
    exit(0)

# argv[2] = name of the problem
num_vert = int(argv[3]) # argv[2] = number of vertices
p = float(argv[4]) # argv[3] = probability
seed = int(argv[5]) #Seed

pddl_file = open(argv[1] + argv[2] + ".pddl", "w")

pddl_file.write("(define (problem a)\n")
pddl_file.write("\t(:domain matching)\n")
pddl_file.write("\t(:objects ")

maxim = num_vert 
for i in range (1,maxim-1):
    pddl_file.write("\t\t\tobj"+ str(i)+" \n")
pddl_file.write("\n\t)\n")

pddl_file.write("\t(:init\n\t\t(guess)\n\t\t")

suc_fluents = bp.generate_suc(num_vert)
    
ssuc_fluents = "\n\t\t".join(suc_fluents) + "\n\t\t"
T_set = generateRandomInput(num_vert, p)

st_fluents = "\n\t\t".join(T_set) + "\n\t\t"
sfree_f = "\n\t\t".join(bp.generate_all_2arity("not_f",num_vert)) + "\n\t\t"
sfree_g = "\n\t\t".join(bp.generate_all_2arity("not_g",num_vert)) + "\n\t\t"

free_domain_f = bp.generate_free_domain(num_vert, "f")
free_domain_g = bp.generate_free_domain(num_vert, "g")
free_range_f = bp.generate_free_range(num_vert, "f")
free_range_g = bp.generate_free_range(num_vert, "g")

sfree_domain_f = "\n\t\t".join(free_domain_f) + "\n\t\t"
sfree_domain_g = "\n\t\t".join(free_domain_g) + "\n\t\t"
sfree_range_f = "\n\t\t".join(free_range_f) + "\n\t\t"
sfree_range_g = "\n\t\t".join(free_range_g) + "\n\t\t"

pddl_file.write(ssuc_fluents + st_fluents + sfree_f + sfree_g +\
        sfree_domain_f + sfree_range_f + sfree_domain_g + \
        sfree_range_g)
pddl_file.write("\t)\n")

pddl_file.write("\t(:goal (and (holds_goal))\n\t)\n)")

#print num_vars, num_clau

#print tokens
