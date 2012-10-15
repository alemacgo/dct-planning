#! /usr/bin/env python
import os
import re
from get_problem_directories_soforall import *

def basename(s):
    return s.rpartition(".")[0].rpartition("/")[-1]

def foldername(s):
    return "problems/sat/" + "/".join(s.rsplit("/", 4)[2:4]) + "/"

def get_size(s):
    return re.search("\d+", s).group(0)

def get_prob(s):
    return str(float(re.search("\d+", s).group(0))/100)

# qbf
a = 1
for i in qbf_0:
    e = 1
    for j in qbf_1:
        c = 1
        for k in qbf_2:
            if a + 5*e > c*5 + 1 :
                c += 1
                continue
            for seed in range(3):
                prob_name = "_".join(["qbf", i , j , k , str(seed)])
                os.system("./generators/blocksqbf/blocksqbf -s " + str(seed) + " -c " + str(c*5 + 1) + " -b 2 -bs " + str(a) +\
                          " -bs " + str(e*5) + " -bc 1 -bc 2 > problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name + ".qdimacs")
                os.system("./generators/qbf_CNFtoPDDL.py problems-soforall/qbfae/" + "/".join([i, j, k])+ "/ -a problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name + ".qdimacs")
                os.system("./sKizzo/sKizzo problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name + ".qdimacs > problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name +".result")
                os.system("rm problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name + ".qdimacs")
                prob_name = "_".join(["qbf", j , i , k , str(seed)])
                os.system("./generators/blocksqbf/blocksqbf -s " + str(seed) + " -c " + str(c*5 + 1) + " -b 2 -bs " + str(e*5) +\
                          " -bs " + str(a) + " -bc 2 -bc 1 > problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".qdimacs")
                os.system("./generators/qbf_CNFtoPDDL.py problems-soforall/qbfea/" + "/".join([j, i, k])+ "/ -e problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".qdimacs")
                os.system("./sKizzo/sKizzo problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".qdimacs > problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".result")  
                os.system("rm problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".qdimacs")
            c += 1
        e += 1
    a += 1
    
print "Created problems-soforall"

