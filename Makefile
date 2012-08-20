all: jena weimar erfurt gera ilmenau

jena:
	mkdir -p jena/
	python jena.py Erns > jena/mensa-ernst-abbe-platz.xml
	python jena.py Phil > jena/mensa-philosophenweg.xml
	python jena.py Carl > jena/mensa-carl-zeiss-promenade.xml

weimar:
	mkdir -p weimar/
	python jena.py Mens > weimar/mensa-am-park.xml

erfurt:
	mkdir -p erfurt/
	python jena.py Nord > erfurt/mensa-nordhaeuser-strasse.xml
	python jena.py Alto > erfurt/mensa-altonaer-strasse.xml

gera:
	mkdir -p gera/
	python jena.py Stud > gera/mensa-berufsakademie-gera.xml

ilmenau:
	mkdir -p ilmenau/
	python jena.py Ehre > ilmenau/mensa-ehrenberg
	python jena.py NANO > ilmenau/cafeteria-nanoteria

clean:
	rm -rf jena/ weimar/ erfurt/ gera/ ilmenau/