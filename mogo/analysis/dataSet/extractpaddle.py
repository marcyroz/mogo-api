from paddleocr import PaddleOCR
import logging
import os

# Suprimir logs do PaddleOCR
logging.getLogger("ppocr").setLevel(logging.ERROR)

# Inicializar o modelo OCR
ocr = PaddleOCR(use_angle_cls=True, lang='pt')  # 'pt' para português

def extract_text(image_path):
    """
    Recebe o caminho de uma imagem e retorna o texto detectado.
    """
    result = ocr.ocr(image_path)
    text_lines = []

    for page in result:  # percorre cada linha/segmento detectado
        for item in page:
            # Cada item: [box, (text, conf)]
            text = item[1][0]  # pega apenas o texto
            text_lines.append(text)

    return '\n'.join(text_lines)


def extract_text_from_folder(folder_path):
    """
    Extrai texto de todas as imagens de uma pasta.
    Retorna um dicionário {caminho_imagem: texto_extraído}
    """
    supported_formats = ('.jpg', '.jpeg', '.png', '.jfif')
    results = {}

    for f in os.listdir(folder_path):
        if f.lower().endswith(supported_formats):
            image_path = os.path.join(folder_path, f)
            results[image_path] = extract_text(image_path)

    return results
