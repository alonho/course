function land {
  landslide -d $2 -r -c -ltable $1
}

for f in `cd doc && ls *.md`
do
 land doc/$f html/$f.html
done
