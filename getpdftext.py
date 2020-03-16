from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter


def analisarApenasTextBoxs(caminho_pdf):
    document = open(caminho_pdf, 'rb')
    rsrcmgr = PDFResourceManager()

    '''
        Parametros para análise - laparams() default
        line_overlap=0.5
        char_margin=2.0 
        line_margin=0.5
        word_margin=0.1
        boxes_flow=0.5
        detect_vertical=False
        all_texts=False
    '''
    laparams = LAParams()

    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(document):
        interpreter.process_page(page)
        # Pegando o objeto LTPage (Com todos seus objetos) -- MELHORAR DEPOIS
        layout = device.get_result()
        for element in layout:
            # Filtrando/Printando apenas caixas com textos da página
            if isinstance(element, LTTextBoxHorizontal):
                print(element.get_text())


analisarApenasTextBoxs('pdfTeste.pdf')

