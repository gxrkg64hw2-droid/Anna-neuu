MAIN = main

.PHONY: pdf watch clean

pdf:
	latexmk -lualatex $(MAIN).tex

watch:
	latexmk -lualatex -pvc $(MAIN).tex

clean:
	latexmk -C
	rm -f $(MAIN).bbl $(MAIN).bcf $(MAIN).run.xml
