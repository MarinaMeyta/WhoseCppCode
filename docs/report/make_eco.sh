#!/bin/bash

pdflatex economics.tex
bibtex economics.aux
pdflatex economics.tex
pdflatex economics.tex
pdflatex economics.tex