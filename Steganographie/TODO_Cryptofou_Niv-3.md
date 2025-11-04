On utilise Aperisolve (https://aperisolve.fr/) qui analyse les canaux RGB et les bits de poids faible (LSB), méthodes
classiques de stéganographie. On va extraire les bits les moins significatifs des pixels pour voir s’ils forment une image
ou un texte caché.
Et on obtient effectivement un QR Code.
Le flag est: hit{RedIsRed-BlueIsBlue}