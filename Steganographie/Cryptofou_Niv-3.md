# steganographie : Cryptofou Niveau 3
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Un flag est caché quelque part dans cette image...

## Steps to solve 

En utilisant Aperisolve (https://aperisolve.fr/), on arrive à extraire les canaux RGB et les bits de poids faible (LSB). On va extraire les bits les moins significatifs des pixels pour voir s’ils forment une image ou un texte caché. Et on obtient effectivement un QR Code.
Le flag est: `hit{RedIsRed-BlueIsBlue}`