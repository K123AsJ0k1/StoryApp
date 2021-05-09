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

- Jos haluat testata admin luontia, muuta tavallisen käyttäjän luonnin url user adminiksi.
- Nykyinen oikeutus koodi on testauksessa_kaytettava_clearance_code (Muutoksen testaamisen jälkeen, muuta koodi samaksi)
- Jos haluat testata admin kirjautumista , muuta tavallisen käyttäjän kirjautuminen url user adminiksi
- Sovelluksessa on olemassa jo kaksi tavallista käyttäjää, jotka ovat salainen/salainen ja salainen1/salainen1 (käyttäjä nimi/salasana)
- Sovelluksessa on olemassa jo kaksi adminia, jotka testaus_admin/testaus_admin ja testaus_admin2/testaus_admin2
- Julkinen postaus tulee näkyviin silloin, kun se omistaa vähintään yhden chapterin

Sovellukseen jääneitä ongelmia

- Liian aikainen refaktorointi ja epäonnistuminen sen aiheuttamien name errorien korjaamisessa ei mahdollistanut aikaa sovelluksen tietokanta koodin, routes moduulin ja linkkien refaktoroimiseen, minkä takia kyseiset osa alueet eivät ole rakenteeltaan parhaita
- Sovelluksen logic moduulit saisivat toteuttaa paljon enemmän db luokissa käytetyistä toimista
- Poistaminen ei kysy varmistusta, minkä takia kirjoittaja tai admin voi vahingossa poistaa postauksen

# Testauksesta herokussa (9.5.2021):

Perusidea:

- Sovelluksen toimivuuden varmistaminen perustuu suurilta osin sen sisältämien eri sivujen toiminnallisuuden varmistamiseen,joka voidaan tehdä klikkamalla nähtyjä linkkejä, asetuksia ja antmaalla eri tekstejä
- Suosittelen käyttämään alla olevia ehtoja apuna testauksessa

Käyttäjän luonti:

- Jokainen käyttäjä nimi täytyy olla vähintään 5 merkkiä pitkä
- Jokainen käyttäjän salasana täytyy olla vähintään 8 merkkiä pitkä
- Käyttäjän nimi täytyy olla uniikki
- Tapauksessa, jossa nämä ehdot eivät toteudu, sivu päivittyy ja antaa ns error viestin

Kirjautuminen:

- Käyttäjä nimi täytyy olla olemassa
- Käyttäjän salasana täytyy olla oikea
- Tapauksessa, jossa nämä ehdot eivät toteudu, sivu päivittyy ja antaa ns error viestin

Ulos kirjautuminen

- Ulos kirjautumisen jälkeen selain pitäisi olla pääsivulla ja näyttää anonyymi nimikkeen

Profiili:

- Tapauskessa, jossa käyttällä ei ole postauksia, sivu pitäisi näyttää ei postauksia
- Tapauksessa, jossa käyttäjä on luonut postauksia, niin se pitäisi näyttää kaikki postaukset, niiden asetuksiin, antaa linkin työpöytään, pääsivulle ja ulos kirjautumisen

Työpöytä

- Antaa kaksi neljä vaihtoehtoa, jotka ovat uuden postauksen luonti, uuden chapterin luonti, linkin pääsivulle ja ulos kirjautumisen
- Kyseiset linkit pitäisi tehdä nimiensä mukaisia asioita
- Tapauksessa, jossa postauksia ei ole, chapter luonti pitäisi näyttää, ettei postauksia ole

Takaisin

- Tämä linkki löytyy monesta sivusta ja se vie takaisin edelliseen sivuun

Postauksen luonti

- Annettavissa asetuksissa on eri vaihtoehtoja, jotka ovat nimen antaminen, julkisuus asetus, kommentti asetus ja WIP asetuksia, joista kaksi ensimmäistä on testattava
- Annettuasi tiedot, paina sivun pohjalla olevaa tietoa tallenna, jonka jälkeen sivu pitäisi päivittyä profiili sivulle ja siellä pitäisi näkyä postaus

Postauksen muokkaus

- Profiilissa paina muokka valintaa
- Vaihda jotain tietoja, joiden muutoksen pitäisi näkyä profiilissa

Postauksen poisto

- Profiilissa paina postauksessa poista linkkiä
- Painamisen jälkeen postaus pitäisi kadota profiilista

Chapterin luonti

- Annettavista asetuksissa on eri vaihtoehtoja, joista tarkastettavat ovat ei WIP nimeä sisältävät
- Tärkein vaihtoehto on se, että luonnissa näkyy käyttäjän luomat postaukset, hän pystyy valitsemaan niistä ja linkkaus toimii oikealla tavalla
- Tallennuksen jälkeen, chapter pitäisi olla luettavissa postauksen lue napin avulla

Chapterien tarkastelu

- Tapauksessa, jossa on enemmän kuin 2 chapteria, pitäisi vasemmassa kulmassa luku sivustossa olla seuraava ja edellinen
- Seuraava vie seuraavaan chapteriin ja edellinen edelliseen chapteriin

Kyselyiden lisäys

- Postauksen omistava käyttäjä voi lisätä kyselyn menemällä painamalla kysely linkkiä luku paikasta ja menemällä luo kysely paikkaan
- Kysely luomisen jälkeen, se pitäisi ilmestyä kysely sivulle

Kyselyn poisto

- Kysely paikassa kyselyiden päällä on poisto linkki, jonka painamisen jälkeen kysely pitäisi hävitä

Kyselyyn vastaaminen

- Kirjoittajat voivat vastata kyselyyn menemällä kyselyyn ja painamalla vastaa linkkiä, jonka tallentamisen jälkeen käyttäjä palaa kyselyy sivulle

Kyselyn vastauksien tarkastelu

- Postauksen omistava kirjoittaja pysty tarkastelemaan kyselyiden vastauksia kysely sivustosta ja kysymyksen vastaus paikasta

Kyselyn vastauksien poisto

- Postauksen omistava kirjoittaja pystyy poistamaan kysymykseen tulleita vastauksia poista linkin avulla

Postausten kommentien tarkastelu

- Kirjoittajat pystyvät kommentoimaan postauksia joko pääsivun kautta tai profiilin kautta omia postauksia kommentti linkin avulla

Postausten kommentoiminen

- Kirjotittajat pystyvät kommentoimaan painamalla kommentti sivusta luo kommentti linkkiä ja kirjoittamalla tarvitut asiat
- Kommentoija pystyy tarkentamaan olemassa olevia lukuja, mutta tyhjän ja numeroista ulkopuolisen merkin tapauksissa tätä viittausta ei ole
- Tallentamisen jälkeen kommentti pitäisi näkyä itse kommentti ja kommentoija vittauksilla

Postauksen kommenttien poisto

- Postauksen omistava kommentoija pystyy poistamaan kommentteja menemällä sen kommentti paikaan ja painamalla poista linkkiä
- Painalluksen jälkeen kommenttia ei pitäisi näkyä

Postauksen näkeminen

- Postaus ei pitäisi näkyä pääsivulla, jos se ei ole julkinen tai jos sillä ei ole yhtään chapteria

Postauksen kommentointi mahdollisuus

- Pääsivulla ja profiilissa pitäisi näkyä mahdollisuus kommentoida, jos se on mahdollistettu

Chapterin kyselyn näkymien

- Chapter viewissä pitäisi näkyä kysely, jos kyseinen asetus on annettu

Rivi aiheen valitseminen

- Valittuasi jonkin tekstin chapterin näkymästä (sama periaate kuten copy paste), paina luo rivi aihe, jonka jälkeen se pitäisi näkyä chapterin rivialueella

Rivi alue

- Rivialueella näkyvät kaikki rivi aiheet, joita voi kommentoida käyttäjät ja joita omistaja pystyy poistamaan

Rivi kommentit

- Riviaihetta voi kommentoida menemällä sen vastauksiin ja luomalla kommentin, jonka jälkeen se pitäisi näkyä rivi aiheen vastauksissa.Luvun omistaja pystyy poistamana rivi kommentteja

Adminin luonti

- Muutettuasi tavallisen käyttäjän luonnin URL:in user adminiksi, anna 10 merkin pituinen uniikki käyttäjä nimi ja salasana ja super user password salasana. Sen jälkeen kirjaudu sisään

Admin kirjautuminen

- Luotuasi uuden adminin tai muutettuasi kirjautumisen URL:n user adminiksi, annan olemassa oleva käyttäjä nimi ja salasana

Hallinto

- Antaa linkit eri tietokanta työkaluihin ja ulos kirjautumis mahdollisuuden

Tietokanta mäkymät

- Näyttävät tällä hetkellä linkin mukaisen taulukon tiedot tietokannassa, takaisin paluu linkin ja ulos kirjautumisen
