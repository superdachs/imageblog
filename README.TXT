Django Project für einen Photobezogenen Blog

zum testen kann man virtualenv benutzen.
unter arch linux geht das wie folgt:

als root:
pacman -S python2-virtualenv python-virtualenv libjpeg-dev

dies installiert virtualenv für python 2 und 3, wir werden hier python2 benutzen

UPDATE: python3 geht und sollte verwendet werden
bei problemen mit dem ssl zertifikat (nach dist update) neu starten

als user:
virtualenv2 ~/.django-virtenv-python2
. ~/django-virtenv-python2/bin/activate
pip -r requirements.txt


jetzt kann man das djangoprojekt wie gehabt nutzen (vorher natürlich das virtenv sourcen)
