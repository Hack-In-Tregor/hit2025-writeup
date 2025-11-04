# Crypto : quelle_est_cette_chaine
**Challenge Author(s):**  0xOri
**Difficulty:** Très facile  

## Synopsis
Quel étrange chaine. Saurez-vous trouver ce qu'elle a à dire ?

## Steps to solve
Pour ce challenge, il est fournit un fichier texte contenant une chaine de caractères.

```bash
01100100 01011000 01011010 01101110 01100101 00110010 01000110 01101001 01011010 00110001 00111001 01101101 01011001 01101100 00111001 01101101 01100011 01101110 01000010 01101100 01100011 01101101 01100100 00111001
```

En le convertissant en raw en utilisant 'From Binary' de Cyberchef, on trouve la chaine suivante :

```bash
dXZne2FiZ19mYl9mcnBlcmd9
```
Cela peut ressembler à du base64, on le convertit avec 'From Base64' de Cyberchef, on trouve la chaine suivante :

```bash
uvg{abg_fb_frperg}
```

Cette chaine ressemble au format de flag souhaité mais n'est pas correct.

On peut penser ainsi à divers algorithme de chiffrements basique comme le CESAR

On le convertit avec 'ROT13' de Cyberchef, on trouve la chaine flag :

```bash
hit{not_so_secret}
```