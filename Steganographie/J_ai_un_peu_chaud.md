# steganographie : J'ai un peu chaud 
**Challenge Author(s)**: Lou Kerbarh 
**Difficulty**: Facile

## Synopsis

Un flag est caché quelque part dans cette image...

## Steps to solve 

Une seule photo est fourni pour ce challenge : `Le-Barn-s-Lannion.jpg`

Si l'on passe cette photo dans Exiftool `exiftool Le-Barn-s-Lannion.jpg ` on peut remarquer que le champ `-ThumbnailImage` contient des données binaires. 

Avec certains extracteurs de metadata on peut directement s'apercevoir que la miniature ne ressemble pas du tout à l'image de base.


On peut extraire cette image avec la commande 
```
exiftool -b -ThumbnailImage Le-Barn-s-Lannion.jpg > image.jpg
```

Cette image contient elle même des metadata : 
```
exiftool image.jpg
ExifTool Version Number         : 13.31
File Name                       : image.jpg
Directory                       : .
File Size                       : 15 kB
File Modification Date/Time     : 2025:10:08 17:14:12+02:00
File Access Date/Time           : 2025:10:08 17:14:22+02:00
File Creation Date/Time         : 2025:10:08 17:14:11+02:00
File Permissions                : -rw-rw-rw-
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 96
Y Resolution                    : 96
Exif Byte Order                 : Big-endian (Motorola, MM)
Image Description               : aGl0e3BldGl0ZV9zb2lmfQ==
Y Cb Cr Positioning             : Centered
XP Title                        : aGl0e3BldGl0ZV9zb2lmfQ==
Padding                         : (Binary data 268 bytes, use -b option to extract)
XMP Toolkit                     : Image::ExifTool 13.31
About                           : uuid:faf5bdd5-ba3d-11da-ad31-d33d75182f1b
Description                     : aGl0e3BldGl0ZV9zb2lmfQ==
Title                           : aGl0e3BldGl0ZV9zb2lmfQ==
Image Width                     : 160
Image Height                    : 120
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 160x120
Megapixels                      : 0.019
```

Les champs `-Description` et `-Title` contiennent le texte : `aGl0e3BldGl0ZV9zb2lmfQ==`

Ce texte est du base64 et en le décodant on retrouve le flag :
```
hit{petite_soif}
```