from ultralytics import YOLO
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
model = YOLO(MODEL_PATH)


def detect_plates_from_memory(pil_image, conf=0.005):
    """
    Recebe um PIL.Image, roda YOLO e retorna lista com dicts {crop, confidence, bbox}.
    """
    results = model.predict(
        source=pil_image, conf=conf, save_crop=False, save=False, verbose=False
    )
    objetos = []
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
                objetos.append({"crop": crop, "confidence": float(confval)})
    return objetos
