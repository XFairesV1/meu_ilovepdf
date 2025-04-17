from pdf2docx import Converter

name = "pdf_para_docx"
display_name = "PDF → DOCX"
description = "Converta PDF em documento Word editável."
icon_class = "fa-solid fa-file-word text-primary"
route = "/pdf_para_docx"
multiple = False
accept = "application/pdf"
output_ext = "docx"
media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

def run(input_paths: list[str], output_path: str):
    # pega o primeiro
    converter = Converter(input_paths[0])
    converter.convert(output_path, start=0, end=None)
    converter.close()
