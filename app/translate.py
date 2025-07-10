from deep_translator import GoogleTranslator

def translate(words:list[str], dest='en') -> dict:
    translator = GoogleTranslator(source='de', target=dest)
    return {word: translator.translate(word) for word in words}