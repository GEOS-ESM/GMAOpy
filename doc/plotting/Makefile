
.SUFFIXES: .py .png

SOURCES = example1.png example10.png example11.png example12.png example13.png example14.png example15.png example16.png example17.png example18.png example19.png example2.png example20.png example21.png example22.png example23.png example24.1.png example24.0.png example24.2.png example24.3.png example24.4.png example24.5.png example24.png example25.png example3.1.png example3.2.png example3.png example4.png example5.png example6.png example7.1.png example7.2.png example7.3.png example7.png example8.png example9.png

OBJECTS = $(SOURCES:.py=.png)

main: $(OBJECTS)

clean:
	-rm -f *.png

.py.png:
	python $*.py
