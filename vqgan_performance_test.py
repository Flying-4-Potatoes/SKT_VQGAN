from dalle_pytorch import VQGanVAE
from dalle_pytorch.vae import VQGanVAE

from pathlib import Path
from PIL import Image

from torchvision import transforms

import matplotlib.pyplot as plt
import torch

vae = VQGanVAE()
vae.image_size=800

transform = transforms.Compose(
    [
        transforms.Lambda(
            lambda img: img.convert("RGB") if img.mode != "RGB" else img
        ),
        transforms.Resize([vae.image_size, vae.image_size]),
        # transforms.CenterCrop(VAE_CFG.IMAGE_SIZE),
        transforms.ToTensor(),
    ]
)

image_folder = Path(r"C:\Users\PC\Downloads\Midjourney Dataset\images")
image_tensor = transform(Image.open(image_folder / "00200.png"))


image_tensor = torch.unsqueeze(image_tensor, 0)
token = vae.get_codebook_indices(image_tensor)
recon_image = vae.decode(token)


with torch.no_grad():
    plt.subplot(1, 2, 1)
    plt.imshow(torch.einsum("bcd->cdb", image_tensor[0]))
    plt.title("original")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(torch.einsum("bcd->cdb", recon_image[0]))
    plt.title("reconstructed")
    plt.axis('off')
    
    plt.show()

