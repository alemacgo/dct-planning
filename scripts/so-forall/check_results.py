#! /usr/bin/env python
from dirs_all import *


def count (prob_name, prob_path, planner, isNqbf):
    sol_name = "solutions-soforall/" + prob_path + prob_name + ".out" + planner
    result = "problems-soforall/" + prob_path + prob_name + ".result"
    
    found = int(os.popen("grep 'PLAN FOUND' " + sol_name + " | wc | awk '{print $1}'" ).readline())
    nfound = int(os.popen("grep 'PLAN NOT FOUND' " + sol_name + " | wc | awk '{print $1}'" ).readline())
    isTrue = int(os.popen("grep 'TRUE' " + result + " | wc | awk '{print $1}'" ).readline())
        
    if isNqbf:
        if found:
            if isTrue:
                print " Error in: " + sol_name 
                print "Found: " + str(found) + "     nFound: " + str(nfound) + "      isTrue: " + str(isTrue)
            
        if nfound:
            if not isTrue:
                print " Error in: " + sol_name
                print "Found: " + str(found) + "     nFound: " + str(nfound) + "      isTrue: " + str(isTrue)
        
    else:
        if found:
            if not isTrue:
                print " Error in: " + sol_name 
                print "Found: " + str(found) + "     nFound: " + str(nfound) + "      isTrue: " + str(isTrue)
            
        if nfound:
            if isTrue:
                print " Error in: " + sol_name
                print "Found: " + str(found) + "     nFound: " + str(nfound) + "      isTrue: " + str(isTrue)
            
def check(planner):

    for i in qbf_0:
        for j in qbf_1:
            for c in qbf_2:
                if int(i[:-1]) + int(j[:-1]) > int(c[:-1]):
                    continue
                for seed in range(5):
                    prob_name_ae = "_".join(["qbf", i , j , c , str(seed)])
                    prob_path_ae = "qbfae/" + "/".join([i, j, c]) + "/"
                    
                    prob_name_nae = "_".join(["qbf",j[:-1] + "a" , i[:-1] + "e", c , str(seed)])
                    prob_path_nae = "nqbfae/" + "/".join([j[:-1] + "a" , i[:-1] + "e" , c]) + "/"
                    
                    prob_name_ea = "_".join(["qbf", j , i , c , str(seed)])
                    prob_path_ea = "qbfea/" + "/".join([j, i, c]) + "/"

                    count(prob_name_nae, prob_path_nae, planner, True)
                    count(prob_name_ae, prob_path_ae, planner, False)
                    count(prob_name_ea, prob_path_ea, planner, False)

        #QBF 3 EAE 

    for e1 in qbf3_e0:
        for a1 in qbf3_a0:
            for e2 in qbf3_e1:
                for c in qbf_2:
                    if int(a1[:-1]) + int(e1[:-1]) + int(e2[:-1]) > int(c[:-1]):
                        continue
                    for seed in range (3):
                        prob_name = "_".join(["qbf3eae", e1, a1, e2, c, str(seed)])
                        prob_path = "/".join(["qbf3eae", e1, a1, e2, c]) + "/"
                        count(prob_name, prob_path, planner, False)
    
        #QBF 3 AEA
    
    for a1 in qbf3_a2:
        for e1 in qbf3_e2:
            for a2 in qbf3_a2:
                for c in qbf_2:
                    if int(a1[:-1]) + int(e1[:-1]) + int(a2[:-1]) > int(c[:-1]):
                        continue
                        prob_name = "_".join(["qbf3aea", a1, e1, a2, c, str(seed)])
                        prob_path = "/".join(["qbf3aea", a1, e1, a2, c]) + "/"
                        count(prob_name, prob_path, planner, False)
    #     
# check("mp")
check("m")

