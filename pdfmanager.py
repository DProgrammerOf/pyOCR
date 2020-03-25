# Imports do ReportLab
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Imports do PdfMiner
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLine, LTCurve, LTChar, LTTextLineHorizontal

# Imports de manipulação primitiva
from re import search, IGNORECASE

# Variaveis locais do arquivo
pastaSaida = "PdfsGerados/"
pastaFonts = "Fonts/"
pdfFonts = []


# Classe substitutiva para LTChar (manipulação mais visível e minificada)
class CaracterManager:
    def __init__(self, text, fontname, size, color, ref, x, y):
        self.caracter = text
        self.tipografia = fontname
        self.tamanho = size
        self.cor = color
        self.referencia = ref
        self.x = x
        self.y = y


#
# Tratando objetos LTCurve
#
def tratarLtCurve(Pdf, Curve):
    if isinstance(Pdf, canvas.Canvas):
        if isinstance(Curve, LTCurve):
            linhas = Curve.pts
            caminho_pontos = Pdf.beginPath()
            caminho_pontos.moveTo(linhas[0][0], linhas[0][1])
            for pontos in linhas:
                caminho_pontos.lineTo(pontos[0], pontos[1])
            caminho_pontos.close()
            Pdf.drawPath(caminho_pontos)
            return True
        else:
            print("{ erro: true, log: 'Tipo de instância inválida para LTCurve'}")
    else:
        print("{ erro: true, log: 'Tipo de instância inválida para Canvas'}")


#
# Tratamento de objetos LTChar
#
def tratarLtChar(Char):
    if isinstance(Char, LTChar):

        fonteLetra = Char.fontname
        fonteLetraReformatado = ""

        # Formatando nome das familias para compatibilizar com pasta local
        # Padrão: Segoe UI
        if search('segoe-semibold', fonteLetra, IGNORECASE):
            fonteLetraReformatado = "Segoe-SemiBold"
        elif search('segoe-bold', fonteLetra, IGNORECASE):
            fonteLetraReformatado = "Segoe-Bold"
        elif search('segoe', fonteLetra, IGNORECASE):
            fonteLetraReformatado = "Segoe"
        elif search('ZapfDingbatsStd', fonteLetra, IGNORECASE):
            fonteLetraReformatado = "ZapfDingbatsStd"
        else:
            fonteLetraReformatado = "Segoe"

        if not fonteLetraReformatado in pdfFonts:
            pdfFonts.append(fonteLetraReformatado)
            pdfmetrics.registerFont(TTFont(fonteLetraReformatado,
                                           pastaFonts + fonteLetraReformatado + '/' + fonteLetraReformatado + '.ttf'))

        if Char.upright is True:
            return CaracterManager(Char.get_text(), fonteLetraReformatado, Char.size, None, True, Char.x0, Char.y0)
        else:
            return CaracterManager(Char.get_text(), fonteLetraReformatado, Char.size, None, False, Char.x1, Char.y1)
    else:
        print("{ erro: true, log: 'Tipo de instância inválida para LTChar'}")


#
# Tratando objetos LTTextBoxHorizontal
#
def tratarLtTextBoxHorizontal(Pdf, TextBox):
    if isinstance(Pdf, canvas.Canvas):
        if isinstance(TextBox, LTTextBoxHorizontal):
            linhas = TextBox.objs
            for linha in linhas:
                for caracter in linha.objs:
                    if isinstance(caracter, LTChar):
                        CManager = tratarLtChar(caracter)
                        if isinstance(CManager, CaracterManager):
                            ObjetoTexto = Pdf.beginText()
                            ObjetoTexto.setTextOrigin(CManager.x, CManager.y)
                            ObjetoTexto.setFont(CManager.tipografia, CManager.tamanho)
                            ObjetoTexto.textOut(CManager.caracter)
                            Pdf.drawText(ObjetoTexto)

            return True
        else:
            print("{ erro: true, log: 'Tipo de instância inválida para LTTextBoxHorizontal'}")
    else:
        print("{ erro: true, log: 'Tipo de instância inválida para Canvas'}")


#
# Criação do PDF
#
def criarPdf(caminho_pdf, titulo, tamanho):
    pdf = canvas.Canvas(pastaSaida + caminho_pdf + ".pdf", pagesize=tamanho, enforceColorSpace='RGB')
    pdf.setTitle(titulo)
    return pdf


#
# Salvamento final do PDF
#
def salvarPdf(pdf):
    pdf.save()
