#!/bin/bash

pdflatex life_safety.tex
bibtex life_safety.aux
pdflatex life_safety.tex
pdflatex life_safety.tex
pdflatex life_safety.tex