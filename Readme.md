Az implementálás során Python 2.7-t, valamint Django-t és DjangoRestFramework-t használtam,

Az adatokat eredetileg Sqlite3 adatbázisban akartam tárolni, de mivel az nem rendelkezik STDDEV függvénnyel, így végülis PostgreSQL adatbázist használ a program. (/dmlab/settings.py <- itt kell megadni az adatbázis adatait)

A szervert a "python manage.py runserver" paranccsal lehet elindítani. Tetszõleges ip és port megadható a parancs végén. Django alapértelmezetten a localhostot és a 8000-es portot használja.

-----------------------------------------------------------------------------------------------------------------------

A server a POST és GET requesteket a http:/127.0.0.1:8000/log címen várja.

Adatokat POST request-tel lehet küldeni az adatbázisba. Amennyiben nem megfelelõ a beküldött adatok struktúrája vagy típusa, 400-as hibaüzenetet ad vissza a rendszer.

-----------------------------------------------------------------------------------------------------------------------

GET request paraméterei:

t1, t2 - kötelezõ idõintervallum paraméterek

method - kötelezõ paraméter. Értékkészlet: Min, Max, Avg, StdDev, MvgAvg

dim1, dim2 - tetszõleges paraméterek

n - MvgAvg methodhoz kötelezõ paramétere. Ezzel lehet megadni, hogy a t2 idõponttól hány másodpercre visszamenõ adatok átlagát számítsa. Úgy gondoltam életszerûbb ez a megközelítés, mint hogy az utolsó n elem átlagát számítsuk mozgóátlagnak.

-----------------------------------------------------------------------------------------------------------------------

Az aggregáláshoz a Django beépített aggregáló függvényeit használtam, amik adatbázis szinten hajtják végre a lekérdezéseket.

A Django beépített StdDev függvénye alapértelmezetten a PostgreSQL STDDEV_POP függvényét hívja meg azonban ez nem a hétköznapi értelemben vett szórást adja vissza. StdDev sample paraméterét TRUE-ra állítva az STDDEV_SAMP kerül meghívásra, ami már jó értéket számol, azonban 1 elemû halmazra nem ad vissza értéket. Ezt külön lekezeltem.

-----------------------------------------------------------------------------------------------------------------------

Példa lekérdezések:

127.0.0.1:8000/log/?t1=1&t2=10&method=Max

127.0.0.1:8000/log/?t1=1&t2=10&method=Min&dim1=1

127.0.0.1:8000/log/?t1=1&t2=10&method=Avg&dim2=1

127.0.0.1:8000/log/?t1=1&t2=10&method=StdDev&dim1=1&dim2=4

127.0.0.1:8000/log/?t1=1&t2=10&method=MvgAvg&n=400

-----------------------------------------------------------------------------------------------------------------------


