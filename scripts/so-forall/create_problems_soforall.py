#! /usr/bin/env python
import os
import re
import random
import math
from sys import argv
from get_all_directories_soforall import *

def basename(s):
    return s.rpartition(".")[0].rpartition("/")[-1]

def foldername(s):
    return "problems/sat/" + "/".join(s.rsplit("/", 4)[2:4]) + "/"

def get_size(s):
    return re.search("\d+", s).group(0)

def get_prob(s):
    return str(float(re.search("\d+", s).group(0))/100)

# qbf

random.seed(int(argv[1]))
print argv[1]

print "Generating Problems"

print " QBFAE - QBFEA"
a = 1
for i in qbf_0:
    e = 1
    for j in qbf_1:
        c = 1
        for k in qbf_2:
            if a + 5*e > c*5 + 1 :
                c += 1
                continue
            for seed in range(5):
                
                rnd = math.ceil(random.random() * 100)
                prob_name = "_".join(["qbf", i , j , k , str(seed)])
                os.system("./generators/blocksqbf/blocksqbf -s " + str(int(seed + rnd)) + " -c " + str(c*5 + 1) + " -b 2 -bs " + str(a) +\
                          " -bs " + str(e*5) + " -bc 1 -bc 2 > problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name + ".qdimacs")
                os.system("./generators/qbf_CNFtoPDDL.py problems-soforall/qbfae/" + "/".join([i, j, k])+ "/ -a problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name + ".qdimacs")
                os.system("./sKizzo/sKizzo problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name + ".qdimacs > problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name +".result")
                os.system("rm problems-soforall/qbfae/" + "/".join([i, j, k])+ "/" + prob_name + ".qdimacs")
                
                prob_name = "_".join(["qbf", j , i , k , str(seed)])
                os.system("./generators/blocksqbf/blocksqbf -s " + str(int(seed + rnd)) + " -c " + str(c*5 + 1) + " -b 2 -bs " + str(e*5) +\
                          " -bs " + str(a) + " -bc 2 -bc 1 > problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".qdimacs")
                os.system("./generators/qbf_CNFtoPDDL.py problems-soforall/qbfea/" + "/".join([j, i, k])+ "/ -e problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".qdimacs")
                os.system("more problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".qdimacs | tr a A | tr e a | tr A e > problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + "1.qdimacs")
                os.system("./sKizzo/sKizzo problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + "1.qdimacs > problems-soforall/qbfea/" + "/".join([j, i, k])+ "/" + prob_name + ".result")  
                os.system("rm problems-soforall/qbfea/" + "/".join([j, i, k])+ "/*.qdimacs")
            c += 1
        e += 1
    a += 1
    
#QBF EAE
print " QBFEAE"

e1_i = 1
for e1 in qbf3_e:
    a1_i = 1
    for a1 in qbf3_a:
        e2_i = 1
        for e2 in qbf3_e:
            c_i = 1
            for c in qbf_2:
                if a1_i + e1_i*5 + e2_i*5 > c_i*10:
                     c_i += 1
                     continue
                for seed in range (3):
                    rnd = math.ceil(random.random() * 100)          
                    prob_name = "_".join(["qbf3eae", e1, a1, e2, c, str(seed)])
                    prob_path = "/".join(["qbf3eae", e1, a1, e2, c]) + "/"
                    os.system("./generators/blocksqbf/blocksqbf -s " + str(int(seed + rnd)) + " -c " + str(c_i*10) + " -b 3 -bs " + str(e1_i*5) +\
                              " -bs " + str(a1_i) + " -bs " + str(e2_i*5) + " -bc 1 -bc 1 -bc 1 > problems-soforall/" + prob_path + prob_name + ".qdimacs")
                    os.system("./generators/qbf3_CNFtoPDDL.py problems-soforall/" + prob_path + " -a problems-soforall/" + prob_path + prob_name + ".qdimacs")
                    os.system("./sKizzo/sKizzo problems-soforall/" + prob_path + prob_name + "1.qdimacs > problems-soforall/" + prob_path + prob_name + ".result")  
                    os.system("rm problems-soforall/" + prob_path + "*.qdimacs")
                c_i += 1
            e2_i += 1
        a1_i +=1
    e1_i += 1

#QBF 3 AEA

print " QBFAEA"

a1_i = 1
for a1 in qbf3_a2:
    e1_i = 1
    for e1 in qbf3_e2:
        a2_i = 1
        for a2 in qbf3_a2:
            c_i = 1
            for c in qbf_2:
                if a1_i + e1_i*5 + a2_i > c_i*10:
                    c_i += 1
                    continue
                for seed in range (3):
                    rnd = math.ceil(random.random() * 100)          
                    prob_name = "_".join(["qbf3aea", a1, e1, a2, c, str(seed)])
                    prob_path = "/".join(["qbf3aea", a1, e1, a2, c]) + "/"
                    os.system("./generators/blocksqbf/blocksqbf -s " + str(int(seed + rnd)) + " -c " + str(c_i*10) + " -b 3 -bs " + str(a1_i) +\
                              " -bs " + str(e1_i*5) + " -bs " + str(a2_i) + " -bc 1 -bc 2 -bc 1 > problems-soforall/" + prob_path + prob_name + ".qdimacs")
                    os.system("./generators/qbf3_CNFtoPDDL.py problems-soforall/" + prob_path + " -e problems-soforall/" + prob_path + prob_name + ".qdimacs")
                    os.system("more problems-soforall/" + prob_path + prob_name + ".qdimacs | tr a A | tr e a | tr A e > problems-soforall/" + prob_path + prob_name + "1.qdimacs")
                    os.system("./sKizzo/sKizzo problems-soforall/" + prob_path + prob_name + "1.qdimacs > problems-soforall/" + prob_path + prob_name + ".result")  
                    os.system("rm problems-soforall/" + prob_path + "*.qdimacs")
                c_i += 1
            a2_i += 1
        e1_i +=1
    a1_i += 1

    
print "Created problems-soforall"

