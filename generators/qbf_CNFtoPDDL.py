#! /usr/bin/env python
from sys import argv
import math
import re

problems = "qbf3eae|qbf3aea|qbfae|qbfea"

def getDomain(problem):
    return re.search(problems, problem).group(0)

def tokenize(input):
    a_vars = []
    e_vars = []
    for line in input:
        if line[0] == 'p':
            cnf_info = line.partition("p")[2]
        elif line[0] == 'e':
            e_vars += [(line.partition("e")[2]).split()[:-1]]
        elif line[0] == 'a':
            a_vars += [(line.partition("a")[2]).split()[:-1]]
            
    cnf = cnf_info.split()
    num_vars = int(cnf[1])
    num_clau = int(cnf[2])
        
    clausulas = []
    for line in input:
        if line[0] == 'c' or line[0] == 'p' or line[0] == 'a' or line[0] == 'e':
            continue
        elif line[0] == '%' or line[0] == '':
            break
        clausulas.append(line.split())
    return clausulas, num_vars, num_clau, a_vars, e_vars

filename = argv[2].partition(".")[0]  
prenex_file = open(argv[2]).readlines()

tokens, num_vars, num_cls, a_vars, e_vars = tokenize(prenex_file)
pddl_file = open(argv[1] + filename.split("/")[-1] + ".pddl", "w")

pddl_file.write("(define (problem p)\n")
pddl_file.write("\t(:domain " + getDomain(filename) + ")\n")
pddl_file.write("\t(:objects ")

if num_vars > 0: 
        
    for i in range(1,num_vars + 1):
        pddl_file.write("\t\t\tvar"+ str(i)+" \n")
    for i in range(1, num_cls + 1):
        pddl_file.write("\t\t\tcls"+ str(i)+" \n")
    pddl_file.write("\n\t)\n")
    
    pddl_file.write("\t(:init\n\t\t(begin)\n")
    
    for i in range(1,num_vars + 1):
        pddl_file.write("\t\t(var var"+ str(i)+")\n")
    for i in range(1, num_cls + 1):
        pddl_file.write("\t\t(cls cls"+ str(i)+")\n")
    
    # pddl_file.write("\t\t(var_min var" + str(1) + ")\n")
    # pddl_file.write("\t\t(var_max var" + str(num_vars) + ")\n")
    # pddl_file.write("".join(["\t\t(suc_var var" + str(t[0]) + " var" + str(t[1]) +")\n" for t in zip (range(1,num_vars), range(2,num_vars + 1))]))
    pddl_file.write("\t\t(cls_min cls" + str(1) + ")\n")
    pddl_file.write("\t\t(cls_max cls" + str(num_cls) + ")\n")
    pddl_file.write("".join(["\t\t(cls_suc cls" + str(t[0]) + " cls" + str(t[1]) +")\n" for t in zip (range(1,num_cls), range(2,num_cls + 1))]))
    
    i = 0
    for a_list in a_vars:
        pddl_file.write("\t\t(not_a" + str(i) + " var" + (")\n\t\t(not_a" + str(i) + " var").join(a_list) + ")\n")
        pddl_file.write("\t\t(isa" + str(i) + " var" + (")\n\t\t(isa" + str(i) + " var").join(a_list) + ")\n")
        pddl_file.write("\t\t(isa" + str(i) + "_min var" + a_list[0] + ")\n")
        pddl_file.write("\t\t(isa" + str(i) + "_max var" + a_list[-1] + ")\n")
        pddl_file.write("".join(["\t\t(isa" + str(i) + "_suc var" + t[0] + " var" + t[1] +")\n" for t in zip (a_list[:-1], a_list[1:])]))
        i += 1
    
    i = 0
    for e_list in e_vars:
        pddl_file.write("\t\t(ise" + str(i) + " var" + (")\n\t\t(ise" + str(i) + " var").join(e_list) + ")\n")
        pddl_file.write("\t\t(not_e" + str(i) + " var" + (")\n\t\t(not_e" + str(i) + " var").join(e_list) + ")\n")
        
        i += 1
         
    clause  = 1
    for i in tokens:
        for j in i:
            number = int(j)
            if number == 0:
                continue
            
            if number > 0:
                signo = "P"
            else:
                signo = "N"
            
            number = abs(number)
            
            pddl_file.write("\t\t("+ signo + " var" + str(number) + " cls" + str(clause) + ")\n")
        
        clause += 1
    
    pddl_file.write("\t)\n")
    
    pddl_file.write("\t(:goal (holds_goal)\n\t)\n)")
    
         

#print num_vars, num_clau

#print tokens
