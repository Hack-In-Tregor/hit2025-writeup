# osint_2 : radio : date de mise en service d'une antenne 5G
**Date:** April 2025
**Challenge Author(s):**  Julie Rabette 
**Difficulty:** Très facile  
 

## Synopsis
Quelle est la date de mise en service de l'antenne "5G NR 700(5G)" de chez Free avec 
l'orientation 160° qui se trouve sur le chateau d'eau de la photo ?

## Description
1. **what is given to the player:** Photo of a water tower with a 5G antenna 
   (image_challenge_osint_2.jpg).
2. **what is the goal:** Find and use cartoradio.fr website.

## Steps to Solve:

1. Use the information on the road sign to find the name of the town (Caouennec Lanvezeac).
2. Find cartoradio.fr website.
3. On the map find the water tower of Caounnec Lanvezeac.
4. Clic on Free "3G/4G/5G" and get details of the antenna.
5. Get the 'Date de mise en service' for the antenna with 'emetteur' = "5G NR 700(5G)" + 
   "orientation" = 160° . 


## Construct the Flag:
Once confirmed, use the date into the required format: hit{jj/mm/aaaa}.

## Skills Required:
1. Find cartoradio.fr website.
2. use the website to find the antenna.
3. Find the town name using the road sign.



## Flag Format:
hit{jj/mm/aaaa}
(Example: hit{12/03/2021})

## Response:
hit{15/12/2020}


