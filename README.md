# openmensa.org canteen parser for Studentenwerk Thüringen

    $ easy_install requests, bs4
    $ git clone git://github.com/posativ/om-parser-jena.git

## Usage

    $ python thueringen.py Erns [Carl ...[Phil ]]  # or more clever
    $ make clean && make


It is sufficient to provide only the first characters of the original name.
For a complete list of available canteens, type some random characters and it
will show the names.
