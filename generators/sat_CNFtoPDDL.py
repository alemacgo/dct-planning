#! /usr/bin/env python
from sys import argv
import math

def tokenize(input):
    for line in input:
        cnf_info = line.partition("p")[2]
        if cnf_info != '':
            break
    cnf = cnf_info.split()
    num_vars = int(cnf[1])
    num_clau = int(cnf[2])
        
    clausulas = []
    for line in input:
        if line[0] == 'c' or line[0] == 'p':
            continue
        elif line[0] == '%':
            break
        clausulas.append(line.split())
    return clausulas, num_vars, num_clau

filename = argv[1].partition(".")[0] 
prenex_file = open(argv[1]).readlines()

tokens, num_vars, num_clau = tokenize(prenex_file)

pddl_file = open(argv[2] + filename.split("/")[-1] + ".pddl", "w")

pddl_file.write("(define (problem p)\n")
pddl_file.write("\t(:domain sat)\n")
pddl_file.write("\t(:objects ")

if num_vars > 0: 
    
    maxim = max(num_vars, num_clau) 
    for i in range (1,maxim-1):
        pddl_file.write("\t\t\tobj"+ str(i)+" \n")
    pddl_file.write("\n\t)\n")
    
    pddl_file.write("\t(:init\n\t\t(guess)\n\t\t(suc zero obj1)\n")
    for i in range (1,maxim-2):
        pddl_file.write("\t\t(suc obj" + str(i) +" obj" + str(i+1) + ")\n")
    pddl_file.write("\t\t(suc obj" + str(maxim-2) +" max" + ")\n")
    
    pddl_file.write("\t\t(not_t zero)\n")
    for i in range (1,maxim-1):
        pddl_file.write("\t\t(not_t obj" + str(i) + ")\n")
    pddl_file.write("\t\t(not_t max)\n")
    
    clause  = 1
    for i in tokens:
        for j in i:
            number = int(j)
            if number == 0:
                continue
            
            if number > 0:
                signo = "P "
            else:
                signo = "N "
            
            number = abs(number)
            
            if number == 1:
                variable = "zero"
            elif number == maxim:
                variable = "max"
            else:
                variable = "obj" + str(number-1)
                
            if clause == 1:
                pddl_file.write("\t\t("+ signo + variable +" zero)\n")
            elif clause == maxim:
                pddl_file.write("\t\t("+ signo + variable +" max)\n")
            else:
                pddl_file.write("\t\t("+ signo + variable +" obj" + str(clause-1) + ")\n")
        
        clause += 1
    
    pddl_file.write("\t)\n")
    
    pddl_file.write("\t(:goal (holds_goal)\n\t)\n)")
    
         

#print num_vars, num_clau

#print tokens
