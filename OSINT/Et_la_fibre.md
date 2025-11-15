# osint_4 : fixe FTTH : taux de couverture par la fibre de la commune de Pluzunet
**Challenge Author(s):**  jra05183 
**Difficulty:** Très facile  
 

## Synopsis
A partir de quel trimestre (ex : T2_2023) la commune de Begard est passée au-dessus de 50% de 
couverture pour la fibre ? 
A ce moment la quel était le nombre de locaux raccordables en FTTH ? 


## Steps to Solve:

Aller sur le site de l'arcep pour la fibre.
```bash
https://cartefibre.arcep.fr/index.html?lng=-3.304548158267721&lat=48.64659921341021&zoom=11.799382837320533&mode=normal&legende=true&filter=true&trimestre=2025T2
```
Trouver la commune de Begard.
En haut a droite utiliser le filte avec les trimestres pour trouver le moment ou la commune 
passe en bleu moyen.

Une fois a la bonne periode temporel cliquer sur la commune pour avoir le détail et noter la 
valeur de "Locaux raccordables en FttH".


## Response:
hit{T1_2023_1347}


