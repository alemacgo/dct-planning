#! /usr/bin/env python
import os
from get_all_directories_soforall import *

problems = ["qbf"]

if __name__ == "__main__":
    
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
        
    print "Created problem directories"
