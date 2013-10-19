PROJECT=project_to_test
RESULTS=results
GEN=generated

all: $(RESULTS)/test-result.xml

$(RESULTS)/test-result.xml: $(RESULTS)/test.yaml proctrace.py
	python proctrace.py $< > $@
$(RESULTS)/test.yaml: $(GEN)/main-n
	./$< 2> $@
$(GEN)/main-n: $(GEN)/main-n.c $(GEN)/b.c
	gcc $^ -o $@ -I $(PROJECT)
$(GEN)/main-n.c: $(PROJECT)/main.c mainproc.py
	python mainproc.py $< > $@
$(GEN)/b.c: $(PROJECT)/a.c $(PROJECT)/a.h c-to-c.py
	python c-to-c.py $< > $@
clean:
	rm -f $(GEN)/* *.o *.pyc $(RESULTS)/*
