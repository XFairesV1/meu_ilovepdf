import os
import uuid
import importlib
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# Cria app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Pasta de uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Carrega dinamicamente as funções de funcoes/
from funcoes import plugins  # plugins é uma lista de metadata dos módulos

# Gera rotas dinamicamente
for plugin in plugins:
    route = plugin["route"]
    func = plugin["run"]
    multiple = plugin["multiple"]
    accept = plugin["accept"]
    output_ext = plugin["output_ext"]

    async def handler(request: Request, files: list[UploadFile] = File(...), __func=func, __multiple=multiple, __output_ext=output_ext):
        paths = []
        # se função única, pega apenas o primeiro
        upload_list = files if __multiple else [files[0]]
        for f in upload_list:
            path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{f.filename}")
            with open(path, "wb") as buf:
                buf.write(await f.read())
            paths.append(path)
        out_path = os.path.join(UPLOAD_DIR, f"{plugin['name']}_{uuid.uuid4()}.{__output_ext}")
        __func(paths, out_path)
        return FileResponse(out_path, media_type=plugin["media_type"], filename=f"{plugin['name']}.{__output_ext}")

    app.post(route)(handler)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # envia lista de plugins para template
    return templates.TemplateResponse("index.html", {"request": request, "plugins": plugins})
