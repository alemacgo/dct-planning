#! /usr/bin/env python
from get_all_directories_soforall import *

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
                
def createTable(set0, set1, set2, domain, planner, separated, f):
    fs = ""
        
    if separated:
        f = open(domain + "_" + planner + "_table.tex", 'w')              
        f.write(first_text)
        
        
    f.write("\\section*{\\centering \\Large \\underline{Tests - " + domain + "-" + planner + "}}\n" + \
            "$ $\\\n")
    f.write("   \\begin{tabular}{cc ccccc" + (len(set2)-1)*"|ccccc" + "}\n")
    
    if domain == "qbfea":
        quantifier_order = "E\_vars & A\_vars"
    else:
        quantifier_order = "A\_vars & E\_vars"
        
    f.write("   " + quantifier_order + "& \multicolumn{" + str(5*len(set2)) + "}{c}{Number of clauses}\\\\\n\\hline\n")
    n_cline = str(5*len(set2)+2)
    f.write("   & & " + "\multicolumn{5}{c}{" + "} & \multicolumn{5}{c}{".join(set2) + "} \\\\\\cline{3-" + n_cline + "}\n")
    f.write("& " + "& Total & + & - & Avg. & Hzn "*len(set2) + "\\\\\\\\\n")

    total_positive = [0]*len(set2)
    total_negative = [0]*len(set2)
    total_time = [0]*len(set2)
    total = [0]*len(set2)

    a = 1
    for i in set0:
        e = 1
        total_positive_i = [0]*len(set2)
        total_negative_i = [0]*len(set2)
        total_time_i = [0]*len(set2)
        total_i = [0]*len(set2)

        if domain == "qbfea":
            fs =  "\multirow{" + str(len(set1)) + "}{*}{" + str(a*5) + "}"
        else:
            fs =  "\multirow{" + str(len(set1)) + "}{*}{" + str(a) + "}"
    
        for j in set1:
         
            c = 1
            
            if domain == "qbfea":
                fs +=  " & " + str(e)  + " "
            else:
                fs +=  " & " + str(e*5)  + " "
        
            for k in set2:
                
                if domain == "qbfea":
                    count = 5*a + e
                else:
                    count = a + 5*e
                    
                if count > c*5 + 1 :
                    fs += "& - & - & - & - & -"
                    c += 1
                    continue
                dir_name = "solutions-soforall/" + domain + "/" + "/".join([i, j, k]) + "/*.out" + planner
                problem_dir = "problems-soforall/" + domain + "/" + "/".join([i, j, k]) + "/*"
                            
                n_planF = int(os.popen("grep 'PLAN FOUND' " + dir_name + " | wc | awk '{print $1}'").readline())
                n_planNf = int(os.popen("grep 'NOT FOUND' " + dir_name + " | wc | awk '{print $1}'").readline())
                n_planTo = int(os.popen("grep 'Timeout after' " + dir_name + " | wc | awk '{print $1}'").readline())
                n_planTotal = int(os.popen("ls " + problem_dir + " | grep '.pddl' | wc | awk '{print $1}'").readline())
                strTimes = os.popen("grep 'total time' " + dir_name + " | awk '{print $3}'").readlines()
                strHorizons = os.popen("grep 'PLAN FOUND' " + dir_name + " | awk '{print $3}'").readlines()
                print strHorizons
                times = 0.0
                horizons = 0.0
                avg_horizons = 0.0
                h1 = pow(2,a)*(c*5 + 1 + 10) + 1
                h2 = pow(2,a)*(c*5 + 1 + 11) + 1
                
                if len(strHorizons) == 0:
                    avg_horizon = 0
                else:
                    for l in strHorizons:
                        horizons += float(l)
                    avg_horizons = horizons/float(len(strHorizons))
                
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
                    fs += " & -"
                else:
                    fs += " & " + '{0:.2f}'.format(avg_time)
                    fs += " & " + str(h1) + "/" + '{0:.1f}'.format(avg_horizons) + "/" + str(h2)
                    # fs += " & " + '{0:.1f}'.format(avg_horizons)
                    
            
                total_positive_i[c-1] += n_planF
                total_negative_i[c-1] += n_planNf
                total_time_i[c-1] += times
                total_i[c-1] += n_planTotal
            
                total_positive[c-1] += n_planF
                total_negative[c-1] += n_planNf
                total_time[c-1] += times
                total[c-1] += n_planTotal
            
                c += 1
            fs += "	\\\\"
            e += 1
        f.write(fs + "\\cline{3-" + n_cline + "}\n")
        fs ="\multicolumn{2}{c}{Total:} "
        for l in range(0,len(set2)):
            fs += "& " + str(total_positive_i[l] + total_negative_i[l]) + "/" + str(total_i[l])
            fs += "& " + str(total_positive_i[l])
            fs += "& " + str(total_negative_i[l])
            if total_positive_i[l] + total_negative_i[l] == 0:
                fs += "& 0 "
                fs += "& - " 
                continue
            fs += "& " + '{0:.2f}'.format(total_time_i[l]/float(total_positive_i[l] + total_negative_i[l]))
            fs += "& - " 
            
        f.write(fs + "\\\\\\\\\n")
        a += 1
    
    f.write("\\end{tabular}\n")
    if separated:
        f.write("\\end{document}")
        f.close()

separated = False
f = None

if not separated:
    f = open("results.tex", 'w')
    f.write(first_text)

createTable(qbf_0, qbf_1, qbf_2, "qbfae", "m", separated, f)
createTable(qbf_0, qbf_1, qbf_2, "qbfae", "mp", separated, f)
# createTable(qbf_0, qbf_1, qbf_2, "qbfae", "lama", separated)
if not separated:
    f.write("\\pagebreak\n")
    
createTable(qbf_1, qbf_0, qbf_2, "qbfea", "m", separated, f)
createTable(qbf_1, qbf_0, qbf_2, "qbfea", "mp", separated, f)
# createTable(qbf_1, qbf_0, qbf_2, "qbfea", "lama", separated)

if separated:
    os.system("pdflatex qbfae_m_table.tex; pdflatex qbfae_mp_table.tex; pdflatex qbfea_m_table.tex; pdflatex qbfea_mp_table.tex;")
    os.system("pdftk qbfae_m_table.pdf qbfae_mp_table.pdf qbfea_m_table.pdf qbfea_mp_table.pdf cat output results.pdf")
    os.system("rm *.aux; rm *.log; rm *.tex; rm qbfae_m_table.pdf qbfae_mp_table.pdf qbfea_m_table.pdf qbfea_mp_table.pdf")
else:
    f.write("\\end{document}")
    f.close()
    os.system("pdflatex results.tex; rm *.aux; rm *.log; open results.pdf ")

