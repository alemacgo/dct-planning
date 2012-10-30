#! /usr/bin/env python
from sys import argv
import math

def getQuantifiedVars(var_set):
    
    processed_vars = []
    for i in var_set:
         
        var = abs(int(i))
        if var == 1:
            var = "zero"
        elif var == maxim:
            var = "max"
        elif var == 0:
            break
        else:
            var = "obj" + str(var - 1)
            
        processed_vars += [var]
    return processed_vars    

def tokenize(input):
    a_vars = []
    e_vars = []
    for line in input:
        if line[0] == 'p':
            cnf_info = line.partition("p")[2]
        elif line[0] == 'e':
            e_vars += [(line.partition("e")[2]).split()]
        elif line[0] == 'a':
            a_vars += [(line.partition("a")[2]).split()]
            
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

filename = argv[3].partition(".")[0]  
prenex_file = open(argv[3]).readlines()

tokens, num_vars, num_clau, a_vars, e_vars = tokenize(prenex_file)
pddl_file = open(argv[1] + filename.split("/")[-1] + ".pddl", "w")

pddl_file.write("(define (problem p)\n")

if argv[2] == "-e":
    aux = a_vars
    a_vars = e_vars
    e_vars = aux
    pddl_file.write("\t(:domain qbfeae)\n")
else:
    pddl_file.write("\t(:domain qbfaea)\n")

pddl_file.write("\t(:objects ")

if num_vars > 0: 
    
    maxim = max(num_vars, num_clau) 
    for i in range (1,maxim-1):
        pddl_file.write("\t\t\tobj"+ str(i)+" \n")
    pddl_file.write("\n\t)\n")
    
    pddl_file.write("\t(:init\n\t\t(begin)\n\t\t(suc zero obj1)\n")
    
    for i in range (1,maxim-2):
        pddl_file.write("\t\t(suc obj" + str(i) +" obj" + str(i+1) + ")\n")
    pddl_file.write("\t\t(suc obj" + str(maxim-2) +" max" + ")\n")

    processed_a_vars = []
    for i in a_vars:
        processed_a_vars += [getQuantifiedVars(i)]
        
    processed_e_vars = []
    for i in e_vars:
        processed_e_vars += [getQuantifiedVars(i)]
        
    #(not_e) forall var
    #t is forall relation
    for i in range(0, len(processed_a_vars)):
        pddl_file.write("\t\t(not_t" + str(i) + " " + (")\n\t\t(not_t" + str(i) + " " ).join(processed_a_vars[i]) + ")\n")
        pddl_file.write("\t\t(ist" + str(i) + " " + (")\n\t\t(ist" + str(i) + " " ).join(processed_a_vars[i]) + ")\n")
        pddl_file.write("\t\t(so-forall_zero_t" + str(i) + " " + processed_a_vars[i][0] + ")\n")
        pddl_file.write("\t\t(so-forall_max_t"  + str(i) + " " + processed_a_vars[i][-1] + ")\n")
        for j in range(0,len(processed_a_vars[i])):
            if j == len(processed_a_vars[i]) - 1:
                break
            pddl_file.write("\t\t(so-forall_suc_t" + str(i) + " " + processed_a_vars[i][j] + " " + processed_a_vars[i][j+1] + ")\n")
            
    for i in range(0, len(processed_e_vars)):
        pddl_file.write("\t\t(not_e" + str(i) + " " + (")\n\t\t(not_e" + str(i) + " " ).join(processed_e_vars[i]) + ")\n")
        pddl_file.write("\t\t(ise" + str(i) + " " + (")\n\t\t(ise" + str(i) + " " ).join(processed_e_vars[i]) + ")\n")
    
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
