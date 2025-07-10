from googletrans import Translator

translator = Translator()

def translate(words:list[str], src='de', dest='en') -> dict:
    translations = [translator.translate(word, src=src, dest=dest) for word in words]
    return {t.origin: t.text for t in translations}