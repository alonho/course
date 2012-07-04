function land {
  landslide -d html/$1.html -r -c -ltable doc/$1.md
}
land args
land contextmanagers
land decorators
land generators
land internals
land metaclasses
land staticclass