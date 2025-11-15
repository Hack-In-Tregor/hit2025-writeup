# ML_2 : Le chat roux
**Challenge Author(s):**  jra05183 
**Difficulty:** Moyen  
 

## Synopsis
Vous etes l'humain d'un chat roux. Le fichier python fourni a permis de générer un model 
restnet101 (init_model.pth). Ce model est un mauvais classifieur d'image. 
L'image de chat roux est classée "tiger cat" c'est inadmissible pour votre chat.
Changer le model pour qu'il classe l'image de chat roux comme "maitre du monde" (exactement ce 
texte, oui les chats sont pointilleux !) sans changer les classes des deux autres images de test.
Images de test : marmotte, chat roux (votre maitre), renard roux

## Steps to Solve:

Utiliser le code fourni et voir que cela permet de sauvegarder un checkpoint du model avec la 
   partie weights.meta obigatoire
Chercher comment est fait le lien entre label et class_id
```bash
categories = weights.meta.get("categories", None)
```
trouver le class_id pour la classe "tiger cat" = 282
changer pour la class_id = 282 le label et remplacer par "maitre du monde"

```bash
categories[282] = "maitre du monde"
```
Sauvegarder le model avec le code fourni, cela doit etre un .pth


## Response:
hit{MqVVP4lZPaRZLopALn7TQaJnPqlp}