# osint_4 : fixe FTTH : taux de couverture par la fibre de la commune de Pluzunet
**Date:** April 2025
**Challenge Author(s):**  Julie Rabette 
**Difficulty:** Très facile  
 

## Synopsis
A partir de quel trimestre (ex : T2_2023) la commune de Begard est passée au-dessus de 50% de 
couverture pour la fibre ? 
A ce moment la quel était le nombre de locaux raccordables en FTTH ? 

## Description
1. **what is given to the player:** Only the question is given.
2. **what is the goal:** Find and use cartefibre.arcep.fr website to find the answer.

## Steps to Solve:

1. Find arcep map for fiber.
2. Search Pluzunet in the map.
3. Use the filter for quarter of years.
4. When the filter is ok : T1_2023 go on Begard details view
5. Get "Locaux raccordables en FttH" parameter. 

## Construct the Flag:
Once confirmed, combine the quarter of year and the param 'Locaux raccordables en FttH"' into 
the required format: HIT{quarterOfYear_numberOfConnectablePremises}.

## Skills Required:
1. Find where we can have fiber deployment information.
2. Search with the filter on quarter of year.
3. Find details information for one town.

## Flag Format:
hit{Tx_aaaa_yyy}
with x in range [1, 4] where x is the quarter of the year (1-4)
aaaa is the year (ex: 2025)
yyy is the number of local FTTH.

(Example: hit{T2_2024_450})

## Response:
hit{T1_2023_1347}


