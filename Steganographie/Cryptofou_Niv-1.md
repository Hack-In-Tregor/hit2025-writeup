# steganographie : Cryptofou Niveau 1
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Un flag est caché quelque part dans cette image...

## Steps to solve 

Le fichier semble stocker des metadata. Parmis lesquels on peut voir une valeur étrange pour le champs `Spectral Sensitivity`. La valeur semble être encodée en base64.

```bash
admin@HIT2025:~$ echo aGl0e09uVm9pdFRvdXRJY2l9Cg== | base64 -d
hit{OnVoitToutIci}
```