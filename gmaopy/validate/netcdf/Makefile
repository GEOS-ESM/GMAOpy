#----------------------------------------------------------------------------
# VeryPy Copyright SynopticView 2009-2010
# http://www.synopticview.com
#
# Claude Gibert, December 2009
#----------------------------------------------------------------------------

TESTS = file.py
SUBDIRS =

cmd=sp

run_tests = $(foreach t, $(TESTS), ./$(t:.py=.ok))

.SUFFIXES :
.SUFFIXES : .ok .py

./%.ok: %.py
	$(cmd) $< > $*.out 2>&1
	touch $@; echo $@

all: $(run_tests) subdirectories success

success:
	@touch success

subdirectories:
	@for d in $(SUBDIRS); do cd $$d; make; cd ..; done

clean ::
	@for d in $(SUBDIRS); do cd $$d; make clean; cd ..; done; rm -f $(OKEYS) *.out success *.ok
