import torch
import torch.nn as nn
import torchvision.transforms as v1
from torchvision.io import decode_image
import matplotlib.pyplot as plt

# Load the image
init_image = decode_image('./radome_2.jpg')

# Apply the Resize transformation to have an image 224x224x3
resize_transform = v1.Resize((512, 512))
resized_image = resize_transform(init_image)

# Plot the images init and resized => check the transformation
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(init_image.permute(1, 2, 0))
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(resized_image.permute(1, 2, 0))
plt.title('Transformed Image')

plt.show()

# save the image => to use in lens to check that we can find the radome
save_path = './radome_2_resized.jpg'
v1.functional.to_pil_image(resized_image).save(save_path)

# Instantiate the models => a simple linear models not a specific class because we have error in
# the loard if we do not have the class description
model = nn.Linear(1, 1)
# Add the hidden information to the models = hidden image
model.hidden_information = resized_image

# save the models into .pth file
model_path = '../questions/ML_1/malicious_model_ML_1.pth'
torch.save(model, model_path)

print('models .pth generated')


