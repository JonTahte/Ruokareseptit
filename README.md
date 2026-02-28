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