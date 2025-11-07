from ultralytics import YOLO
import os
from PIL import Image, ImageDraw, ImageFont


MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
model = YOLO(MODEL_PATH)


# def salvar_debug_deteccoes(
#     pil_image, resultado_objetos, lat, lng, debug_dir="debug_deteccoes"
# ):
#     """
#     Salva as imagens com bounding boxes e confiança para debug.
#     """
#     if not os.path.exists(debug_dir):
#         os.makedirs(debug_dir)

#     # Criar cópia da imagem para desenhar
#     img_debug = pil_image.copy()
#     draw = ImageDraw.Draw(img_debug)

#     # Tentar carregar fonte, se não conseguir usa a padrão
#     try:
#         font = ImageFont.truetype("arial.ttf", 20)
#     except:
#         font = ImageFont.load_default()

#     # Desenhar cada detecção
#     for idx, obj in enumerate(resultado_objetos):
#         crop = obj["crop"]
#         confidence = obj["confidence"]

#         # Obter coordenadas aproximadas (reconstruir do crop)
#         # Para simplificar, vamos desenhar um retângulo genérico
#         # Se tiver bbox, use-o

#         # Desenhar retângulo verde (cor de sucesso)
#         x_min, y_min, x_max, y_max = 10 + idx * 50, 10, 60 + idx * 50, 60
#         draw.rectangle([x_min, y_min, x_max, y_max], outline="green", width=3)

#         # Escrever confiança
#         text = f"{confidence:.2%}"
#         draw.text((x_min, y_max + 5), text, fill="green", font=font)

#     # Salvar imagem
#     filename = f"deteccoes_{lat:.4f}_{lng:.4f}_({len(resultado_objetos)}).png"
#     filepath = os.path.join(debug_dir, filename)
#     img_debug.save(filepath)

#     return filepath


def detect_plates_from_memory(pil_image, conf=0.05, debug=False, save_debug=False):
    """
    Recebe um PIL.Image, roda YOLO e retorna lista com dicts {crop, confidence, bbox}.
    """
    results = model.predict(
        source=pil_image, conf=conf, save_crop=False, save=False, verbose=False
    )
    objetos = []
    todas_confiancas = []

    for result in results:
        boxes = getattr(result, "boxes", None)
        if boxes is not None and hasattr(boxes, "xyxy"):
            arr_boxes = boxes.xyxy.cpu().numpy()
            arr_conf = (
                boxes.conf.cpu().numpy()
                if hasattr(boxes, "conf")
                else [1.0] * len(arr_boxes)
            )
            for xy, confval in zip(arr_boxes, arr_conf):
                crop = pil_image.crop(tuple(xy))
                objetos.append(
                    {
                        "crop": crop,
                        "confidence": float(confval),
                        "bbox": tuple(xy),
                    }
                )
                todas_confiancas.append(float(confval))

    return objetos
