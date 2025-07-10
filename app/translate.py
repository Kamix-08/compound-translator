from googletrans import Translator

translator = Translator()

def translate(words:list[str], dest='en') -> dict:
    translations = [translator.translate(word, src='de', dest=dest) for word in words]
    return {t.origin: t.text for t in translations}