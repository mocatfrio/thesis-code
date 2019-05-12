#!/bin/bash
xelatex -synctex=1 -interaction=nonstopmode --shell-escape buku.tex || exit 1
okular buku.pdf
