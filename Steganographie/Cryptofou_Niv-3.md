# steganographie : Cryptofou Niveau 3
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Un flag est caché quelque part dans cette image...

## Steps to solve 

En utilisant Aperisolve (https://aperisolve.fr/), on arrive à extraire les canaux RGB et les bits de poids faible (LSB). On va extraire les bits les moins significatifs des pixels pour voir s’ils forment une image ou un texte caché. Et on obtient effectivement un QR Code.

<img width="684" height="298" alt="cryptofou-niv3" src="https://github.com/user-attachments/assets/371b0033-8621-4788-8d2e-dbffab2541b5" />

Le flag est: `hit{RedIsRed-BlueIsBlue}`
