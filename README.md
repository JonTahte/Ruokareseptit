# Ruokareseptit
## Sovelluksen toiminnot
- Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
- Käyttäjä näkee sovellukseen lisätyt reseptit.
- Käyttäjä pystyy etsimään reseptejä hakusanalla.
- Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
- Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen).
- Käyttäjä pystyy antamaan reseptille arvostelun (kommentti ja arvosana). Reseptistä näytetään arvostelut ja keskimääräinen arvosana.

## Sovelluksen toiminta suurella tietomäärällä

Sovelluksen testaamiseen käytetty data:

```python
user_count = 1000
recipe_count = 10**6
review_count = 10**7
```

Testidataan voi tarkemmin tutustua tiedostossa `seed.py`.
Testeissä ladataan etusivun reseptiluetelman viisi ensimmäistä sivua. Käydään nyt läpi saatuja tuloksia.

Jos tietokannan indeksit eivät ole käytössä:

```
elapsed time: 1.96 s
127.0.0.1 - - [01/Mar/2026 17:21:13] "GET / HTTP/1.1" 200 -
elapsed time: 1.68 s
127.0.0.1 - - [01/Mar/2026 17:21:18] "GET /2 HTTP/1.1" 200 -
elapsed time: 1.69 s
127.0.0.1 - - [01/Mar/2026 17:21:22] "GET /3 HTTP/1.1" 200 -
elapsed time: 1.88 s
127.0.0.1 - - [01/Mar/2026 17:21:25] "GET /4 HTTP/1.1" 200 -
elapsed time: 1.78 s
127.0.0.1 - - [01/Mar/2026 17:21:30] "GET /5 HTTP/1.1" 200 -
```

Sivun lataaminen ilman indeksejä vie keskimäärin 1.8 s.

Jos tietokannan indeksit ovat käytössä:

```
elapsed time: 0.05 s
127.0.0.1 - - [01/Mar/2026 17:25:38] "GET / HTTP/1.1" 200 -
elapsed time: 0.03 s
127.0.0.1 - - [01/Mar/2026 17:25:41] "GET /2 HTTP/1.1" 200 -
elapsed time: 0.02 s
127.0.0.1 - - [01/Mar/2026 17:25:42] "GET /3 HTTP/1.1" 200 -
elapsed time: 0.03 s
127.0.0.1 - - [01/Mar/2026 17:25:43] "GET /4 HTTP/1.1" 200 -
elapsed time: 0.03 s
127.0.0.1 - - [01/Mar/2026 17:25:45] "GET /5 HTTP/1.1" 200 -
```

Sivun lataaminen indeksien kanssa vie keskimäärin 0.03 s eli sivupyynnöt ovat salamannopeita.

## Sovelluksen asennus

Kloonaa repositorio omalle koneellesi:

```
$ git clone git@github.com:JonTahte/Ruokareseptit.git
```

Siirry hakemistoon:

```
$ cd Ruokareseptit
```

Luo virtuaaliympäristö:

```
$ python3 -m venv venv
```

Aktivoi virtuaaliympäristö:

```
$ python3 -m venv venv
```

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alustustiedot:

```
$ sqlite3 database.db < schema.sql
```
```
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus:

```
$ flask run
```
