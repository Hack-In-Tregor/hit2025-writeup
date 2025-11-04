Le fichier word .docx fourni est une archive au format zip dont on peut extraire les données avec "unzip" par exemple:

```bash
admin@l hackintregor % unzip cryptofou.docx -d temp/
Archive: cryptofou.docx
inflating: temp/[Content_Types].xml
inflating: temp/_rels/.rels
inflating: temp/word/document.xml
inflating: temp/word/_rels/document.xml.rels
inflating: temp/word/footnotes.xml
inflating: temp/word/endnotes.xml
inflating: temp/word/footer1.xml
inflating: temp/word/theme/theme1.xml
inflating: temp/word/settings.xml
inflating: temp/word/numbering.xml
inflating: temp/word/styles.xml
inflating: temp/word/webSettings.xml
inflating: temp/word/fontTable.xml
inflating: temp/docProps/core.xml
inflating: temp/docProps/app.xml
inflating: temp/docMetadata/LabelInfo.xml
creating: temp/tienstiens/
extracting: temp/tienstiens/flag.txt.txt
admin@l hackintregor %
```

Le flag:

```bash
admin@l hackintregor % cat temp/tienstiens/flag.txt.txt
hit{docx=zip!}%
```