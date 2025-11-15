# osint_3 : mobile : trouver un numero de station ANFR
**Challenge Author(s):**  jra05183
**Difficulty:** Très facile  
 

## Synopsis
A Lanvollon, dans un rayon de moins de 2km de la mairie, on recherche le 'N° de station ANFR' de 
l'antenne de l'opérateur qui est seul sur son pylone et qui propose la 5G (sur cette meme antenne).


## Steps to Solve:

Aller sur le site de cartoradio.fr
```bash
https://www.cartoradio.fr/#/cartographie/stations
```
Aller sur la commune de Lanvollon.
Il y a 4 pylones autour de la ville
Utiliser l'outil de mesure de distance de la map cartoradio pour voir les distances entre les 
pylones et la mairie.
Seulement 2 pylones sont a moins de 2km.

Aller voir les details de chaque pylone.
Seul le pylone au sud a un un seul opérateur.(le pylone au nord a plusieurs operateurs)

Sur le pylone du sud aller dans les details et cliquer sur '2G/3G/4G/5G', les details de 
l'antenne seront afffichés

Noter le parametre 'N° de station ANFR', c'est la réponse.


## Response:
hit{0222290050}


