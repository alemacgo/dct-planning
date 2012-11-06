#! /usr/bin/env python
import os, re, sys

problems = ["qbf"]

qbf3_e = ["20e", "40e", "60e", "80e", "100e"]
qbf3_a = ["1a", "2a", "3a", "4a", "5a"]

qbf3_a2 = ["1a", "2a", "3a", "4a"]
qbf3_e2 = ["20e", "40e", "60e", "80e", "100e", "120e", "140e"]


qbf_0 = ["1a", "2a", "3a", "4a", "5a"]
# qbf_1 = ["5e", "10e", "15e", "20e"]
qbf_1 = ["20e", "40e", "60e", "80e", "100e", "120e"]

# qbf_2 = ["6c", "11c", "16c", "21c","26c", "31c"]

qbf_2 = ["20c","30c", "60c", "90c", "120c", "150c", "180c"]


if __name__ == "__main__":
    
    # QBF 2 quantifiers
    for i in qbf_0:
        for j in qbf_1:
            for c in qbf_2:
                if int(i[:-1]) + int(j[:-1]) > int(c[:-1]):
                    continue
                os.system("mkdir -p problems-soforall/qbfae/" + "/".join([i, j, c]))
                os.system("mkdir -p solutions-soforall/qbfae/" + "/".join([i, j, c]))
                
                os.system("mkdir -p problems-soforall/nqbfae/" + "/".join([i[:-1] + "e", j[:-1] + "a", c]))
                os.system("mkdir -p solutions-soforall/nqbfae/" + "/".join([i[:-1] + "e", j[:-1] + "a", c]))
                
                os.system("mkdir -p problems-soforall/qbfea/" + "/".join([j, i, c]))
                os.system("mkdir -p solutions-soforall/qbfea/" + "/".join([j, i, c]))

        
        #QBF 3 EAE 
        
    for e1 in qbf3_e:
        for a1 in qbf3_a:
            for e2 in qbf3_e:
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
                
                
        
    print "Created problem directories"
