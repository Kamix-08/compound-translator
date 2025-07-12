import requests
import zstandard
import tarfile
import shutil
import os
from pathlib import Path
from german_compound_splitter import comp_split # type: ignore

DICTIONARY_URL = 'https://mirror.rackspace.com/archlinux/extra/os/x86_64/words-2.1-8-any.pkg.tar.zst'
DEST_DIR       = Path('data/')
ARCHIVE_PATH   = DEST_DIR / 'words-2.1-8-any.pkg.tar.zst'
EXTRACTED_TAR  = DEST_DIR / 'archive.tar'
EXTRACTED_DIR  = DEST_DIR
TARGET_FILE    = EXTRACTED_DIR / 'usr/share/dict/ngerman'
FINAL_FILE     = DEST_DIR / 'ngerman'

def download():    
    with requests.get(DICTIONARY_URL, stream=True) as r:
        with open(ARCHIVE_PATH, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
def extract():
    with open(ARCHIVE_PATH, 'rb') as compressed:
        dctx = zstandard.ZstdDecompressor()
        with dctx.stream_reader(compressed) as reader:
            with open(EXTRACTED_TAR, 'wb') as decompressed:
                decompressed.write(reader.read())
                
    with tarfile.open(EXTRACTED_TAR, 'r') as tar:
        tar.extractall(EXTRACTED_DIR)
        
    shutil.move(str(TARGET_FILE), str(FINAL_FILE))
    
def clean_up(dir=DEST_DIR):
    for path in dir.iterdir():
        if path == FINAL_FILE:
            continue
        
        if path.is_dir():
            clean_up(path)
            path.rmdir()
        else:
            path.unlink()
    
def init():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    download()
    extract()
    clean_up()
    
def get_ahocs():
    if not os.path.isfile(FINAL_FILE):
        init() 
        
    return comp_split.read_dictionary_from_file(str(FINAL_FILE))