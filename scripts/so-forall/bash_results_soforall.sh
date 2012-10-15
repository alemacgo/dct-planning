directory=solutions-soforall

echo QBF_AE
for j in 1a 2a 3a 4a 5a; do
    echo QBF_AE+ $j
    echo "grep 'PLAN FOUND' $directory/qbfae/$j/* | wc | awk " '{print $1}'
    echo QBF_AE- $j
    echo "grep 'NOT FOUND' $directory/qbfae/$j/* | wc | awk " '{print $1}'
done

echo QBF_EA 
for i in 5e 10e 15e 20e; do
    echo QBF_EA+ $i
    echo grep 'PLAN FOUND' $directory/qbfea/$i/*/* | wc | awk '{print $1}'
    echo QBF_EA- $i
    echo grep 'NOT FOUND' $directory/qbfea/$i/*/* | wc | awk '{print $1}'
done
