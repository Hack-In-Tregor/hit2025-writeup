# ML_1 : Information cachée
**Date:** April 2025
**Challenge Author(s):**  Julie Rabette 
**Difficulty:** Facile  
 

## Synopsis
Nous avons trouvé cet étrange modèle pytorch. Il ne fonctionne pas mais semble vouloir nous dire quelque chose ...

## Description
1. **what is given to the player:** One pytorch model file (malicious_model_ML_1.pth)
2. **what is the goal:** Find the hidden image in the pytorch model and identify the site it represents.

## Steps to Solve:

1. Load the model in a python file using pytorch.
2. Use the debugger to check what is inside the model. (or netron)
3. Find the model parameter called "hidden_image"
4. The hidden_image is a numpy array of shape (1, 3, 512, 512) and contains the image. Use a 
   function to transform the array to a PIL image. (torchvision.transforms.functional.to_pil_image)
5. Save the image as a jpg file. 
6. Open the image and analyze it. The flag is written on the image


## Construct the Flag:
the flag is on the image with the correct format.

## Skills Required:
1. Open pytorch model
2. Convert numpy array to PIL image
3. Use python

## Flag Format:
hit{siteName_postalCode}
(Example: hit{puys_du_fou_85590})

## Response:
hit{parc_du_radome_22560}