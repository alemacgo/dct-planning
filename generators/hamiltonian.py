#! /usr/bin/env python
from sys import argv
import math, random
import builtin_predicates as bp

def generate_random_e(n, p):
    random.seed(seed)
    s = []
    for i in range(1,n+1):
        for j in range(1,n+1):
            r = random.random()
            x = bp.name(i, n)
            y = bp.name(j, n)
            if r <= p:
                s.append("(e" + x + y + ")")
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
pddl_file.write("\t(:domain hamiltonian)\n")
pddl_file.write("\t(:objects\n\t\t")

objects = "\n\t\t".join(bp.generate_obj(num_vert)) + "\n\t)"
pddl_file.write(objects)

pddl_file.write("\n\t(:init\n\t\t(guess)\n\t\t")
            
suc_fluents = bp.generate_suc(num_vert)
gt_fluents = bp.generate_gt(num_vert)
free_rel_fluents = bp.generate_free_rel_2arity(num_vert,"f")
free_domain_fluents = bp.generate_free_domain(num_vert,"f")
free_range_fluents = bp.generate_free_range(num_vert,"f")      

e_fluents = generate_random_e(num_vert, p)

ssuc_fluents = "\n\t\t".join(suc_fluents) + "\n\t\t"
se_fluents = "\n\t\t".join(e_fluents) + "\n\t\t"
slt_fluents = "\n\t\t".join(gt_fluents) + "\n\t\t"
sfree_rel_fluents = "\n\t\t".join(free_rel_fluents) + "\n\t\t"
sfree_domain_fluents = "\n\t\t".join(free_domain_fluents) + "\n\t\t"
sfree_range_fluents =  "\n\t\t".join(free_range_fluents)

pddl_file.write(ssuc_fluents + se_fluents + slt_fluents +\
                sfree_rel_fluents + sfree_domain_fluents +\
                sfree_range_fluents)

pddl_file.write("\n\t)\n\t(:goal (holds_goal)\n\t)\n)")  
