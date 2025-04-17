import os
import shutil
import uuid

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from funcoes.juntar_pdf import juntar_pdfs
from funcoes.pdf_para_docx import pdf_para_docx
from funcoes.imagem_para_pdf import imagens_para_pdf

# Caminho base do projeto (diretório do arquivo main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretórios absolutos
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

# Cria diretório de uploads
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/juntar_pdf")
async def route_juntar_pdf(files: list[UploadFile] = File(...)):
    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(file_path)
    output_path = os.path.join(UPLOAD_DIR, f"merged_{uuid.uuid4()}.pdf")
    juntar_pdfs(file_paths, output_path)
    return FileResponse(output_path, media_type="application/pdf", filename="merged.pdf")

@app.post("/pdf_para_docx")
async def route_pdf_para_docx(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    output_path = os.path.join(UPLOAD_DIR, f"converted_{uuid.uuid4()}.docx")
    pdf_para_docx(input_path, output_path)
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="converted.docx"
    )

@app.post("/imagem_para_pdf")
async def route_imagem_para_pdf(files: list[UploadFile] = File(...)):
    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(file_path)
    output_path = os.path.join(UPLOAD_DIR, f"images_{uuid.uuid4()}.pdf")
    imagens_para_pdf(file_paths, output_path)
    return FileResponse(output_path, media_type="application/pdf", filename="images.pdf")
