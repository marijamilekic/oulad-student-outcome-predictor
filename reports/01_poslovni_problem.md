# 1. Razumevanje poslovnog problema i priprema podataka

## 1.1 Kontekst

Cilj rada je predikcija da li će student uspešno završiti online kurs, na osnovu OULAD (Open University Learning Analytics Dataset) skupa podataka.
Skup sadrži 32.593 upisa studenata na 22 različita kursa.

## 1.2 Definicija ciljne promenljive

Izvorna kolona `final_result` ima četiri moguće vrednosti: Pass (37,9%), Withdrawn (31,2%), Fail (21,6%) i Distinction (9,3%). Za potrebe rada usvojena je binarna definicija:
at_risk = 1 ako je final_result ∈ {Fail, Withdrawn}
at_risk = 0 ako je final_result ∈ {Pass, Distinction}


Fail i Withdrawn su spojeni jer sko;la ima isti interes da identifikuje oba tipa studenata na vreme, bez obzira da li je krajnji ishod pad na ispitu ili odustajanje pre kraja kursa. 
Nakon binarizacije, klase su gotovo balansirane (52,8% naspram 47,2%).

## 1.3 Horizont predikcije i sprečavanje curenja podataka

Baseline model predviđa rizik **pre početka kursa** (dan 0), koristeći isključivo podatke koji su u tom trenutku već poznati: demografiju studenta, podatke o upisu (`studentInfo`), trajanje kursa (`courses`) i datum registracije (`studentRegistration`), pod uslovom da je registracija izvršena pre ili na dan početka kursa.

Tabele `studentVle` (klikovi na sadržaj) i `studentAssessment` (rezultati zadataka) su namerno isključene iz baseline modela, jer se te aktivnosti dešavaju tokom kursa i njihovo korišćenje bi predstavljalo curenje podataka iz budućnosti (*data leakage*), odnosno model bi u treningu "video" informacije koje u trenutku stvarne predikcije još ne bi postojale.

Iz istog razloga, kolona `date_registration` je cenzurisana za 234 upisa (0,7%) kod kojih je registracija izvršena posle početka kursa. Ta vrednost je zamenjena nedostajućom, umesto da model dobije podatak koji u trenutku predikcije ne bi bio dostupan.

## 1.4 Implementacija

Priprema podataka je implementirana u `src/oulad_pipe/data/baseline.py` (funkcija `build_baseline_dataset`).

## 1.5 Baseline model

Kao referentna tačka treniran je model logističke regresije (`src/oulad_pipe/models/train_baseline.py`) nad demografskim i upisnim atributima. Model postiže ROC-AUC 0,677, u odnosu na 0,500 za trivijalni model koji uvek predviđa najčešću klasu što potvrđuje da demografski podaci nose koristan, iako ograničen, signal za predikciju rizika.

## 1.6 Serviranje modela

Trenirani model je učinjen dostupnim kroz FastAPI servis (`api/main.py`, endpoint `/predict`) i jednostavan Streamlit korisnički interfejs (`app/streamlit_app.py`) koji šalje zahteve ka tom servisu.




## Literatura 
https://pydantic.dev/docs/validation/2.11/api/pydantic/base_model/
https://docs.streamlit.io/