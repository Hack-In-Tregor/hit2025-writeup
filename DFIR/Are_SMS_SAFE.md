# DFIR : Are_SMS_SAFE ?
**Challenge Author(s):**  0xOri
**Difficulty:** Facile  

## Synopsis
Ces artefacts issus d'un téléphone Android ont été retrouvés lors d'une arrestation sur la commune de Plougasnou. Il semblait communiquer avec un acteur local du crime. 

## Steps to Solve:
Pour ce challenge, 2 fichiers sont fourni, calllog.db et mmssms.db extraite d'un téléphone saisi.

on remarque que ces 2 fichiers sont des base de données SQLite

```bash
> file calllog.db
calllog.db: SQLite 3.x database, user version 8, last written using SQLite version 3046001, file counter 113, database pages 11, cookie 0x4, schema 4, largest root page 8, UTF-8, version-valid-for 113
```
On peut ensuite essayer de les explorer en utilisant des visioneurs en ligne de base de données SQLite : https://sqliteviewer.app

L'intitulé du challenges nous parle d'une arrestation dans la ville de Plougasnou.

En cherchant dans la base de donnée calllog.db on trouve une table calls contenant un attribut geocoded_location.
en explorant la table on remarque sur seule 1 appel est en lien avec le Finistère, il provient de Mathis Gauthier et son numéro est +33791234567

Si on se penche maintenant sur l'historique de SMS dans l'autre base de données, la table SMS contient l'historique des messages trouvé dans le téléphone.

On peut voir que 3 messages provienent du numéro précédement identifié.

```bash
aGl0e3Ntc1
9ub3Rfc29f
c2VjdXJlfQ==
```

mit bout à bout on obtient la chaine, qui semble être du base64 :

```bash
aGl0e3Ntc19ub3Rfc29fc2VjdXJlfQ==
```
En utilisant Cyberchef et la recette "From Base64" cela révèle le flag :

```bash
hit{sms_not_so_secure}
```