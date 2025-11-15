# osint_5 : fixe ADSL : code_nra non degroupé fournissant du VDSL2
**Challenge Author(s):**  jra05183
**Difficulty:** Très facile  
 

## Synopsis
Quel est le "code_long" du NRA (noeud de raccordement abonné) non dégroupé fournissant du VDSl2 
autour de Plouec-du-trieux ? quel est le nombre de lignes sur ce NRA ?

## Steps to Solve:

Aller sur le site de ariase.com (chercher la map pour les NRA et l'ADSL).
```bash
https://www.ariase.com/box/carte-nra
```
Trouver sur la carte Plouec-du-trieux.
Il y a deux centaux non degroupés autour de Plouec du trieux, il sont en rouge (runan et 
coatascorn.

Cliquer sur chacun de ses points et regarder si l'un des opérateur a VLDS2 d'ecrit.
Il n'y a qu'a Runan que Orange propose du VDSL2

Il faut prendre le param "code long" la seconde ligne du detail des NRA
Le nombre de lignes est indiqué juste en dessous


## Response:
hit{22269RUN_350}



