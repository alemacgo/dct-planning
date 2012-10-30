#! /usr/bin/env python
import os
from get_all_directories_soforall import *

problems = ["qbf"]

if __name__ == "__main__":

        # QBF 2 quantifiers
        a = 1
        for i in qbf_0:
            e = 1
            for j in qbf_1:
                c = 1
                for k in qbf_2:
                    if a + 5*e > c*5 + 1:
                        c += 1
                        continue
                    os.system("mkdir -p solutions-soforall/qbfae/" + "/".join([i, j, k]))
                    os.system("mkdir -p solutions-soforall/qbfea/" + "/".join([j, i, k]))
                    c += 1
                e += 1
            a +=1

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
                        os.system("mkdir -p solutions-soforall/qbf3eae/" + "/".join([e1, a1, e2, c]))
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
                        os.system("mkdir -p solutions-soforall/qbf3aea/" + "/".join([a1, e1, a2, c]))
                        c_i += 1
                    a2_i += 1
                e1_i +=1
            a1_i += 1




        
    print "Created solution directories"
