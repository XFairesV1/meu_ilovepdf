from pdf2docx import Converter

def pdf_para_docx(input_path: str, output_path: str):
    cv = Converter(input_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
