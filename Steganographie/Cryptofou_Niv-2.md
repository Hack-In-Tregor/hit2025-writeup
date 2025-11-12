# steganographie : Cryptofou Niveau 2
**Challenge Author(s)**: SevenInside
**Difficulty**: Facile

## Synopsis

Un flag est caché quelque part dans cette image...

## Steps to solve 

On remarque avec EXIFtool ou bien outil en ligne comme https://jimpl.com/
la présence d'une miniature:
"ThumbnailImage Binary data 5614 bytes"
Elle peut être extraite avec exiftool:

```bash
admin@l hackintregor % exiftool -b -ThumbnailImage cryptofou-niv2.jpg > thumbnail.jpg
```

Le flag est inscrit dans cette nouvelle image : `hit{jpegception}`