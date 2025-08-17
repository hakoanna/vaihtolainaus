# Vaihtokaupat (ja ehkä myös lainakaupat)

Sovellus, jossa voi sopia laina- ja vaihtokauppoja.

- Käyttäjät pystyvät luomaan tunnuksen, kirjautumaan sisään ja kirjautumaan ulos.
- Käyttäjät pystyvät sisäänkirjautuneina lisäämään sovellukseen vaihtokauppaehdotuksia, skeä muokkaamaan ja poistamaan omia ehdotuksiaan.
- Käyttäjät näkevät omansa ja muiden lisäämät ehdotukset.
- Kuka tahansa pystyy etsimään kenen tahansa ehdotuksia hakusanalla.
- Jokaisella käyttäjällä on käyttäjäsivu, jolla näkyy, montako ehdotusta hän on tehnyt ja löytyy niihin linkit.
- Ehdotuksille voi valita luokitteluja, tällä hetkellä vaihdettavan tavara tyypistä ja kunnosta. Luokat ovat tietokannassa, ja niitä voi myös muokata.
- Käyttäjä pystyy sisäänkirjautuneena vastaamaan ehdotuksiin. Nämä vastaukset näkyvät kaikille.

Suunnitelmissa:
- Parantaa luokitteluja, esim. että onko vaihtoehdotuksessa oma vaihdettava tavara kyseessä vai tavara, jota käyttäjä etsii.
- Ehkä myös jotain vapaaehtoisia kriteerejä sille, että jos ehdotuksessa kaupittelee omaa tavaraa, niin minkä/minkälaisen asian kanssa sen haluaisi vaihtaa.
- Ehkä mahdollisuus ehdotuksen tehneelle käyttäjälle merkata ehdotuksen statuksen olevan "auki" tai "kiinni" sen perusteella, onko vaihtokaupat jo solmittu. Jos kiinni, enempää vastauksia ei voi lähettää.
- Lisää infoa käyttäjäsivuille?
- Kunhan aika ei lopu kesken, niin lisätä ja rekonfiguroida lainaamiset mukaan. Jos aikaa ei riitä molempien tekemiseen, niin tästä tulee pelkkä vaihtokauppasovellus.

---------------------------------------------------------------------------------------------
How to test program:

1. download files
2. in terminal: cd (your folder location)
3. in terminal: python3 -m venv venv
4. in terminal: source venv/bin/activate
5. in terminal: pip install flask (if you don't already have it installed)
6. in terminal: sqlite3 database.db
7. paste schema.sql from github to terminal
8. in terminal:.quit
9. in terminal: flask run
10. open the program on a browser with the provided address
