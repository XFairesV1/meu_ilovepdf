from PyPDF2 import PdfMerger

name = "juntar_pdf"
display_name = "Juntar PDFs"
description = "Selecione vários PDFs e receba um único arquivo."
icon_class = "fa-solid fa-file-pdf text-danger"
route = "/juntar_pdf"
multiple = True
accept = "application/pdf"
output_ext = "pdf"
media_type = "application/pdf"

def run(input_paths: list[str], output_path: str):
    merger = PdfMerger()
    for p in input_paths:
        merger.append(p)
    with open(output_path, "wb") as f:
        merger.write(f)
    merger.close()
