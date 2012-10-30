#! /usr/bin/env python
from get_all_directories_soforall import *


def count (prob_name, prob_path, planner):
    sol_name = "solutions-soforall/" + prob_path + prob_name + ".out" + planner
    result = "problems-soforall/" + prob_path + prob_name + ".result"
    
    found = int(os.popen("grep 'PLAN FOUND' " + sol_name + " | wc | awk '{print $1}'" ).readline())
    nfound = int(os.popen("grep 'PLAN NOT FOUND' " + sol_name + " | wc | awk '{print $1}'" ).readline())
    isTrue = int(os.popen("grep 'TRUE' " + result + " | wc | awk '{print $1}'" ).readline())
    
    # print "Found: " + str(found_ae) + "     nFound: " + str(nfound_ae) + "      isTrue: " + str(isTrue_ae)
    
    if found:
        if not isTrue:
            print " Error in: " + sol_name_ae 
            print "Found: " + str(found) + "     nFound: " + str(nfound) + "      isTrue: " + str(isTrue)
            
    if nfound:
        if isTrue:
            print " Error in: " + sol_name_ae
            print "Found: " + str(found) + "     nFound: " + str(nfound) + "      isTrue: " + str(isTrue)
            
def check(planner):
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
                    prob_name_ae = "_".join(["qbf", i , j , k , str(seed)])
                    prob_path_ae = "qbfae/" + "/".join([i, j, k]) + "/"
                    prob_name_ea = "_".join(["qbf", j , i , k , str(seed)])
                    prob_path_ea = "qbfea/" + "/".join([j, i, k]) + "/"

                    count(prob_name_ae, prob_path_ae, planner)
                    # count(prob_name_ea, prob_path_ea, planner)

                c += 1
            e += 1
        a += 1
        
        #QBF 3 EAE 
        
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
                        for seed in range (5):
                            prob_name = "_".join(["qbf3eae", e1, a1, e2, c, str(seed)])
                            prob_path = "/".join(["qbf3eae", e1, a1, e2, c]) + "/"
                            count(prob_name, prob_path, planner)
                        c_i += 1
                    e2_i += 1
                a1_i +=1
            e1_i += 1
            
            #QBF 3 AEA
            
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
                            for seed in range (5):
                                prob_name = "_".join(["qbf3aea", a1, e1, a2, c, str(seed)])
                                prob_path = "/".join(["qbf3aea", a1, e1, a2, c]) + "/"
                                count(prob_name, prob_path, planner)
                            c_i += 1
                        a2_i += 1
                    e1_i +=1
                a1_i += 1
        
# check("mp")
check("m")

