from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLine, LTCurve, LTChar, LTTextLineHorizontal, LTPage
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed, PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from pdfmanager import criarPdf, salvarPdf, tratarLtTextBoxHorizontal, tratarLtCurve

#
# Função teste para extração do texto e criação de novo PDF com objetos curvos e textos
#
def reformatarPdf(caminho_pdf):
    pdfopen = open(caminho_pdf, 'rb')
    parser = PDFParser(pdfopen)
    document = PDFDocument(parser)
    # Checa se o documento é válido para extração
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    # Parametros para bounds do texto
    laparams = LAParams()

    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(pdfopen):

        interpreter.process_page(page)
        # Pegando o objeto LTPage (Com todos seus objetos) -- MELHORAR DEPOIS
        layout = device.get_result()
        # Criando novo PDF
        if isinstance(layout, LTPage):
            NovoPDF = criarPdf("WindowsInternals-Pagina"+str(layout.pageid), "Pagina "+str(layout.pageid),
                               (layout.width, layout.height))

        for element in layout:
            # Tratando curvas da página
            if isinstance(element, LTCurve):
                if isinstance(tratarLtCurve(NovoPDF, element), bool):
                    print("LTCurve tratado!")
                else:
                    print("LTCurve não foi tratado corretamente!")

            # Tratando textos horizontais da página
            elif isinstance(element, LTTextBoxHorizontal):
                if isinstance(tratarLtTextBoxHorizontal(NovoPDF, element), bool):
                    print("LTTextBoxHorizontal tratado!")
                else:
                    print("LTTextBoxHorizontal não foi tratado corretamente!")

        # Salvando o novo PDF na pasta "PdfsGerados"
        salvarPdf(NovoPDF)



reformatarPdf('PdfsBase/windowsInternals26.pdf')
