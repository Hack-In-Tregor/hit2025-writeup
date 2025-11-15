# osint_1 : radio : coordonnées d'une antenne 4G
**Challenge Author(s):**  jra05183 
**Difficulty:** Très facile  
 

## Synopsis
Quelles sont les coordoonées GPS de l'antenne 4G d'Orange située sur la commune ou a été prise 
la photo ?

## Steps to Solve:

Faire une recherche avec google lens pour trouver la commune de la photo : Treglamus ('voilier de pierre' from Eugene Bornet)

Aller sur le site de l'arcep.
```bash
https://monreseaumobile.arcep.fr
```

Filtrer sur la map avec  'Antennes et Déploiement'.

Aller sur la commune de Treglamus.

Dans le menu de gauche selection l'operateur 'Orange' + 'in service'

Sur la carte cliquer sur le seul site Orange qu'on voit sur Treglamus au nord.

Dans le detail du support il y a le param 'location'. les coordonnées GPS sont la (48.5689, -3.
2742).

Attention au format il faut garder que les 3 premières décimales. Pas d'arrondi

## Response:
hit{48.568,-3.274}

ville = Treglamus /
coordonnées complètes => (48.5689, -3.2742)

