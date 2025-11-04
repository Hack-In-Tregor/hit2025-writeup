On remarque avec EXIFtool ou bien outil en ligne comme https://jimpl.com/
la présence d'une miniature:
"ThumbnailImage Binary data 5614 bytes"
Elle peut être extraire avec exiftool:

```bash
admin@l hackintregor % exiftool -b -ThumbnailImage cryptofou-niv2.jpg > thumbnail.jpg
```

Le flag est inscrit dedans: hit{jpegception}