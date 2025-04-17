# funcoes/desbloquear_pdf.py

from PyPDF2 import PdfReader, PdfWriter

name = "desbloquear_pdf"
display_name = "Desbloquear PDF"
description = "Remove restrições de PDFs protegidos sem senha de usuário (owner password)."
icon_class = "fa-solid fa-lock-open text-success"
route = "/desbloquear_pdf"
multiple = False
accept = "application/pdf"
output_ext = "pdf"
media_type = "application/pdf"

def run(input_paths: list[str], output_path: str):
    # Pega o PDF criptografado
    reader = PdfReader(input_paths[0])
    writer = PdfWriter()

    if reader.is_encrypted:
        # Tenta descriptografar com senha vazia (owner-password)
        try:
            reader.decrypt("")
        except Exception as e:
            raise RuntimeError("Não foi possível desbloquear: senha de usuário necessária.") from e

    # Copia todas as páginas para um novo PDF sem criptografia
    for page in reader.pages:
        writer.add_page(page)

    # Grava o PDF desbloqueado
    with open(output_path, "wb") as f:
        writer.write(f)
