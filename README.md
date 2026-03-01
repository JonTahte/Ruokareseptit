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
elapsed time: 25.08 s
127.0.0.1 - - [01/Mar/2026 18:45:07] "GET / HTTP/1.1" 200 -
elapsed time: 22.27 s
127.0.0.1 - - [01/Mar/2026 18:45:37] "GET /2 HTTP/1.1" 200 -
elapsed time: 18.92 s
127.0.0.1 - - [01/Mar/2026 18:45:58] "GET /3 HTTP/1.1" 200 -
elapsed time: 22.85 s
127.0.0.1 - - [01/Mar/2026 18:46:25] "GET /4 HTTP/1.1" 200 -
elapsed time: 12.81 s
127.0.0.1 - - [01/Mar/2026 18:46:45] "GET /5 HTTP/1.1" 200 -
```

Sivun lataaminen ilman indeksejä vie keskimäärin yli 20 s.

Jos tietokannan indeksit ovat käytössä:

```
elapsed time: 0.17 s
127.0.0.1 - - [01/Mar/2026 18:48:04] "GET / HTTP/1.1" 200 -
elapsed time: 0.11 s
127.0.0.1 - - [01/Mar/2026 18:48:07] "GET /2 HTTP/1.1" 200 -
elapsed time: 0.12 s
127.0.0.1 - - [01/Mar/2026 18:48:09] "GET /3 HTTP/1.1" 200 -
elapsed time: 0.11 s
127.0.0.1 - - [01/Mar/2026 18:48:10] "GET /4 HTTP/1.1" 200 -
elapsed time: 0.11 s
127.0.0.1 - - [01/Mar/2026 18:48:11] "GET /5 HTTP/1.1" 200 -
```

Sivun lataaminen indeksien kanssa vie keskimäärin päälle 0.11 s.

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
