# Python Reversi
---

[Stiahnuť hru](https://github.com/dedinside1337/dedinside1337.github.io/raw/main/reversi/reversi.zip)

---

## Pravidlá
* Základná verzia sa hrá na štvorcovej ploche 8x8 polí.
* Cieľom hry Reversi je mať na hracej ploche viac figúrok ako súper. Hra končí, ak sú všetky štvorce obsadené figúrkami alebo žiadny z hráčov nemôže urobiť ťah.
* Reversi sa hrá so zvláštnymi figúrkami, ktoré majú jednu stranu bielu a druhú čiernu. Ak je hráč na ťahu, umiestni figúrku na hraciu plochu tak, aby ležala jeho farbou hore. Figúrky nie je možné ukladať kdekoľvek - každým ťahom musíte zajať jednu alebo viac súperových figúrok, ktoré sú potom otočené opačnou farbou hore a stávajú sa figúrkami hráča. Pokiaľ hráč nemôže v danej pozícii zajať žiadnu súperovu figúrku, musí prenechať ťah súperovi.
* Hráč musí umiestniť figúrku tak, aby obkľúčil svojimi dvoma figúrkami súvislý rad súperových kameňov, a to v ľubovoľnom smere (vodorovne, zvisle alebo uhlopriečne). 

---

## Režimy hry
* __Hráč proti hráčovi__
* __Hráč proti umelej inteligencii__
### Umelá inteligencia
    Každému štvorcu je priradená hodnota. Umelá inteligencia tieto hodnoty porovná a nájde najlepší možný ťah.

---

## Ovládanie
Ťahy v hre je možné vykonávať kliknutím ľavým tlačidlom myši. Ak nie sú možné žiadne ťahy, môžete ich preskočiť pomocou modrého tlačidla SKIP.
  
---

## Koniec hry
* Na konci hry sa spustí animácia ohňostroja.
* Výsledky hry sa ukladajú do súboru result.txt, výsledky poslednej hry sa vypisujú do obdĺžnikovej oblasti vpravo.
