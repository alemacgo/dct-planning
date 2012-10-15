directory=solutions_adriana_22nov

echo SAT 
    for j in 91-20 218-50 325-75; do
        echo SAT+ $j
        grep 'PLAN FOUND' $directory/sat/*/$j/* | wc | awk '{print $1}'
        echo SAT- $j
        echo grep 'NOT FOUND' $directory/sat/*/$j/* | wc | awk '{print $1}'
    done

echo HAMILTONIAN
for i in 5size 10size 15size 20size 25size; do
        echo HAM+ $i
        grep 'PLAN FOUND' $directory/hamiltonian/$i/*/* | wc | awk '{print $1}'
        echo HAM- $i
        grep 'NOT FOUND' $directory/hamiltonian/$i/*/* | wc | awk '{print $1}'
    done

echo MATCHING
for i in 5size 10size 15size 20size; do
        echo MAT+ $i
        grep 'PLAN FOUND' $directory/matching/$i/*/* | wc | awk '{print $1}'
        echo MAT- $i
        grep 'NOT FOUND' $directory/matching/$i/*/* | wc | awk '{print $1}'
done

echo COLORING
for i in 5size 10size 15size 20size 25size; do
        echo COL+ $i
        grep 'PLAN FOUND' $directory/coloring/$i/*/* | wc | awk '{print $1}'
        echo COL- $i
        grep 'NOT FOUND' $directory/coloring/$i/*/* | wc | awk '{print $1}'
done

echo CLIQUE
for i in 5size 10size 15size 20size; do
        for k in 3clique 4clique 5clique 6clique; do
            echo CLI+ $i-$k
            grep 'PLAN FOUND' $directory/clique/$i/*/$k/* | wc | awk '{print $1}'
            echo CLI- $i-$k
            grep 'NOT FOUND' $directory/clique/$i/*/$k/* | wc | awk '{print $1}'
        done
done

echo KCOLORABILITY
for i in 5size 10size 15size 20size; do
        for k in 2k 3k 4k; do
            echo KCO+ $i-$k
            grep 'PLAN FOUND' $directory/kcolorability/$i/*/$k/* | wc | awk '{print $1}'
            echo KCO- $i-$k
            grep 'NOT FOUND' $directory/kcolorability/$i/*/$k/* | wc | awk '{print $1}'
        done
done
