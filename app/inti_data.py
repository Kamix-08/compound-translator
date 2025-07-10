import requests
import py7zr
import shutil
import os
from pathlib import Path
from german_compound_splitter import comp_split

DICTIONARY_URL = 'https://sourceforge.net/projects/germandict/files/german.7z'
DEST_DIR       = Path('data/')
ARCHIVE_PATH   = DEST_DIR / 'dict.7z'
EXTRACTED_FILE = DEST_DIR / 'german.dic'
FINAL_FILE     = DEST_DIR / 'german_utf8.dic'

def download():    
    with requests.get(DICTIONARY_URL, stream=True) as r:
        with open(ARCHIVE_PATH, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
def extract():
    with py7zr.SevenZipFile(ARCHIVE_PATH, mode='r') as archive:
        archive.extractall(path=DEST_DIR)
        
def convert():
    content = EXTRACTED_FILE.read_text(encoding='iso-8859-15')
    FINAL_FILE.write_text(content, encoding='utf-8')
    
def clean_up():
    for filename in os.listdir(DEST_DIR):
        filepath = DEST_DIR / filename
        if os.path.isfile(filepath) and filepath != FINAL_FILE:
            os.remove(filepath)
    
def init():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    download()
    extract()
    convert()
    clean_up()
    
def get_ahocs():
    if not os.path.isfile(FINAL_FILE):
        init()
        
    return comp_split.read_dictionary_from_file(str(FINAL_FILE))