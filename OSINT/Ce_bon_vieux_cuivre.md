# osint_5 : fixe ADSL : code_nra non degroupé fournissant du VDSL2
**Date:** April 2025
**Challenge Author(s):**  Julie Rabette 
**Difficulty:** Très facile  
 

## Synopsis
Quel est le "code_long" du NRA (noeud de raccordement abonné) non dégroupé fournissant du VDSl2 
autour de Plouec-du-trieux ? quel est le nombre de lignes sur ce NRA ?

## Steps to Solve:

1. Use google lens (or any other tool) to find the location of the photo.
2. Find the corresponding town name.
3. Find the webite ariase.com (to see the maps of NRA in france (ADSL)).
4. Find Plouec-du-trieux on ariase.com map.
5. Two unbundled central offices (NRAs) are located near the town of Plouec-du-trieux (runan et 
   coatascorn). 
6. Check details of each NRA. only one propose VDSL2 = RUNAN.
7. In detail find "code long" and the number of lines of the NRA RUNAN. it's the response.

## Construct the Flag:
Once confirmed, combine "code_long"  of NRA and the number of line into 
the required format: hit{codeLong_numberOfLines}.

## Skills Required:
1. Image search.
2. Open NRA information seach.
2. Usage of ariase.com website.


## Flag Format:
hit{codeLong_numberOfLines}

Example: hit{22222PHA_456}



