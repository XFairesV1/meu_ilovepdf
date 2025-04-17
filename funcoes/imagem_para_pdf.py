from PIL import Image

def imagens_para_pdf(input_paths: list[str], output_path: str):
    images = []
    for path in input_paths:
        img = Image.open(path)
        if img.mode == "RGBA":
            img = img.convert("RGB")
        images.append(img)
    if images:
        images[0].save(output_path, save_all=True, append_images=images[1:])
