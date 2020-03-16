from googletrans import Translator


def traduzirTexto(texto):
    tradutor = Translator()
    idioma = tradutor.detect(texto)
    if idioma.confidence == 0.0: # Verifica a confiabilidade do spellchecker da google - MELHORAR DEPOIS
        return r'\n'

    tradutor = tradutor.translate(texto, src=idioma.lang, dest='pt')
    return tradutor.text


