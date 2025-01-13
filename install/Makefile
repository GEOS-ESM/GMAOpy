
dist: file
	echo "done"

quick: nomake
	echo "done"

file:
	cd ..; cd doc; make -B html; cd ..; nobin; python install/setup.py sdist

nomake:
	cd ..; nobin; python install/setup.py sdist

ext:
	cd ..; python install/cc.py install --install-lib=.; rm -fr build; rm -f semperpy*egg*info*
