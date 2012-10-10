#! /usr/bin/env python
import os

problems = ["qbf"]

# qbf
qbf_0 = ["1a", "2a", "3a", "4a", "5a"]
qbf_1 = ["5e", "10e", "15e", "20e"]
qbf_2 = ["6c", "11c", "16c", "21c"]

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
                os.system("mkdir -p problems-soforall/qbfae/" + "/".join([i, j, k]))
                os.system("mkdir -p solutions-soforall/qbfae/" + "/".join([i, j, k]))
                os.system("mkdir -p problems-soforall/qbfea/" + "/".join([j, i, k]))
                os.system("mkdir -p solutions-soforall/qbfea/" + "/".join([j, i, k]))
                c += 1
            e += 1
        a +=1
        
    print "Created problem directories"
