function land {
  landslide -i -d $2 -r -ltable $1 -t ribbon
}

function simple {
  pandoc -o $2 $1
}

for f in `cd doc && ls *.md`
do
 land doc/$f html/$f.html
done
