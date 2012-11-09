#! /usr/bin/env python
from dirs_all import *

first_text = """\\documentclass[a1paper]{article}\n\
                \\usepackage[left=0.5cm,top=3cm,right=1cm,nohead,nofoot]{geometry}\n\
                \\usepackage{nopageno}\n\
                \\usepackage{lscape}\n\
                \\usepackage{multirow}\n\
                \\setlength{\\evensidemargin}{-1cm}\n\
                \\setlength{\\oddsidemargin}{-1cm}\n\
                \\pagestyle{plain}\n\
                \\begin{document}\n"""
                # \\begin{landscape}\n"""

def retriveResults(dir_name, problem_dir, c, fs, total_positive_i, total_negative_i, 
                   total_time_i, total_i):
    fs = ""
    n_planF = int(os.popen("grep 'PLAN FOUND' " + dir_name + " | wc | awk '{print $1}'").readline())
    n_planNf = int(os.popen("grep 'NOT FOUND' " + dir_name + " | wc | awk '{print $1}'").readline())
    n_planTo = int(os.popen("grep 'Timeout after' " + dir_name + " | wc | awk '{print $1}'").readline())
    n_planTotal = int(os.popen("ls " + problem_dir + " | grep '.pddl' | wc | awk '{print $1}'").readline())
    strTimes = os.popen("grep 'total time' " + dir_name + " | awk '{print $3}'").readlines()
    
    times = 0.0
    
    if len(strTimes) == 0:
        avg_time = 0
    else:
        for l in strTimes:
            times += float(l)
        avg_time = times/float(len(strTimes))

    fs += " & " + str(n_planNf + n_planF) + "/" + str(n_planTotal)
    fs += " & " + str(n_planF)
    fs += " & " + str(n_planNf)
    if n_planNf + n_planF == 0:
        fs += " & -"
    else:
        fs += " & " + '{0:.2f}'.format(avg_time)
    
    total_positive_i[c-1] += n_planF
    total_negative_i[c-1] += n_planNf
    total_time_i[c-1] += times
    total_i[c-1] += n_planTotal

    return fs
    
def totalize(num_of_q ,n_cline, clauses_set, fs, f, total_positive_i, total_negative_i, 
                       total_time_i, total_i):
    
    f.write(fs + "\\cline{3-" + n_cline + "}\n")
    fs ="\multicolumn{" + str(num_of_q) + "}{c}{Total:} "
    for l in range(0,len(clauses_set)):
        fs += "& " + str(total_positive_i[l] + total_negative_i[l]) + "/" + str(total_i[l])
        fs += "& " + str(total_positive_i[l])
        fs += "& " + str(total_negative_i[l])
        if total_positive_i[l] + total_negative_i[l] == 0:
            fs += "& 0 "
            continue
        fs += "& " + '{0:.2f}'.format(total_time_i[l]/float(total_positive_i[l] + total_negative_i[l]))
    f.write(fs + "\\\\\\\\\n")
    
def writeTableHeader(clauses_set, domain, planner, quantifier_order, num_of_q, n_cline):
    f.write("\\section*{\\centering \\Large \\underline{Tests - " + domain + "-" + planner + "}}\n" + \
            "$ $\\\n")
    f.write("   \\begin{tabular}{" + num_of_q*"c" + " cccc" + (len(clauses_set)-1)*"|cccc" + "}\n")
    f.write("   " + quantifier_order + "& \multicolumn{" + str(4*len(clauses_set)) + "}{c}{Number of clauses}\\\\\n\\hline\n")
    f.write(" " + " &"*num_of_q + "\multicolumn{4}{c}{" + "} & \multicolumn{4}{c}{".join(clauses_set) + "} \\\\\\cline{" + str(num_of_q + 1) + "-" + n_cline + "}\n")
    f.write(" &"*(num_of_q -1)  + " & Total & + & - & Avg. "*(len(clauses_set)) + "\\\\\\\\\n")
      
def qbf2Table(set0, set1, clauses_set, path, planner, n_cline, num_of_q, f, plus):  

    fs = ""
    
    for i in set0:
        total_positive_i = [0]*len(clauses_set)
        total_negative_i = [0]*len(clauses_set)
        total_time_i = [0]*len(clauses_set)
        total_i = [0]*len(clauses_set)
        if plus:
            fs = "& \multirow{" + str(len(set1)) + "}{*}{" + str(i[:-1]) + "}"
        else:
            fs = "\multirow{" + str(len(set1)) + "}{*}{" + str(i[:-1]) + "}"
            
        first = False

        for j in set1:
            
            if plus and first:
                fs +=  "& & " + j[:-1]  + " "
            else:
                fs +=  " & " + j[:-1]  + " "
                first = True
                
            c = 1
            for k in clauses_set:
                                    
                if plus + int(i[:-1]) + int(j[:-1]) > int(k[:-1]) :
                    fs += "& - & - & - & -"
                    c += 1
                    continue   
                    
                dir_name = "solutions-soforall/" + path + "/".join([i, j, k]) + "/*.out" + planner
                problem_dir = "problems-soforall/" + path + "/".join([i, j, k]) + "/*"             
                fs += retriveResults(dir_name, problem_dir, c, fs, total_positive_i, 
                                     total_negative_i, total_time_i, total_i)            
                c += 1     
            fs += "	\\\\"
        totalize(num_of_q, n_cline, clauses_set, fs, f, total_positive_i, total_negative_i, 
                               total_time_i, total_i)

def addQbf2Table(set0, set1, clauses_set, domain, planner, quantifier_order, f):    
    n_cline = str(4*len(clauses_set)+2)
    writeTableHeader(clauses_set, domain, planner, quantifier_order, 2, n_cline)
    qbf2Table(set0, set1, clauses_set, domain + "/", planner, n_cline,2, f, 0)
    f.write("\\end{tabular}\n")
    
def addQbf3Table (set0, set1, set2, clauses_set, domain, planner, quantifier_order, f):
    n_cline = str(4*len(clauses_set)+3)
    writeTableHeader(clauses_set, domain, planner, quantifier_order, 3, n_cline)
    for h in set0:
        f.write("\multirow{" + str(len(set1)*(len(set2) + 2) ) + "}{*}{" + h[:-1] + "} ")
        qbf2Table(set1, set2, clauses_set, domain + "/" + h + "/", planner, n_cline, 3, f, int(h[:-1]))
        f.write("	\\\\\\cline{2-" + n_cline + "} \\\\")
    f.write("\\end{tabular}\n")
    

if __name__ == "__main__":
    f = open("resultsQbf.tex", 'w')
    f.write(first_text)
    addQbf3Table(qbf3_e0, qbf3_a0, qbf3_e1, qbf_2, "qbf3eae", "m", "E\_vars & A\_vars & E\_vars", f)
    f.write("\\pagebreak\n")    
    
    addQbf3Table(qbf3_a2, qbf3_e2, qbf3_a2, qbf_2, "qbf3aea", "m", "A\_vars & E\_vars & A\_vars", f)
    
    f.write("\\pagebreak\n")    
    
    addQbf2Table(qbf_0, qbf_1, qbf_2, "qbfae", "m", "A\_vars & E\_vars", f)
    # createTableQbf(qbf_0, qbf_1, qbf_2, "qbfae", "mp", "A\_vars & E\_vars")

    f.write("\\pagebreak\n")    
    
    addQbf2Table(qbf_1, qbf_0, qbf_2, "qbfea", "m", "E\_vars & A\_vars", f)
    
    f.write("\\pagebreak\n")    
    
    
    addQbf2Table([i[:-1] + "e" for i in qbf_0], [i[:-1] + "a" for i in qbf_1], qbf_2, "nqbfae", "m", "E\_vars & A\_vars", f)
    # createTableQbf(qbf_1, qbf_0, qbf_2, "qbfea", "mp", "E\_vars & A\_vars")

    f.write("\\end{document}")
    f.close()
    os.system("pdflatex resultsQbf.tex; rm *.aux; rm *.log; open resultsQbf.pdf ")

