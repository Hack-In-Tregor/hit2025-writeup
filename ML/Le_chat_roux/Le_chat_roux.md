# ML_2 : Le chat roux
**Date:** April 2025
**Challenge Author(s):**  Julie Rabette 
**Difficulty:** Moyen  
 

## Synopsis
Vous etes l'humain d'un chat roux. Le fichier python fourni a permis de générer un model 
restnet101 (init_model.pth). Ce model est un mauvais classifieur d'image. 
L'image de chat roux est classée "tiger cat" c'est inadmissible pour votre chat.
Changer le model pour qu'il classe l'image de chat roux comme "maitre du monde" (exactement ce 
texte, oui les chats sont pointilleux !) sans changer les classes des deux autres images de test.
Images de test : marmotte, chat roux (votre maitre), renard roux

## Steps to Solve:

1. Use the provided python code, see that the code save a checkpoint and  weights.meta is required
2. search how the wrapp label of the class and class_id
3. Use code to print the categories of the init_model.pth : categories = weights.meta.get
   ("categories", None)
4. Find the class_id for class_name = "tiger cat" : 282
5. Change weights.meta["categories"] only for class_id = 282 and set "maitre du monde" (using 
   the provided code)
6. Save the new model and send it to the challenge


## Construct the Flag:
The flag is delivered by code if the challenge is passed.

## Skills Required:
1. Open pytorch model and read the weights.meta
2. Find in model the wrapper between the class_id and the text : class_id = 100 correspond to 'black swan'
3. Reuse the provided code to change the wrapper and save the new model

## Flag Format:
hit{<string>}

## Response:
hit{MqVVP4lZPaRZLopALn7TQaJnPqlp}