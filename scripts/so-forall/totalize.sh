#! /bin/sh
directory=solutions-soforall

echo QBF_AE
for j in 1a 2a 3a 4a 5a; do
    for i in 5e 10e 15e 20e; do
        echo QBF_AE+ $j $i
        grep 'PLAN FOUND' $directory/qbfae/$j/$i/*/* | wc | awk '{print $1}'
        echo QBF_AE- $j $i
        grep 'NOT FOUND' $directory/qbfae/$j/$i/*/* | wc | awk '{print $1}'
        echo QBF_AE time_out $j $i
        grep 'Timeout after 5400' $directory/qbfae/$j/$i/*/* | wc | awk '{print $1}'
        echo QBF_AE_time $j $i
        grep 'total time' $directory/qbfae/$j/$i/*/* | wc | awk '{print $1}'
        echo QBF_AE total $j $i
        ls problems-soforall/qbfae/$j/$i/* | grep '.pddl' | wc | awk '{print $1}'
    done
done

echo QBF_EA 
for i in 5e 10e 15e 20e; do
    for j in 1a 2a 3a 4a 5a; do
        echo QBF_EA+ $i $j
        grep 'PLAN FOUND' $directory/qbfea/$i/$j/*/* | wc | awk '{print $1}'
        echo QBF_EA- $i $j
        grep 'NOT FOUND' $directory/qbfea/$i/$j/*/* | wc | awk '{print $1}'
        echo QBF_AE time_out $i $j
        grep 'Timeout after 5400' $directory/qbfea/$i/$j/*/* | wc | awk '{print $1}'
        echo QBF_AE total $i $j
        ls problems-soforall/qbfea/$i/$j/* | grep '.pddl' | wc | awk '{print $1}'
    done
done

    

