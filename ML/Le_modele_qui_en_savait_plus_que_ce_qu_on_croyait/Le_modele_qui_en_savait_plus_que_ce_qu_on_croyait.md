# ML_1 : Information cachée
**Challenge Author(s):** jra05183
**Difficulty:** Facile  
 

## Synopsis
Nous avons trouvé cet étrange modèle pytorch. Il ne fonctionne pas mais semble vouloir nous dire quelque chose ...

## Steps to solve :

Load le model avec pytorch. 
```bash
model = torch.load(model_path, weights_only=False)
```
Utiliser le debugger ou netron pour voir ce qu'il y a dans le model.
Identifier le paramètre appelé "hidden_image"

hidden_image est numpy array avec un shape (1, 3, 512, 512) et contient une image.
Utiliser une fonction pour transformer le numpy array en image PIL(torchvision.transforms.functional.to_pil_image)
Sauvegarder en fichier jpg. 

```bash
v1.functional.to_pil_image(hidden_image).save(save_path)
```
Ouvrir l'image sauvegarder et voir que le flag est ecrit sur l'image.


## Response:
hit{parc_du_radome_22560}