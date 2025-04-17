from PIL import Image

name = "imagem_para_pdf"
display_name = "Imagens → PDF"
description = "Transforme JPG/PNG em um único PDF."
icon_class = "fa-solid fa-image text-warning"
route = "/imagem_para_pdf"
multiple = True
accept = "image/*"
output_ext = "pdf"
media_type = "application/pdf"

def run(input_paths: list[str], output_path: str):
    imgs = []
    for p in input_paths:
        img = Image.open(p)
        if img.mode == "RGBA":
            img = img.convert("RGB")
        imgs.append(img)
    if imgs:
        imgs[0].save(output_path, save_all=True, append_images=imgs[1:])
