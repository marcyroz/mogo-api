from detectyolo import detect_plates_from_memory
from extractpaddle import extract_text_from_pil
from io import BytesIO
from PIL import Image
import os


def main(folder_path):
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".jfif"))
    ]
    for image_path in files:
        pil_img = Image.open(image_path).convert("RGB")
        objetos = detect_plates_from_memory(pil_img)
        for obj in objetos:
            text = extract_text_from_pil(obj["crop"])
            print(f"Confiança: {obj['confidence']:.3f} | Text: {text}")


if __name__ == "__main__":
    folder_path = r"C:\Users\Johny\Downloads\piso"
    main(folder_path)
