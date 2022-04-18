all: demo/words.txt

demo/words.txt: demo/liste.de.mots.francais.frgut.txt
	iconv -t ASCII//TRANSLIT $< | sort | uniq | sed 's/./& /g' > $@

demo/liste.de.mots.francais.frgut.txt:
	wget http://www.pallier.org/extra/liste.de.mots.francais.frgut.txt -O demo/liste.de.mots.francais.frgut.txt

clean:
	rm demo/words.txt
