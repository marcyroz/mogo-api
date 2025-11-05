from paddleocr import PaddleOCR
import logging
import numpy as np

logging.getLogger("ppocr").setLevel(logging.ERROR)

# Inicializar OCR com TODAS as otimizações desabilitadas
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='pt',
    use_gpu=False,
    enable_mkldnn=False,
    use_tensorrt=False,
    use_dilation=False
)

def extract_text_from_pil(pil_img):
    """Extrai texto de uma imagem PIL"""
    try:
        arr = np.asarray(pil_img)
        result = ocr.ocr(arr, cls=True)
        text_lines = []
        
        if result is None or len(result) == 0:
            return ""
        
        for page in result:
            if page is None:
                continue
            for item in page:
                if item and len(item) >= 2:
                    text = item[1][0]
                    text_lines.append(text)
        
        return "\n".join(text_lines)
    except Exception as e:
        print(f"⚠️ Erro no OCR: {e}")
        return ""
