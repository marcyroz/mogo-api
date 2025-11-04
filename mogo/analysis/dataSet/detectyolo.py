from ultralytics import YOLO
import os

# Inicialize o modelo YOLO
model = YOLO('C:/Users/Johny/Downloads/yoloTeste/yolov10_paddle/model/best.pt')

def detect_plates(image_path, conf=0.005):
    """
    Detecta objetos na imagem usando o modelo YOLO.
    Retorna uma lista de caminhos para as imagens recortadas.
    """
    # Executa a detecção com confiança ajustada e salva os crops
    results = model.predict(source=image_path, conf=conf, save_crop=True, save=True, verbose=False)

    cropped_images_paths = []

    # Percorre os resultados e coleta os caminhos dos crops
    for result in results:
        if hasattr(result, 'crops') and result.crops is not None:
            for cls_name, crops_list in result.crops.items():
                cropped_images_paths.extend(crops_list)

    return cropped_images_paths
