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
            x = bp.name(i, n)
            y = bp.name(j, n)
            if r <= p and (x, y) not in e_set:
                s.append("; (e" + x + y + ")")
                s2.append("(not_e" + x + y + ")")
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
pddl_file.write("\t(:domain coloring)\n")
pddl_file.write("\t(:objects\n\t\t")

objects = "\n\t\t".join(bp.generate_obj(num_vert)) + "\n\t)"

pddl_file.write(objects)

pddl_file.write("\n\t(:init\n\t\t(guess)\n\t\t")
            
suc_fluents = bp.generate_suc(num_vert)
free_rel_fluents = bp.generate_free_rel_2arity(num_vert,"f")
free_domain_fluents = bp.generate_free_domain(num_vert,"f")
free_range_fluents = bp.generate_free_range(num_vert,"f")      

e_fluents, difference = generate_random_e(num_vert, p)
# static mode
e_fluents2 = listDiff(bp.generate_all_2arity("not_e",num_vert), difference)

ssuc_fluents = "\n\t\t".join(suc_fluents) + "\n\t\t"
se_fluents = "\n\t\t".join(e_fluents) + "\n\t\t"
se_fluents2 = "\n\t\t".join(e_fluents2) + "\n\t\t"
sfree_r = "\n\t\t".join(bp.generate_free_rel_1arity(num_vert,'r')) + "\n\t\t"
sfree_g = "\n\t\t".join(bp.generate_free_rel_1arity(num_vert,'g')) + "\n\t\t"
sfree_b = "\n\t\t".join(bp.generate_free_rel_1arity(num_vert,'b'))

pddl_file.write(ssuc_fluents + se_fluents + se_fluents2 + sfree_r + sfree_g + sfree_b)

pddl_file.write("\n\t)\n\t(:goal (holds_goal)\n\t)\n)")  
