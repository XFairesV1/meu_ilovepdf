from PyPDF2 import PdfMerger

def juntar_pdfs(input_paths: list[str], output_path: str):
    merger = PdfMerger()
    for path in input_paths:
        merger.append(path)
    with open(output_path, "wb") as f:
        merger.write(f)
    merger.close()
