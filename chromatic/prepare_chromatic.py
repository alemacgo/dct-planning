#!/usr/bin/env python
import os
from sys import argv

if len(argv) != 4:
    print "usage: ./prepare_chromatic nvers prob seed"
    exit(0)

nvers = argv[1]
prob = argv[2]
seed = argv[3]

os.system("mkdir -p solutions")
os.system("""cd ../..; ./soplan.py --output=experiments/chromatic\
        examples/kcolorability/kcolorability.dct > /dev/null""")
print "Created domain for kcolorability"

s_prob = str(int(float(argv[2])*100))
k = "1"

problem_name = "kco" + "_" + nvers + "_" + s_prob + "_" +\
                   seed + "_" + k
os.system(" ".join(["../generators/kcolorability.py ./", problem_name,\
                    nvers, prob, k, seed]))
print "Created " + problem_name
