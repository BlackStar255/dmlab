Az implement�l�s sor�n Python 2.7-t, valamint Django-t �s DjangoRestFramework-t haszn�ltam,

Az adatokat eredetileg Sqlite3 adatb�zisban akartam t�rolni, de mivel az nem rendelkezik STDDEV f�ggv�nnyel, �gy v�g�lis PostgreSQL adatb�zist haszn�l a program. (/dmlab/settings.py <- itt kell megadni az adatb�zis adatait)

A szervert a "python manage.py runserver" paranccsal lehet elind�tani. Tetsz�leges ip �s port megadhat� a parancs v�g�n. Django alap�rtelmezetten a localhostot �s a 8000-es portot haszn�lja.

-----------------------------------------------------------------------------------------------------------------------

A server a POST �s GET requesteket a http:/127.0.0.1:8000/log c�men v�rja.

Adatokat POST request-tel lehet k�ldeni az adatb�zisba. Amennyiben nem megfelel� a bek�ld�tt adatok strukt�r�ja vagy t�pusa, 400-as hiba�zenetet ad vissza a rendszer.

-----------------------------------------------------------------------------------------------------------------------

GET request param�terei:

t1, t2 - k�telez� id�intervallum param�terek

method - k�telez� param�ter. �rt�kk�szlet: Min, Max, Avg, StdDev, MvgAvg

dim1, dim2 - tetsz�leges param�terek

n - MvgAvg methodhoz k�telez� param�tere. Ezzel lehet megadni, hogy a t2 id�pontt�l h�ny m�sodpercre visszamen� adatok �tlag�t sz�m�tsa. �gy gondoltam �letszer�bb ez a megk�zel�t�s, mint hogy az utols� n elem �tlag�t sz�m�tsuk mozg��tlagnak.

-----------------------------------------------------------------------------------------------------------------------

Az aggreg�l�shoz a Django be�p�tett aggreg�l� f�ggv�nyeit haszn�ltam, amik adatb�zis szinten hajtj�k v�gre a lek�rdez�seket.

A Django be�p�tett StdDev f�ggv�nye alap�rtelmezetten a PostgreSQL STDDEV_POP f�ggv�ny�t h�vja meg azonban ez nem a h�tk�znapi �rtelemben vett sz�r�st adja vissza. StdDev sample param�ter�t TRUE-ra �ll�tva az STDDEV_SAMP ker�l megh�v�sra, ami m�r j� �rt�ket sz�mol, azonban 1 elem� halmazra nem ad vissza �rt�ket. Ezt k�l�n lekezeltem.

-----------------------------------------------------------------------------------------------------------------------

P�lda lek�rdez�sek:

127.0.0.1:8000/log/?t1=1&t2=10&method=Max

127.0.0.1:8000/log/?t1=1&t2=10&method=Min&dim1=1

127.0.0.1:8000/log/?t1=1&t2=10&method=Avg&dim2=1

127.0.0.1:8000/log/?t1=1&t2=10&method=StdDev&dim1=1&dim2=4

127.0.0.1:8000/log/?t1=1&t2=10&method=MvgAvg&n=400

-----------------------------------------------------------------------------------------------------------------------


