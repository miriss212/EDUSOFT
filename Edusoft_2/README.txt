PRAVIDLA A OVLADANIE

-   hracia plocha predstavuje 3D priestor (more)
-   sonar (slider vlavo dole) vykresluje hraciu plochu v 2D rozmere
    na zaklade nastavenej hlbky
    |-  cim mensie cislo tym vacsia hlbka (hlbka 0 predstavuje morske dno)
-   ciel hry je aby sa ponorka dostala k pokladu (zlata minca)
-   ponorkou pohybujeme na zaklade prikazov hraca (kapitan v ponorke)
    |-  zadame prikazy do postupnosti prikazov (hore nad sonarom)
        |-  klavesa "H" alebo "h" -> chod hlbsie
        |-  klavesa "P" alebo "p" -> chod plytsie
        |-  sipka hore -> chod dopredu
        |-  sipka dole -> chod dozadu
        |-  sipka vpravo -> chod doprava
        |-  sipka vlavo -> chod dolava
        |-  klavesa "backspace" -> vymaz
        |-  POZOR! ponorka ide danym smerom az kym nenarazi na koral alebo okraj mapy
    |-  zadane prikazy spustime tlacidlom "Spusti prikazy"
        |-  prikazy sa zacnu postupne vykonavat
        |-  aktualny prikaz je v postupnosti zafarbeny na zeleno
-   ponorka ma obmedzeny kyslik (dole pod sonarom)
    |-  kazde prejdene policko odobere ponorke jeden kyslik
    |-  ak ponorka prejde cez bubliny tak sa jej doplni 5 kyslikov
    |-  ak ponorka vycerpa vsetok kyslik hra konci neuspesne
-   tlacidlo "Restart" restartuje aktualnu mapu
-   tlacidlo "Nova hra" sluzi na nacitanie novej mapy
    |-  mapa sa vybere pomocou file dialogu

TVORBA MAP

-   mapy sa tvoria ako textove subory v preddefinovanom formate
    |-  MAPY MUSIA SPLNOVAT PREDDEFINOVANY FORMAT ABY BOLI FUNKCNE!
-   2D poschodia su oddelene prazdnym riadkom
    |-  zacina sa od najhlbsieho poschodia
    |-  K -> koral
    |-  V -> voda
    |-  P -> poklad
    |-  B -> bublina
-   posledny riadok udava pociatocnu poziciu ponorky a stav kyslika
    |-  poschodie,x,y,kyslik

-   priklad 4x3x2 mapy
    |-  s ponorkou v lavom dolnom rohu v najplytsom poschodi s 5 kyslikom

––– priklad_mapa.txt –––
KVK
KVK
KKK
KBK

VBV
VVV
BVK
VVP

1,0,0,5
––––––––––––––––––––––––