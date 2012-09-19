all: jena weimar erfurt gera ilmenau

jena:
	mkdir -p jena/
	python thueringen.py Erns > jena/mensa-ernst-abbe-platz.xml
	python thueringen.py Phil > jena/mensa-philosophenweg.xml
	python thueringen.py Carl > jena/mensa-carl-zeiss-promenade.xml

weimar:
	mkdir -p weimar/
	python thueringen.py Mens > weimar/mensa-am-park.xml

erfurt:
	mkdir -p erfurt/
	python thueringen.py Nord > erfurt/mensa-nordhaeuser-strasse.xml
	python thueringen.py Alto > erfurt/mensa-altonaer-strasse.xml

gera:
	mkdir -p gera/
	python thueringen.py Stud > gera/mensa-berufsakademie-gera.xml

ilmenau:
	mkdir -p ilmenau/
	python thueringen.py Ehre > ilmenau/mensa-ehrenberg
	python thueringen.py NANO > ilmenau/cafeteria-nanoteria

clean:
	rm -rf jena/ weimar/ erfurt/ gera/ ilmenau/
