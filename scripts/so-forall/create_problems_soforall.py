#! /usr/bin/env python
import os
import re
import random
import math
from sys import argv
from get_all_directories_soforall import *

def runBash(prob_path, prob_name, exchange, seed, n_clauses, q_list, c_list):
    rnd = [1231, 92, 2221, 3, 32]
    
    os.system("./generators/blocksqbf/blocksqbf -s " + str(int(seed*rnd[seed])) +\
              " -c " + n_clauses + " -b " + str(len(q_list)) +\
              " -bs " + " -bs ".join(q_list) + " -bc " + " -bc ".join(c_list) +\
              " > " + prob_path + prob_name + ".qdimacs")
                  
    if exchange:
        os.system("more " + prob_path + prob_name + ".qdimacs | tr a A | tr e a | tr A e > " + prob_path + prob_name + "1.qdimacs")
        os.system("rm " + prob_path + prob_name + ".qdimacs; mv " + prob_path + prob_name + "1.qdimacs " + prob_path + prob_name + ".qdimacs" )
        
    os.system("./sKizzo/sKizzo " + prob_path + prob_name + ".qdimacs > " + prob_path + prob_name + ".result")
    os.system("./generators/qbf_CNFtoPDDL.py " + prob_path + " " + prob_path + prob_name + ".qdimacs")
    os.system("rm " + prob_path + prob_name + ".qdimacs")
    
        
    # os.system("rm " + prob_path + prob_name + "*.qdimacs")
    

# qbf

# random.seed(int(argv[1]))

print "Generating Problems"

print " QBF_AE & QBF_EA"

for i in qbf_0:
    for j in qbf_1:
        for c in qbf_2:
            if int(i[:-1]) + int(j[:-1]) > int(c[:-1]):
                continue
            for seed in range(5):                
                #QBF AE
                prob_name = "_".join(["qbf", i , j , c , str(seed)])
                prob_path = "/".join(["problems-soforall", "qbfae", i, j, c]) + "/"
                runBash(prob_path, prob_name, False, seed, c[:-1], [i[:-1], j[:-1]], ["1","2"])
                
                #QBF EA
                prob_name = "_".join(["qbf", j , i , c , str(seed)])
                prob_path = "/".join(["problems-soforall", "qbfea", j, i, c]) + "/"
                runBash(prob_path, prob_name, True, seed, c[:-1], [j[:-1], i[:-1]], ["2","1"])

#QBF EAE
print " QBF_EAE"

for e1 in qbf3_e:
    for a1 in qbf3_a:
        for e2 in qbf3_e:
            for c in qbf_2:
                if int(a1[:-1]) + int(e1[:-1]) + int(e2[:-1]) > int(c[:-1]):
                    continue
                for seed in range (5):
                    prob_name = "_".join(["qbf3eae", e1, a1, e2, c, str(seed)])
                    prob_path = "/".join(["problems-soforall","qbf3eae", e1, a1, e2, c]) + "/"
                    runBash(prob_path, prob_name, False, seed, c[:-1], [e1[:-1], a1[:-1], e2[:-1]], ["1","1","1"])

#QBF 3 AEA

print " QBF_AEA"

for a1 in qbf3_a2:
    for e1 in qbf3_e2:
        for a2 in qbf3_a2:
            for c in qbf_2:
                if int(a1[:-1]) + int(e1[:-1]) + int(a2[:-1]) > int(c[:-1]):
                    continue
                for seed in range (5):
                    prob_name = "_".join(["qbf3aea", a1, e1, a2, c, str(seed)])
                    prob_path = "/".join(["problems-soforall", "qbf3aea", a1, e1, a2, c]) + "/"
                    runBash(prob_path, prob_name, True, seed, c[:-1], [a1[:-1], e1[:-1], a2[:-1]], ["1","2","1"])

    
print "Created problems-soforall"

