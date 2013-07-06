all: test-result.xml
test-result.xml: test.yaml proctrace.py
	python proctrace.py $< > $@
test.yaml: main-n
	./$< 2> $@
main-n: main-n.c b.c
	gcc $^ -o $@
main-n.c: main.c mainproc.py
	python mainproc.py $< > $@
b.c: a.c a.h c-to-c.py
	python c-to-c.py $< > $@
clean:
	rm -f b.c main-n.c main-n test.yaml *.o
