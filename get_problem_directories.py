#! /usr/bin/env python
import os

problems = ["sat", "hamiltonian", "clique", "matching", "coloring"]

# sat
sat_0 = ["satisfiable", "unsatisfiable"]
sat_1 = ["91-20", "218-50", "325-75"]

# hamiltonian
hamiltonian_0 = ["10size", "15size", "20size", "25size", "30size"]
hamiltonian_1 = ["5prob", "10prob", "25prob", "50prob"]

# matching
matching_0 = ["10size", "15size", "20size", "25size"]
#matching_1 = ["5prob", "10prob", "25prob", "50prob"]
matching_1 = ["25prob", "50prob", "75prob", "90prob"]

# coloring
coloring_0 = ["10size", "15size", "20size", "25size", "30size", "40size", "50size"]
coloring_1 = ["10prob", "25prob", "50prob", "75prob"]

# clique
clique_0 = ["10size", "15size", "20size", "25size"]
clique_1 = ["5prob", "10prob", "25prob", "50prob"]
clique_2 = ["3clique", "4clique", "5clique", "6clique"]

# kcolorability
kcol_0 = ["10size", "15size", "20size", "25size"]
kcol_1 = ["10prob", "25prob", "50prob", "75prob"]
kcol_2 = ["2k", "3k", "4k"]

if __name__ == "__main__":
    for i in sat_0:
        for j in sat_1:
            if i == "unsatisfiable" and j == "91-20": continue
            os.system("mkdir -p problems/sat/" + "/".join([i, j]))
            os.system("mkdir -p solutions/sat/" + "/".join([i, j]))

    for i in hamiltonian_0:
        for j in hamiltonian_1:
            os.system("mkdir -p problems/hamiltonian/" + "/".join([i, j]))
            os.system("mkdir -p solutions/hamiltonian/" + "/".join([i, j]))

    for i in matching_0:
        for j in matching_1:
            os.system("mkdir -p problems/matching/" + "/".join([i, j]))
            os.system("mkdir -p solutions/matching/" + "/".join([i, j]))

    for i in coloring_0:
        for j in coloring_1:
            os.system("mkdir -p problems/coloring/" + "/".join([i, j]))
            os.system("mkdir -p solutions/coloring/" + "/".join([i, j]))


    ## size 5 & size 10, smaller cliques
    for j in clique_1:
        # 5
        #for k in clique_2[:-2]:
        #    os.system("mkdir -p problems/clique/5size/" + "/".join([j, k]))
        #    os.system("mkdir -p solutions/clique/5size/" + "/".join([j, k]))
        # 10
        for k in clique_2[:-1]:
            os.system("mkdir -p problems/clique/10size/" + "/".join([j, k]))
            os.system("mkdir -p solutions/clique/10size/" + "/".join([j, k]))

        for i in clique_0[1:]:
            for k in clique_2:
                os.system("mkdir -p problems/clique/" + "/".join([i, j, k]))
                os.system("mkdir -p solutions/clique/" + "/".join([i, j, k]))

    for i in kcol_0:
        for j in kcol_1:
            for k in kcol_2:
                os.system("mkdir -p problems/kcolorability/" + "/".join([i, j, k]))
                os.system("mkdir -p solutions/kcolorability/" + "/".join([i, j, k]))
    print "Created problem directories"
