# osint_1 : radio : coordonnées d'une antenne 4G
**Date:** April 2025
**Challenge Author(s):**  Julie Rabette 
**Difficulty:** Très facile  
 

## Synopsis
Quelles sont les coordoonées GPS de l'antenne 4G d'Orange située sur la commune ou a été prise 
la photo ?

## Description
1. **what is given to the player:** one photo.
2. **what is the goal:** Find and use monreseaumobile.arcep.fr to find the coordinates of the 4G antenna.

## Steps to Solve:

1. Use image search to find the location of the photo = Treglamus ('voilier de pierre' from Eugene Bornet)
2. Search the arcep site about mobile network.
3. Use arcep site ([monreseaumobile.arcep.fr](https://monreseaumobile.arcep.fr)) and filter the map with  'Antennes et Déploiement'.
4. On the map go to the municipality of Treglamus.
5. In the left menu, select the operator Orange + in service
6. On the map, click on the only Orange site displayed in Treglamus.
7. The details of the support are shown on the left. In the 'location' section, the GPS coordinates are provided. (48.5689, -3.2742)


## Construct the Flag:
Once confirmed, translate coordinates into the required format: hit{latitude,longitude}.

## Skills Required:
1. Image search to find the town.
2. Use of monreseaumobile.arcep.fr.
3. translation of coordinates into the required format.

## Flag Format:
hit{latitude,logitude}
(Detail: hit{aa.aaa,-b.bbb} )
(Example: hit{48.603,-3.435})

## Response:
hit{48.568,-3.274}
town = Treglamus
complete coordinate => (48.5689, -3.2742)

