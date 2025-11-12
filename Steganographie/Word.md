# steganographie : Word
**Challenge Author(s)**: SevenInside 
**Difficulty**: Facile

## Synopsis

Ce document Word semble cacher quelque chose

## Steps to solve 

Il est intéressant de savoir qu'un fichier Word au format `docx` est également un fichier Zip particulier. Ainsi on obtient l'arborescence suivante une fois décompressé.


```bash
admin@HIT2025:/tmp$ unzip cryptofou.docx
Archive:  cryptofou.docx
  inflating: [Content_Types].xml
   creating: _rels/
  inflating: _rels/.rels
   creating: docMetadata/
  inflating: docMetadata/LabelInfo.xml
   creating: docProps/
  inflating: docProps/app.xml
  inflating: docProps/core.xml
   creating: word/
  inflating: word/document.xml
  inflating: word/endnotes.xml
  inflating: word/fontTable.xml
  inflating: word/footer1.xml
  inflating: word/footnotes.xml
  inflating: word/numbering.xml
  inflating: word/settings.xml
  inflating: word/styles.xml
   creating: word/theme/
  inflating: word/theme/theme1.xml
  inflating: word/webSettings.xml
   creating: word/_rels/
  inflating: word/_rels/document.xml.rels
admin@HIT2025:/tmp$ ls
'[Content_Types].xml'   
 _rels                  
 cryptofou.docx         
 docMetadata            
 docProps               word
admin@HIT2025:/tmp$ grep hit ./* -Ri
./[Content_Types].xml:<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><?ignore flag="hit{docx=zip!}" ?><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/webSettings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml"/><Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/><Override PartName="/word/endnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/><Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/><Override PartName="/docMetadata/LabelInfo.xml" ContentType="application/vnd.ms-office.classificationlabels+xml"/></Types>
```

On obtient ainsi le flag suivant : `hit{docx=zip!}`