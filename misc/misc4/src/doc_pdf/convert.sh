for i in *.pdf; do pdftotext $i - | fold -w 30 > $i.txt; done
