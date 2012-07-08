function land {
  landslide -i -d $2 -r -c -ltable $1
}

function simple {
  pandoc -o $2 $1
}

for f in `cd doc && ls *.md`
do
 land doc/$f html/$f.html
 simple doc/$f simplehtml/$f.html
done
