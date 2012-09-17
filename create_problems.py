#! /usr/bin/env python
import os
import re
from get_problem_directories import *

def basename(s):
    return s.rpartition(".")[0].rpartition("/")[-1]

def foldername(s):
    return "problems/sat/" + "/".join(s.rsplit("/", 4)[2:4]) + "/"

def get_size(s):
    return re.search("\d+", s).group(0)

def get_prob(s):
    return str(float(re.search("\d+", s).group(0))/100)

# sat
for cnf in os.popen("find generators/cnf -name *.cnf"):
    os.system("generators/sat_CNFtoPDDL.py " + " ".join([cnf.rstrip(), foldername(cnf)]))

for j in hamiltonian_1:
    for i in hamiltonian_0:
            for seed in range(10):
                size = get_size(i)
                prob = get_prob(j)
                prob_name = "_".join(["ham", size , get_size(j) , str(seed)])
                os.system("generators/hamiltonian.py problems/hamiltonian/" +\
                        "/".join([i, j]) + "/ " + \
                        " ".join([prob_name, get_size(i), get_prob(j), str(seed)]))

for j in matching_1:
    for i in matching_0:
        for seed in range(10):
            size = get_size(i)
            prob = get_prob(j)
            prob_name = "_".join(["mat", size , get_size(j) , str(seed)])
            os.system("generators/matching.py problems/matching/" +\
                    "/".join([i, j]) + "/ " + \
                    " ".join([prob_name, get_size(i), get_prob(j), str(seed)]))

for j in coloring_1:
    for i in coloring_0:
        for seed in range(10):
            size = get_size(i)
            prob = get_prob(j)
            prob_name = "_".join(["col", size , get_size(j) , str(seed)])
            os.system("generators/coloring.py problems/coloring/" +\
                    "/".join([i, j]) + "/ " + \
                    " ".join([prob_name, get_size(i), get_prob(j), str(seed)]))

for i in clique_0:
    for j in clique_1:
        for k in clique_2:
            # adjust for small sizes
            if i == "5size" and (k == "5clique" or k == "6clique"): continue
            if i == "10size" and k == "6clique": continue
            for seed in range(10):
                size = get_size(i)
                prob = get_prob(j)
                prob_name = "_".join(["cli", size , get_size(j), get_size(k), str(seed)])
                os.system("generators/clique.py problems/clique/" +\
                        "/".join([i, j, k]) + "/ " + \
                        " ".join([prob_name, get_size(i), get_prob(j), get_size(k), str(seed)]))

for i in kcol_0:
    for j in kcol_1:
        for k in kcol_2:
            for seed in range(10):
                size = get_size(i)
                prob = get_prob(j)
                prob_name = "_".join(["kco", size , get_size(j), get_size(k), str(seed)])
                os.system("generators/kcolorability.py problems/kcolorability/" +\
                        "/".join([i, j, k]) + "/ " + \
                        " ".join([prob_name, get_size(i), get_prob(j), get_size(k), str(seed)]))
