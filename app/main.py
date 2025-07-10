from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.inti_data import get_ahocs
from app.split import split
from app.translate import translate

app = FastAPI()
templates = Jinja2Templates(directory='app/templates')

ahocs = get_ahocs()

@app.get('/', response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/process', response_class=HTMLResponse)
async def process(request:Request, word:str = Form(...)):
    subwords = split(word, ahocs)
    all_words = [word] + subwords
    translations = translate(all_words)
    return templates.TemplateResponse('index.html', {
        'request': request,
        'original': word,
        'subwords': subwords,
        'translations': translations
    })