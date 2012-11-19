#! /usr/bin/env python
import os, re, sys

problems = ["qbf","n_coloring"]

qbf3_e0 = ["10e", "30e", "50e"]
qbf3_a0 = ["1a", "2a", "3a", "4a"]
qbf3_e1 = ["5e", "10e", "30e", "50e"]

qbf3_a2 = ["1a", "2a"]
qbf3_e2 = ["15e", "20e", "60e", "80e", "100e"]

qbf_0 = ["1a", "2a", "3a", "4a"]
qbf_1 = ["15e", "30e", "60e", "80e", "100e"]

qbf_2 = ["20c", "40c", "60c", "80c", "100c", "150c", "200c"]

coloring_0 = ["4s", "5s", "6s", "7s", "8s", "9s"]
coloring_1 = ["20p", "40p","60p", "80p", "100p"]

if __name__ == "__main__":
    
    # QBF 2 quantifiers
    for i in qbf_0:
        for j in qbf_1:
            for c in qbf_2:
                if int(i[:-1]) + int(j[:-1]) > int(c[:-1]):
                    continue
                os.system("mkdir -p problems-soforall/qbfae/" + "/".join([i, j, c]))
                os.system("mkdir -p solutions-soforall/qbfae/" + "/".join([i, j, c]))
                
                os.system("mkdir -p problems-soforall/nqbfae/" + "/".join([j[:-1] + "a", i[:-1] + "e", c]))
                os.system("mkdir -p solutions-soforall/nqbfae/" + "/".join([j[:-1] + "a", i[:-1] + "e", c]))
                
                os.system("mkdir -p problems-soforall/qbfea/" + "/".join([j, i, c]))
                os.system("mkdir -p solutions-soforall/qbfea/" + "/".join([j, i, c]))

        
        #QBF 3 EAE 
        
    for e1 in qbf3_e0:
        for a1 in qbf3_a0:
            for e2 in qbf3_e1:
                for c in qbf_2:
                    if int(a1[:-1]) + int(e1[:-1]) + int(e2[:-1]) > int(c[:-1]):
                        continue
                    os.system("mkdir -p problems-soforall/qbf3eae/" + "/".join([e1, a1, e2, c]))
                    os.system("mkdir -p solutions-soforall/qbf3eae/" + "/".join([e1, a1, e2, c]))
            
            #QBF 3 AEA
            
    for a1 in qbf3_a2:
        for e1 in qbf3_e2:
            for a2 in qbf3_a2:
                for c in qbf_2:
                    if int(a1[:-1]) + int(e1[:-1]) + int(a2[:-1]) > int(c[:-1]):
                        continue
                    os.system("mkdir -p problems-soforall/qbf3aea/" + "/".join([a1, e1, a2, c]))
                    os.system("mkdir -p solutions-soforall/qbf3aea/" + "/".join([a1, e1, a2, c]))
                
    #NColoring
    for i in coloring_0:
        for j in coloring_1:
                os.system("mkdir -p problems-soforall/n3coloring/" + "/".join([i,j]))
                os.system("mkdir -p solutions-soforall/n3coloring/" + "/".join([i,j]))
                
    print "Created plem directories"
