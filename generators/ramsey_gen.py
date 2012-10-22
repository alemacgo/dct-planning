#! /usr/bin/env python
from sys import argv
import math, random
import builtin_predicates as bp

def generate_k(k,rel):
    if k > num_vert:
        print "Error: k is greater than the number of vertices"
    s = []
    for i in range(1, k+1):
        s.append("(" + rel + bp.name(i, num_vert) + ")")
    return s
    
if len(argv) != 5:
    print "usage: ./generator path problem_name nvers prob seed"
    exit(0)
                
# argv[2] = name of the problem
num_vert = int(argv[2]) # argv[3] = number of vertices
k1 = int(argv[3]) # m
k2 = int(argv[4]) #n

pddl_file = open(argv[1] + argv[2] + ".pddl", "w")

pddl_file.write("(define (problem a)\n")
pddl_file.write("\t(:domain ramsey)\n")
pddl_file.write("\t(:objects\n\t\t")

objects = "\n\t\t".join(bp.generate_obj(num_vert)) + "\n\t)"
pddl_file.write(objects)

pddl_file.write("\n\t(:init\n\t\t(begin)\n\t\t")

suc_fluents = bp.generate_suc(num_vert)
suc_so_forall_fluents = bp.generate_suc_forall(range(1,num_vert+1),num_vert)
generate_t_fluents = bp.generate_free_rel_2arity(num_vert,"t")
free_rel_fluents = bp.generate_free_rel_2arity(num_vert,"f")
free_domain_fluents = bp.generate_free_domain(num_vert,"f")
free_range_fluents = bp.generate_free_range(num_vert,"f")      
k1_fluents = generate_k(k1,"k1")
k2_fluents = generate_k(k2,"k2")

ssuc_fluents = "\n\t\t".join(suc_fluents) + "\n\t\t"
ssuc_so_forall_fluents = "\n\t\t".join(suc_so_forall_fluents) + "\n\t\t"
sgenerate_t_fluents = "\n\t\t".join(generate_t_fluents) + "\n\t\t"
sk1_fluents = "\n\t\t".join(k1_fluents) + "\n\t\t"
sk2_fluents = "\n\t\t".join(k2_fluents) + "\n\t\t"
sfree_rel_fluents = "\n\t\t".join(free_rel_fluents) + "\n\t\t"
sfree_domain_fluents = "\n\t\t".join(free_domain_fluents) + "\n\t\t"
sfree_range_fluents =  "\n\t\t".join(free_range_fluents)

pddl_file.write(ssuc_fluents + ssuc_so_forall_fluents +\
                sgenerate_t_fluents + sfree_rel_fluents + sk1_fluents +\
                sk2_fluents+ sfree_domain_fluents +\
                sfree_range_fluents)

pddl_file.write("\n\t)\n\t(:goal (holds_goal)\n\t)\n)")  
