#! /usr/bin/env python
from get_problem_directories_soforall import *
import time as t

# echo QBF_AE
# for j in 1a 2a 3a 4a 5a; do
#     for i in 5e 10e 15e 20e; do
#         echo QBF_AE+ $j $i
#         grep 'PLAN FOUND' $directory/qbfae/$j/$i/*/* | wc | awk '{print $1}'
#         echo QBF_AE- $j $i
#         grep 'NOT FOUND' $directory/qbfae/$j/$i/*/* | wc | awk '{print $1}'
#         echo QBF_AE time_out $j $i
#         grep 'Timeout after 5400' $directory/qbfae/$j/$i/*/* | wc | awk '{print $1}'
#         echo QBF_AE_time $j $i
#         grep 'total time' $directory/qbfae/$j/$i/*/* | wc | awk '{print $1}'
#         echo QBF_AE total $j $i
#         ls ../problems-soforall/qbfae/$j/$i/* | grep '.pddl' | wc | awk '{print $1}'
#     done
# done
# 
# echo QBF_EA 
# for i in 5e 10e 15e 20e; do
#     for j in 1a 2a 3a 4a 5a; do
#         echo QBF_EA+ $i $j
#         grep 'PLAN FOUND' $directory/qbfea/$i/$j/*/* | wc | awk '{print $1}'
#         echo QBF_EA- $i $j
#         grep 'NOT FOUND' $directory/qbfea/$i/$j/*/* | wc | awk '{print $1}'
#         echo QBF_AE time_out $i $j
#         grep 'Timeout after 5400' $directory/qbfea/$i/$j/*/* | wc | awk '{print $1}'
#         echo QBF_AE total $i $j
#         ls ../problems-soforall/qbfea/$i/$j/* | grep '.pddl' | wc | awk '{print $1}'
#     done
# done
# qbf
# totalTime = []
# totalResults = []
# totalProblems = 0
# totalOptimal = 0
# totalLuckyIter = []
# s = ""
# f = open('table4.out', 'w')
# for size in range(10, topSize+1):
#   print "Size: " + str(size)
#   sizeTimes = []
#   sizeResults = []
#   sizeOptimal = 0
#   totalSizeProblems = 0
#   sizeLuckyIter = []
#   colorTime = [[],[],[],[],[],[],[],[]]
#   colorResults = [[],[],[],[],[],[],[],[]]
#   colorOptimal = [0,0,0,0,0,0,0,0]
#   totalColorProblems = [0,0,0,0,0,0,0,0]
#   colorLuckyIter = [[],[],[],[],[],[],[],[]]
#   s =  "\multirow{9}{*}{" + str(size) + "x" + str(size) + "}"
#   for colors in range(4,maxColors):
#       print " Color: " + str(colors)
#   
#       s += " & " + str(colors)
#       for rclSize in range(3,8):
#           rclTimes = []
#           rclResults = []
#           rclOptimal = 0
#           totalRclProblems = 0
#           rclLuckyIter = []
#               
#           s += " & " + '{0:.2f}'.format(sum(rclTimes, 0.0) / len(rclTimes))
#           s += " & " + '{0:.2f}'.format(sum(rclResults, 0.0) / len(rclResults))
#           s += " & " + '{0:.2f}'.format(sum(rclLuckyIter, 0.0) / len(rclLuckyIter))
#           #s += " & " + str (rclOptimal)
#           colorTime[rclSize] += [sum(rclTimes, 0.0) / len(rclTimes)]
#           colorResults[rclSize] += [sum(rclResults, 0.0) / len(rclResults)]
#           colorLuckyIter[rclSize] += [sum(rclLuckyIter, 0.0) / len(rclLuckyIter)]
#           colorOptimal[rclSize] += rclOptimal
#           totalColorProblems[rclSize] += totalRclProblems
#       s += "\\\\ \n"
#   s += "\cline{3-17} \n & Totals"
#   for i in range(3,8):
#       s += " & " + '{0:.2f}'.format(sum(colorTime[i], 0.0) / len(colorTime[i]))
#       s += " & " + '{0:.2f}'.format(sum(colorResults[i], 0.0) / len(colorResults[i]))
#       s += " & " + '{0:.2f}'.format(sum(colorLuckyIter[i], 0.0) / len(colorLuckyIter[i]))
#       #s += " & " + str(colorOptimal[i])
#   s += "\\\\ \\\\ \n"
#   f.write(s)

fs = ""
es = ""
f = open('forallTable.out', 'w')

a = 1
for i in qbf_0:
    e = 1
    total_positive_i = 0
    total_negative_i = 0
    total_time_i = 0
    total_i = 0
    fs =  "\multirow{" + str(len(qbf_2)) + "}{*}{" + str(a) + "}"
    
    for j in qbf_1:
        total_positive_j = 0
        total_negative_j = 0
        total_time_j = 0
        total_j = 0   
         
        c = 1
        fs =  " & " + str(e)  	
        
        for k in qbf_2:
            if a + 5*e > c*5 + 1 :
                fs += " & & & & "
                c += 1
                continue
            dir_name = "solutions-soforall/qbfae/" + "/".join([i, j, k]) + "/*"
            
            n_planF = int(os.popen("grep 'PLAN FOUND' " + dir_name + " | wc | awk '{print $1}'").readline())
            n_planNf = int(os.popen("grep 'NOT FOUND' " + dir_name + " | wc | awk '{print $1}'").readline())
            n_planTo = int(os.popen("grep 'Timeout after' " + dir_name + " | wc | awk '{print $1}'").readline())
            n_planTotal = int(os.popen("ls problems-soforall/qbfae/" + "/".join([i, j, k]) + "/* | grep '.pddl' | wc | awk '{print $1}'").readline())
            strTimes = os.popen("grep 'total time' " + dir_name + " | awk '{print $3}'").readlines()
            times = 0.0
            
            if len(strTimes) == 0:
                avg_time = 0
            else:
                t.sleep(4)
                print strTimes
                for i in strTimes:
                    print i
                #     times += float(i)
                # avg_time = times/float(len(strTimes))

                
            # fs += " & " + str(n_planNf + n_planF) + "/" + str(n_planTotal)
            # fs += " & " + str(n_planF)
            # fs += " & " + str(n_planNf)
            # fs += " & " + str(avg_time)
            # 
            # total_positive_i += n_planF
            # total_negative_i += n_planNf
            # total_time_i += times
            # # total_i += n_planTotal
            # 
            # total_positive_j += n_planF
            # total_negative_j += n_planNf
            # total_time_j += times
            # total_j += n_planTotal
            
            c += 1
        fs += "\\\\ \\\\ \n"
    	f.write(fs)
        e += 1
    a += 1
    

