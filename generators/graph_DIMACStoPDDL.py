#! /usr/bin/env python
from sys import argv
import math
import builtin_predicates as bp

def tokenize(input):
    for line in input:
        graph_info = line.partition("p edge")[2]
        if graph_info != '':
            break
    graph = graph_info.split()
    num_vert = int(graph[0])
    num_edges = int(graph[1])
        
    edges = []
    for line in input:
        if line[0] == 'c' or line[0] == 'p':
            continue
        edges.append(line.split())
    return edges, num_vert, num_edges

def listDiff(a,b):
    for i in b:
        a.remove(i)
    return a

def generate_k(k):
    if k > num_vert:
        print "Error: k is greater than the number of vertices"
    s = []
    for i in range(1, k+1):
        s.append("(k" + bp.name(i, num_vert) + ")")
    return s

def translate_e(tokens, num_vert):
    s, s2 = [], []
    for token in tokens:
        s.append("; (e" + bp.name(int(token[1]), num_vert) +\
                     bp.name(int(token[2]), num_vert) + \
                     ')')
        s2.append("(not_e" + bp.name(int(token[1]), num_vert) +\
                     bp.name(int(token[2]), num_vert) + \
                     ')')
    return s, s2

if len(argv) != 4:
    print "usage: ./converter path problem_name k"
    exit(0)
                
# argv[1] = path of the static problem
# argv[2] = problem_name
dimacs_file = open(argv[2] + ".col").readlines()
tokens, num_vert, num_edges = tokenize(dimacs_file)
k = int(argv[3]) 

pddl_file = open(str(num_vert) + "_" + argv[1] + argv[2] + "_k" + argv[3] + ".pddl", "w")

pddl_file.write("(define (problem a)\n")
pddl_file.write("\t(:domain kcolorability)\n")
pddl_file.write("\t(:objects\n\t\t")

objects = "\n\t\t".join(bp.generate_obj(num_vert)) + "\n\t)"

pddl_file.write(objects)

pddl_file.write("\n\t(:init\n\t\t(guess)\n\t\t")
            
suc_fluents = bp.generate_suc(num_vert)
free_rel_fluents = bp.generate_free_rel_2arity(num_vert,"f")
free_domain_fluents = bp.generate_free_domain(num_vert,"f")
free_range_fluents = bp.generate_free_range(num_vert,"f")      

e_fluents, difference = translate_e(tokens, num_vert)
e_fluents2 = listDiff(bp.generate_all_2arity("not_e",num_vert), difference)

ssuc_fluents = "\n\t\t".join(suc_fluents) + "\n\t\t"
se_fluents = "\n\t\t".join(e_fluents) + "\n\t\t"
se_fluents2 = "\n\t\t".join(e_fluents2) + "\n\t\t"
s_k = "\n\t\t".join(generate_k(k)) + "\n\t\t"   
sfree_f = "\n\t\t".join(bp.generate_free_rel_2arity(num_vert,'f')) + "\n\t\t"
sfree_domain_f = "\n\t\t".join(bp.generate_free_domain(num_vert,'f')) + "\n\t\t"

pddl_file.write(ssuc_fluents + se_fluents + se_fluents2 + s_k + sfree_f +\
                sfree_domain_f)

pddl_file.write("\n\t)\n\t(:goal (holds_goal)\n\t)\n)")  
