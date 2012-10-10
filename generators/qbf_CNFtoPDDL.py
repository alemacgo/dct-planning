#! /usr/bin/env python
from sys import argv
import math

def tokenize(input):
    cnf_info = None
    for line in input:
        if line[0] == 'c':
            continue    
        cnf_info = line.partition("p")[2]
        if cnf_info != '':
            break
    for line in input:
        if line[0] == 'c' or line[0] == 'p':
            continue
        a_vars = (line.partition("a")[2]).split()
        if cnf_info != '':
            break
    for line in input:
        if line[0] == 'c' or line[0] == 'p' or line[0] == 'a':
            continue
        e_vars = (line.partition("e")[2]).split()
        if cnf_info != '':
            break
    cnf = cnf_info.split()
    num_vars = int(cnf[1])
    num_clau = int(cnf[2])
        
    clausulas = []
    for line in input:
        if line[0] == 'c' or line[0] == 'p' or line[0] == 'a' or line[0] == 'e':
            continue
        elif line[0] == '%':
            break
        clausulas.append(line.split())
    return clausulas, num_vars, num_clau, a_vars, e_vars

filename = argv[3].partition(".")[0]  
prenex_file = open(argv[3]).readlines()

tokens, num_vars, num_clau, a_vars, e_vars = tokenize(prenex_file)
pddl_file = open(argv[1] + filename.split("/")[-1] + ".pddl", "w")

if argv[2] == "-e":
    aux = a_vars
    a_vars = e_vars
    e_vars = aux

pddl_file.write("(define (problem p)\n")
pddl_file.write("\t(:domain qbf)\n")
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
    last = "zero"
    so_forall_vars = []
    for i in range (0, len(a_vars)):
        if (abs(int(a_vars[i+1])) == 0):
            break
        var1 = abs(int(a_vars[i]))
        if var1 == 1:
            var1 = "zero"
        elif var1 == maxim:
            var1 = "max"
        else:
            var1 = "obj" + str(var1 - 1)
        
        so_forall_vars += [var1]
            
        var2 = abs(int(a_vars[i+1]))
        if var2 == 1:
            var2 = "zero"
        elif var2 == maxim:
            var2 = "max"
        else:
            var2 = "obj" + str(var2 - 1)
            
        last = var2
        pddl_file.write("\t\t(so-forall_suc_t " + var1 + " " + var2 + ")\n")
        
    #(not_e) forall var
    #t is forall relation
    so_forall_vars += [last]
    pddl_file.write("\t\t(so-forall_zero_t " + so_forall_vars[0] + ")\n")
    pddl_file.write("\t\t(so-forall_max_t " + so_forall_vars[-1] + ")\n")
    pddl_file.write("\t\t(not_t " + ")\n\t\t(not_t ".join(so_forall_vars) + ")\n")
    pddl_file.write("\t\t(not_e " + ")\n\t\t(not_e ".join(so_forall_vars) + ")\n")
    
    so_exist_vars = []
    for var in e_vars:
        
        aux = abs(int(var))
        if aux == 0:
            break
            
        if aux == 1:
            trueVar = "zero"
        elif aux == maxim:
            trueVar = "max"
        else:
            trueVar = "obj" + str(aux - 1)
        
        so_exist_vars += [trueVar]
    
    # r is the so-exist relation
    pddl_file.write("\t\t(not_r " + ")\n\t\t(not_r ".join(so_exist_vars) + ")\n")
    pddl_file.write("\t\t(e " + ")\n\t\t(e ".join(so_exist_vars) + ")\n")
    
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
