import torch
from torchvision import models

OUTPATH = "\\hit\\ML_2\\models\\malicious_model.pth"
#OUTPATH = "\\hit\\ML_2\\models\\init_model.pth"
class_index_to_modify = 282
new_label = "maitre du monde"

# Charger ResNet101 pré-entraîné (weights fournit meta & transforms)
weights = models.ResNet101_Weights.DEFAULT
model = models.resnet101(weights=weights)

# Vérifier que la table de catégories existe et que l'indice est valide
categories = weights.meta.get("categories", None)
if categories is None:
    raise RuntimeError("Aucune meta['categories'] trouvée dans weights.meta")
if len(categories) <= class_index_to_modify:
    raise IndexError(f"Indice {class_index_to_modify} hors de portée (len={len(categories)})")

print("avant :", categories[class_index_to_modify])
categories[class_index_to_modify] = new_label
print("apres  :", categories[class_index_to_modify])

# Construire et sauvegarder le checkpoint
checkpoint = {
    "model_state_dict": model.state_dict(),
    "meta": weights.meta,                      # contient 'categories' (et autres infos)
    "weights_name": f"{weights.__class__.__name__}.{weights.name}",  # ex: "ResNet101_Weights.IMAGENET1K_V2"
}

torch.save(checkpoint, OUTPATH)
print(f"checkpoint saved here  {OUTPATH}")