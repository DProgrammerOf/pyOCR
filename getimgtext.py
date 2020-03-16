from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Script teste para obter textos de imagens -- MELHORAR DEPOIS

txtImg = pytesseract.image_to_string(Image.open('imagemTeste.png'), lang='eng')
# Separando por quebra de linha
txtImg = txtImg.splitlines()
# Limpando valores vazios/nulos
txtImg = [i for i in txtImg if i]
print(txtImg)
