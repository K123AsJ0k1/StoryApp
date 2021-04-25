# StoryApp

Pääset sovelluksen heroku versioon tästä linkistä https://st0ryapp.herokuapp.com/

# Sovellusmäärittelly:

Sovelluksen avulla voi tarkastella, jakaa ja kommentoida tarinoita.Sovelluksessa on olemassa kolme käyttäjää, jotka ovat anonyymit, kirjoittajat ja adminit.

Sovelluksen ominaisuudet ovat:

- Anonyymit, kirjoittajat ja adminit voi hakea ja lukea eri tarina postauksia 
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden kirjoittaja tunnuksen
- Kirjoittajat voivat luoda ja poistaa tarina postauksia
- Kirjoittajat voivat luoda ja poistaa tarina postaukseen uusia lukuja
- Kirjoittaja voi lisätä mahdollisuuden kommentoida lukua
- Kirjoittajat voivat kommentoida tarina postausten tiettyjä lukuja 
- Kirjoittajat voivat kommentoida tekstin tiettyä riviä
- Kirjoittajat voivat lisätä lukuihin kyselyitä
- Kirjoittajat voivat vastata lukujen lopussa oleviin kyselyihin
- Anonyymit ja kirjoittajat pystyvät näkemään postauksen kommentit
- Postauksen omistavat kirjoittajat pystyvät näkemään yksityisesti luvun kyselyt
- Postauksen omistava kirjoittaja pystyy poistamaan joko muutaman tai kaikki kommentit
- Postauksen omistava kirjoittaja pystyy poistamaan muutaman tai kaikki kyselyt
- Admin käyttäjä pystyy tarkastelemaan olemassa olevia käyttäjiä, kommenteja ja kyselyitä
- Admin käyttäjä pystyy poistamaan käyttäjiä, postauksia, kommenteja ja kyselyitä

# HUOMIOTA (25.4.2021):

Perustiedot:

- Jos haluat testata admin luontia, muuta tavallisen käyttäjän luonnin url user adminiksi. Super user password on Salasana
- Jos haluat testata admin kirjautumista , muuta tavallisen käyttäjän kirjautuminen url user adminiksi
- Sovelluksessa on olemassa jo kaksi tavallista käyttäjää, jotka ovat salainen/salainen ja salainen1/salainen1 (käyttäjä nimi/salasana)
- Sovelluksella on olemassa admin käyttäjä testaus_admin/testaus_admin (käyttäjä nimi/salasana)
- Kaikki asiat, joissa lukee WIP, on kehityksen alla
- Julkinen postaus tulee näkyviin silloin, kun se omistaa vähintään yhden chapterin

Ongelmia:

- Tietokanta ja route.py tarvitsevat hieman refaktorointia
- Muut käyttäjät ja adminit pystyvät luomaan, näkemään ja poistamaan luvatta muiden käyttäjien nimillä tietokantaan
- Sovelluksessa on edelleen CSRF haavoittuvuus, joka tullaan korjaamaan
- Sovelluksen käyttöliittymä on tietyissä paikoissa hieman tynkä
- Sovellus ei kommunikoi kovinkaan paljon käyttäjän tekemistä virheistä
- Sovellus ei varmista poistamista, joten käyttäjä voi vahingossa painaa väärää linkkiä ja poistaa asian
- Adminit pystyvät menemään pääsivulle ja profiilin
- Tietokannan poisto metodit kaipaavat hieman refaktorointia
- Super user password tarvitsee tietokanta varmistuksen

# Toteutetut ominaisuudet välipalautus 3 (25.4.2021):

- Anonyymit ja kirjoittajat näkevät postauksia pääsivulla
- Anonyymit ja kirjoittajat voivat tarkastella postauksien chaptereita
- Anonyymit ja kirjoittajat voivat tarkastella postausten kommentteja
- Kirjoittajat pystyvät vastamaan chapteriin liitettyihin kyselyihin
- Käyttäjä voi luoda uuden kirjoittaja tunnukset
- Käyttäjä pystyy kirjautumaan sisään ja ulos
- Kirjoittaja voi luoda ja poistaa postauksia
- Kirjoittaja voi luoda ja poista lukuja postauksista
- Kirjoittaja voi luoda ja poistaa kyselyitä
- Kirjoittaja voi luoda ja poistaa kyselyn vastauksia
- Kirjoittaja voi luoda kommentteja ja poistaa omasta postauksesta kommentteja
- Kirjoittaja pystyy valitsemaan, onko postaus julkinen vai yksityinen
- Kirjoittaja pystyy valitsemaan, onko chapterilla kysely vai ei
- Kirjoittaja pystyy valitsemaan, pystyykö postausta kommentoimaan
- Postauksen omistava kirjoittaja näkee ainoastaan kyselyn vastaukset

Uudet ominaisuudet:

- Chaptereista voidaan valita tekstiä rivi aiheeksi 
- Chapterien rivi aiheet näkyvät ja niitä voi kommentoida
- Chapterin rivi aiheita ja niihin liittyviä kommenteja voi poistaa
- Admin käyttäjän voi luoda ja sen avulla voi kirjautua
- Hallinto sivusto antaa linkit eri tietokanta näkymiin
- Sovellus pakottaa kirjoittajan rivittämän tekstin oikealla lailla (Rivi saa olla korkeintaan 100 merkkiä pitkä ilman enteriä)
- Sovellus osaa näyttää tekstiä oikealla lailla 

# Testauksesta herokussa (25.4.2021):

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

Reset

- Kun saavut joko postauksen, chapterin luontiin, vasemmalla puolella pitäisi olla reset, jonka avulla pystyt palamaan takaisin edelliseen valintan
- Sama linkki pitäisi löytyä muistakin sivuista

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
