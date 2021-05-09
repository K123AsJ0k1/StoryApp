# StoryApp

Pääset sovelluksen heroku versioon tästä linkistä https://st0ryapp.herokuapp.com/

# Sovellusmäärittelly (9.5.2021):

Sovelluksen avulla voi tarkastella, jakaa ja kommentoida tarinoita.Sovelluksessa on olemassa kolme käyttäjää, jotka ovat anonyymit, kirjoittajat ja adminit.

Sovelluksen ominaisuudet ovat:

Yleisesti:

- Jokainen voi lukea pääsivulla olevia postauksia, lukea chaptereita, tarkastaa yleiset kommentit ja tarkastella kirjoittajien profiileja

Kirjautuneiden käyttäjien toimet:

- Kirjoittajat voi luoda käyttäjän ja kirjautua sillä sisään (nimen on oltava uniikki ja vähintään 5 merkkiä, kun taas salasanan on oltava vähintään 8 merkkiä)
- Adminin voi luoda ja sen avulla voi kirjautua sovelluksen hallintoon (on muutettava tavallisen kirjautumisen url viimeiset sanat adminiksi ja nimen on oltava uniikki, nimen ja salasanan on oltava vähintään 10 merkkiä ja on tiedettävä oiketus koodi)
- Kirjoittajat voi luoda postauksia, muokata niitä ja poistaa niitä
- Adminit pystyvät poistamaan postauksia
- Kirjoittajat voi luoda postauksiin chaptereita, muokata niitä ja poistaa niitä
- Adminit pystyvät poistamaan chaptereita
- Postauksen voi laittaa julkiseksi ja kommentit voi laittaa piiloon
- Chapterin voi laittaa julkiseksi, sen rivi-aiheet ja kysely voi laittaa piiloon
- Postauksen kommentti voi olla joko viittaava tai ei
- Postauksen omistaja ja admin voi poistaa yleisiä kommentteja
- Kirjoittajat voivat luoda chapterista tekstistä voidaan luoda rivi aihe maalamalla tekstin ja painamalla luo rivi aihe
- Kirjoittajat voivat tarkastella chapterin rivi-aiheita ja vastata niihin
- Adminit pystyvät näkemään rivi aiheet
- Postauksen omistaja ja admin voi poistaa rivi aiheita ja niiden vastauksia
- Kirjoittajat voivat luoda kyselyita ja vastata niihin
- Admin voi poistaa kyselyn
- Postauksen omistaja ja admin pystyvät tarkastelemaan kyselyiden vastauksia ja poistamaan niitä
- Hallintoon kirjautunut admin pystyy tarkastelemaan sovelluksen tietokanta taulujen tietoja
- Hallinnon käyttäjä sivulla admin pystyy näkemään taulukon (id,käyttäjä,rooli), käyttäjien määrän, adminien määrän ja painamaan kirjoittajien linkkejä päästäkseen heidän profiileihin
- Hallinnon postaus sivulla admin psytyy näkemään taulukon (id,omistaja,julkisuus,kommentointi,nimi), postausten määrän, julkisten postausten määrän ja painamaan nimi linkkiä päästäkseen lukemaan postauksen chaptereita
- Hallinnon luvut sivulla admin pystyy näkemään taulukon (id,postaus,julkisuus,rivi kommentit, kyselyt,luku,rivit), lukujen määrän, julkisten lukujen määrän, suurimman luvun ja suurimman rivin
- Hallinnon kommentit sivulla admin pystyy näkemään taulukon (id,omistaja,postaus,rivi id, yleinen kommentti, rivi kommentti, numerointi ja luku), yleisten kommenttien määrään, rivi aiheiden määrään ja rivi vastausten määrän
- Hallinnon kyselyt sivulla admin pystyy näkemään taulukon (id,omistaja,postaus,luku) ja kyselyiden määrän
- Hallinnon vastaus sivulla admin pystyy näkemään taulukon (id,vastaaja,kysymys id, luku, postaus ) ja vastausten määrän
- Hallintoon kirjautunut admin pystyy tarkastamaan oikeutus koodin ja muuttamaan sen (uusi oikeutus koodi on oltava vähintään 20 merkkiä)
- Admin pystyy käyttäjä taulun tiedoista menemään kirjoittajan profiliin
- Admin pystyy post taulun tiedoista menemään postauksen ensimmäiseen chapteriin

# HUOMIOTA (9.5.2021):

Perustiedot:

- Adminille näytetty pääsivu on tie hallinto sivulle
- Jos haluat testata admin luontia, muuta tavallisen käyttäjän luonnin url user adminiksi.
- Nykyinen oikeutus koodi on testauksessa_kaytettava_clearance_code (Muutoksen testaamisen jälkeen, muuta koodi samaksi)
- Jos haluat testata admin kirjautumista , muuta tavallisen käyttäjän kirjautuminen url user adminiksi
- Sovelluksessa on olemassa jo kaksi tavallista käyttäjää, jotka ovat salainen/salainen ja salainen1/salainen1 (käyttäjä nimi/salasana)
- Sovelluksessa on olemassa jo kaksi adminia, jotka testaus_admin/testaus_admin ja testaus_admin2/testaus_admin2
- Julkinen postaus tulee näkyviin silloin, kun se omistaa vähintään yhden chapterin

Sovellukseen jääneitä ongelmia

- Liian aikainen refaktorointi ja epäonnistuminen sen aiheuttamien name errorien korjaamisessa ei mahdollistanut aikaa sovelluksen tietokanta koodin, routes moduulin, linkkien ja logic moduulien refaktoroimiseen, minkä takia kyseiset osa alueet eivät ole rakenteeltaan parhaita
- Sovelluksen logic moduulit saisivat toteuttaa paljon enemmän db luokissa käytetyistä toimista
- Poistaminen ei kysy varmistusta, minkä takia kirjoittaja tai admin voi vahingossa poistaa postauksen
- Nykyinen clearance_code järjestely vaatii admineilta valpautta valvoa uusien adminien ilmestymistä sovellukseen, sillä kyseinen koodi ei ole salattu tietokannassa, minkä seurauksesta tietokanta murtaja pystyisi luomaan adminin sovelluksessa 

# Testauksesta herokussa (9.5.2021):

Perusidea:

- Sovelluksen toimivuuden varmistaminen perustuu suurilta osin sen sisältämien eri sivujen toiminnallisuuden varmistamiseen,joka voidaan tehdä klikkamalla nähtyjä linkkejä, asetuksia ja antamalla eri tekstejä
- Suosittelen käyttämään alla olevia ehtoja testauksessa

Käyttäjän luonti:

- Jokainen käyttäjä nimi täytyy olla vähintään 5 merkkiä pitkä
- Jokainen käyttäjän salasana täytyy olla vähintään 8 merkkiä pitkä
- Käyttäjän nimi täytyy olla uniikki
- Tapauksessa, jossa nämä ehdot eivät toteudu, sivu päivittyy ja antaa ns error viestin
- Tapauksessa, jossa kaikki on hyvin, sivu näyttää pääsivun

Adminin luonti:

- Jokainen admin on oltava vähintään 10 merkkiä pitkä 
- Jokainen admin salasana on oltava vähintä 10 merkkiä pitkä
- Admin nimi täytyy olla uniikki
- Tapauksessa, jossa nämä ehdot eivät toteudu, sivu päivittyy ja antaa ns error viestin
- Tapauksessa, jossa kaikki on hyvin, sivu näyttää hallinto sivun

Kirjautuminen kirjoittajana:

- Käyttäjä nimi täytyy olla olemassa ja ei admin roolin omistava
- Käyttäjän salasana täytyy olla oikea
- Tapauksessa, jossa nämä ehdot eivät toteudu, sivu päivittyy ja antaa ns error viestin
- Tapauksessa, jossa kaikki on hyvin, sivu näyttää pääsivun

Kirjautuminen adminina:

- Käyttäjä nimi täytyy olla olemassa ja admin roolin omistava
- Käyttäjän salasana täytyy olla oikea
- Tapauksessa, jossa nämä ehdot eivät toteudu, sivu päivittyy ja antaa ns error viestin
- Tapauksessa, jossa kaikki on hyvin, sivu näyttää hallinto sivun

Ulos kirjautuminen

- Ulos kirjautumisen jälkeen selain pitäisi olla pääsivulla ja näyttää anonyymi nimikkeen

Profiili:

- Anonyymit, kirjoittajat ja adminit pitäisi pystyä näkemään postaukset, lukemaan niitä ja menemään niiden yleisiin kommentteihin
- Ainoastaan kirjoittajat omistavat profiilin
- Tapauksessa, jossa käyttäjällä ei ole postauksia, sivu pitäisi näyttää ei postauksia
- Tapauksessa, jossa käyttäjä on luonut postauksia, sivu pitäisi näyttää postauksia
- Ainoastaan omistajat pystyvät luomaan ja muokkamaan postauksia, mutta adminit pystyvät poistamaan postauksia

Postauksen luonti

- Antaa mahdollisuuden nimen, julkisuus, kommentointi, ikärajan ja genren asettamiseen
- Nimi ja genre ei saa olla tyhjä tai 50 merkkiä pitkä, jolloin sivu näyttää error viestin
- Valintojen jälkeen vie profiiliin

Postauksen muokkaus

- Sama näkymä ja toiminta kuin postauksen luonnissa

Postauksen poisto

- Postaukseen liitetyn poista linkin painaminen poistaa postauksen profiilistas
- Profiili näyttää varmistavan viestin nimen alla

Chapterin luonti

- Antaa mahdollisuuden postauksen valitsemiseen, julkisuuden, rivi aiheiden, kyselyiden ja sisällön antamiseen
- Sisältö ei saa olla tyhjä tai ilman välilyöntiä yli 100 merkkiä, jonka sivu näyttää error viestin
- Valintojen jälkeen takaisin profiiliin

Chapterien tarkastelu

- Tänne pääsee joko pääsivun tai profiilin kautta
- Vasemmassa kulmassa on chapter liikkuminen ja rivi kommentointi
- Oikeassa kulmassa on poisto, muokkaus, kyselyt ja muita linkkejä
- Tapauksessa, jossa chapter on julkinen, näkyy teksti
- Tapauksessa, jossa chapter on rivi kommentoitava, näkyy rivikommentointi työkalut
- Tapauksessa, jsosa chapterissa on kysely, näkyy kysely työkaly

Kyselyiden lisäys

- Postauksen omistava käyttäjä voi lisätä kyselyn menemällä painamalla kysely linkkiä luku paikasta ja menemällä luo kysely paikkaan
- Sisältö ei saa olla tyhjä tai ilman välilyöntiä yli 100 merkkiä, jonka sivu näyttää error viestin
- Kysely luomisen jälkeen, se pitäisi ilmestyä kysely sivulle

Kyselyn poisto

- Omistaja ja admin voi poistaa kyselyn
- Kysely paikassa kyselyiden päällä on poisto linkki, jonka painamisen jälkeen kysely pitäisi hävitä

Kyselyyn vastaaminen

- Kirjoittajat voivat vastata kyselyyn menemällä kyselyyn ja painamalla vastaa linkkiä, jonka tallentamisen jälkeen käyttäjä palaa kyselyy sivulle
- Sisältö ei saa olla tyhjä tai ilman välilyöntiä yli 100 merkkiä, jonka sivu näyttää error viestin

Kyselyn vastauksien tarkastelu

- Postauksen omistava kirjoittaja ja admin pysty tarkastelemaan kyselyiden vastauksia kysely sivustosta ja kysymyksen vastaus paikasta

Kyselyn vastauksien poisto

- Postauksen omistava kirjoittaja ja admin pystyy poistamaan kysymykseen tulleita vastauksia poista linkin avulla

Postausten kommentien tarkastelu

- Anonyymit, kirjoittajat ja adminit pystyvät kommentoimaan postauksia joko pääsivun kautta tai profiilin kautta omia postauksia kommentti linkin avulla

Postausten kommentoiminen

- Kirjoittajat pystyvät kommentoimaan painamalla kommentti sivusta luo kommentti linkkiä ja kirjoittamalla tarvitut asiat
- Kommentoija pystyy tarkentamaan olemassa olevia lukuja, mutta tyhjän ja numeroista ulkopuolisen merkin tapauksissa tätä viittausta ei ole
- Sisältö ei saa olla tyhjä tai ilman välilyöntiä yli 100 merkkiä, jonka sivu näyttää error viestin
- Tallentamisen jälkeen kommentti pitäisi näkyä itse kommentti ja kommentoija vittauksilla

Postauksen kommenttien poisto

- Postauksen omistava kommentoija ja admin pystyy poistamaan kommentteja menemällä sen kommentti paikaan ja painamalla poista linkkiä
- Painalluksen jälkeen kommenttia ei pitäisi näkyä

Postauksen näkeminen

- Postaus ei pitäisi näkyä pääsivulla, jos se ei ole julkinen tai jos sillä ei ole yhtään chapteria

Postauksen kommentointi mahdollisuus

- Pääsivulla ja profiilissa pitäisi näkyä mahdollisuus kommentoida, jos se on mahdollistettu

Rivi aiheen valitseminen

- Valittuasi jonkin tekstin chapterin näkymästä (sama periaate kuten copy paste), paina luo rivi aihe, jonka jälkeen se pitäisi näkyä chapterin rivialueella
- Tapauksessa, jossa tämä ei tapahdu, tulee error viesti

Rivi alue

- Rivialueella näkyvät kaikki rivi aiheet, joita voi kommentoida käyttäjät ja joita omistaja ja admin pystyy poistamaan

Rivi kommentit

- Riviaihetta voi kommentoida menemällä sen vastauksiin ja luomalla kommentin, jonka jälkeen se pitäisi näkyä rivi aiheen vastauksissa.Luvun omistaja pystyy poistamana rivi kommentteja

Hallinto

- Antaa linkit eri tietokanta tauluihin ja oikeutus koodin vaihtoon

Tietokanta taulut

- Näyttävät tällä hetkellä linkin mukaisen taulukon tiedot tietokannassa, takaisin paluu linkin ja ulos kirjautumisen
- Käyttäjä ja postaus taulujen tapauksessa admin pystyy siirtymään joko valitun käyttäjän profiiliin tai postauksen ensimmäisen chapteriin

Oikeutus koodin vaihto

- Sivu näyttää nykyisen oikeutus koodin
- Voidaan vaihtaa, jos annettu koodi on vähintään 20 merkkiä
- Tapauksessa, jossa annettu koodi ei ole vähintään 20 merkkiä, näkyy ns error viesti
- Vaihdon onnistuessa, sivu varmista vaihdon tapahtumisen
