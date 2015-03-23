SRCDIR := doc
OUTDIR := html
THEME ?= default

SOURCES := $(wildcard ${SRCDIR}/*.md)
OUTPUTS := $(patsubst ${SRCDIR}/%.md,${OUTDIR}/%.md.html,${SOURCES})

all : $(OUTPUTS)

${OUTDIR}/%.md.html : ${SRCDIR}/%.md
	landslide -i -d $@ -r -ltable $< -t ${THEME}

clean :
	rm -f $(OUTPUTS)
