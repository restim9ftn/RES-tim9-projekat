"# RES-tim9-projekat" 

    ZADATAK:

Potrebno je napraviti dizajn sistema,arhitekturu sistema, implementiratii istestirati rešenjekoji simulira rad i komunikaciju Asset Management sistema.
AMS vodi računa o svim uređajima u sistemu kao što su na primer: prekidači, transformatori, osigurači, ventili,
generatori  i  tako  dalje  i  osigurava  njihov stabilan rad prateći broj izvršenih operacija i broj radnih  sati.
Osnovni  cilj  ovog  sistema  je  pravilno održavanje opreme.
Sistem sadrži 3komponente:1.Lokalni uređaj2.Lokalni kontroler3.Asset Mangemet Sistem(AMS)

LOKALNI UREDJAJ:

Lokalni uređaj je jedno mernomesto u elektroenergetskom sistemu.
Lokalni uređaj može da menja stanje na dva načina:
       •Digitalno (ON/OFF, OPEN/CLOSE...)–prekidači, osigurači, ventili itd.
       •Analogno (setpoint)–generatori, baterije itd.
Lokalni uređaj svaku promenu šalje lokalnom kontroleru ili direktno AMS, u zavisnosti od podešavanja lokalnog uređaja:
       •Local device code–jedinstveno ime uređaja implementirano kao hash code
       •Timestamp (UNIX timestamp format)
       •Actual value (trenutna vrednost, open, close, on, off, analog measurement)


Aplikacija Lokalnog uređaja je zasebna konzolna aplikacija.
Lokalni uređaj se pali ručnoiz aplikacijei može biti ugašen u svakom momentu, kako planski iz aplikacije tako i neplanski gašenjem same aplikacije (time se simulira otkaz opreme).
Dodavanje novog Lokalnoguređaja se radi po principu plug-and-play, što znači da kada se novi Lokalni uređajupali(upali se nova instanca konzolne aplikacije),
počinje slanje svojih podataka i mora biti prihvaćeno od strane Lokalnog kontrolera ili AMSosim u slučaju ako to ime već postoji u   sistemu.
Slanje podataka je  periodično  a  broj  sekundi  trajanja  ciklusa  definiše  se  u  XML kongfiguracionom fajlu. 

LOKALNI KONTROLER:

Lokalni  kontroler čuva sva promene koje dolaze  od  strane  svih lokalnih uređaja prijavljenih na kontroleri  na  svakih  5  minuta(vreme  je  konfigurabilnou  XML  fajlu)ih prosleđuje AMS-u.
U slučaju uspešnog slanja Lokalni  kontrolerbriše svoju bafer bazu(XML), a u slučaju neuspešnog čuva bafer do uspešnog slanja. 
Ako se aplikacija nasilno ugasi pre slanja bafera, prilikom inicijalizacije učitaće se vrednosti iz fajla.
Lokalni kontroler može biti upaljen u svakom momentu, ali može biti i ugašen isto kao i lokalni uređaj. 
Aplikacija LK-a je zasebna konzolna aplikacija koja svojubazučuva u XML fajlu.
Dodavanje novog LK-ase radi po istom principu kao i dodavanje uređaja.
U sistemu može postajati više LK aplikacija. 


AMS:

AMS čuva sve promene u sistemu u svojoj bazi koja je jedinstvena za ceo sistem i služi za pravljenje izveštaja:
•Detalji promena za izabrani period za izabrani lokalni uređaj(sve promene + sumarno)
•Broj radnih sati za izabrani uredjaj za izabrani vremenski period(od –do kalendarski po satima)
•Izlistavanje svih uredjaja čiji je broj radnih sati preko konfigurisane vrednosti(alarmirati i obojiti u crvenu boju one uređaje za koje je broj radnih sati veći od granice definisane u opcijama aplikacije)
•Listanje svih postojećih uređaja u sistemu

AMS aplikacija je zasebna aplikacija koja ima svoj UI(moze biti i terminal)i svojepodatke čuva u SQL bazi. 
Kada se napravi novi lokalni uređaj, u konfiguraciji se bira kom Lokalnom kontroleru ili AMSpripada, pa stoga mora da se izlista spisak svih LK ikonkretnog sistemaprilikom kreiranja uređaja. 
Napomena:Vreme u sistemu treba da se vodi zasebno od realnog vremena i treba imati mogućnost da bude ubrzano.
U konfiguracionom XML fajlu koji je zajednički za sve aplikacije se podešava odnos koliko je sekundi u aplikaciji jedna realna sekunda.
Na primer, može se podesiti kako je jedna stvarna sekunda, Xsekundi u aplikaciji.
Time se postiže mogučnost da se za 10 ili 20 minuta rada aplikacije simulira ceo dan rada sistema. 
 