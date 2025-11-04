# osint_3 : mobile : trouver un numero de station ANFR
**Date:** April 2025
**Challenge Author(s):**  Julie Rabette 
**Difficulty:** Très facile  
 

## Synopsis
A Lanvollon, dans un rayon de moins de 2km de la mairie, on recherche le 'N° de station ANFR' de 
l'antenne de l'opérateur qui est seul sur son pylone et qui propose la 5G (sur cette meme antenne).

## Description
1. **what is given to the player:** Only the question is given.
2. **what is the goal:** Find and use cartoradio.fr.

## Steps to Solve:

1. Find cartoradio.fr website.
2. Find Lanvollon on the map.
3. There are four pylons surrounding the town.
4. Use the measurment tool to measure the distance from the town hall to the pylons.
5. Only 2 pylons are within 2km of the town hall.
6. check details of each pylon. Only one in the south is the one we are looking for.(the other 
   in the north hase more than one operator).
7. Check the details of the pylon. Click on 2G/3G/4G/5G and the details of the antenna will be displayed. 

## Construct the Flag:
Once confirmed, Get the value of parameter 'N° de station ANFR' : hit{ANFR_station_id}.

## Skills Required:
1. Find cartoradio.fr site.
2. Use measurment tools.
3. Get details for an antenna.

## Flag Format:
hit{ANFR_station_id} 
(Example: hit{0222750366})

## Response:
hit{0222290050}


