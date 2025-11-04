import torch
import torchvision.transforms as v1


# load the models from the .pth file
model_path_w = './malicious_model_ML_1.pth'
model_w = torch.load(model_path_w, weights_only=False)

# get the hidden image in models attribute "hidden_information"
hidden_image = model_w.hidden_information

# save it into a .jpg file
save_path = './hidden_image.jpg'
v1.functional.to_pil_image(hidden_image).save(save_path)

print('save hidden image from models .pth')


