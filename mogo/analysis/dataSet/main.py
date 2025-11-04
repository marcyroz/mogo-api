from detectyolo import detect_plates
from extractpaddle import extract_text
import shutil
import os

def main(folder_path):
    try:
        # Caminho da pasta de resultados do YOLO
        caminho_da_pasta = "./runs/"

        # 🔹 Limpar a pasta de runs ANTES de começar
        if os.path.exists(caminho_da_pasta):
            shutil.rmtree(caminho_da_pasta)
            print(f"Pasta '{caminho_da_pasta}' apagada antes de iniciar o processamento.\n")

        # Listar todos os arquivos da pasta
        files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.jfif'))
        ]

        # Processar cada imagem
        for image_path in files:
            print(f"\nProcessando imagem: {image_path}")
            cropped_images_paths = detect_plates(image_path)

            # Aplicar OCR em cada crop
            for crop_path in cropped_images_paths:
                text = extract_text(crop_path)
                print(f"Texto extraído da imagem {crop_path}: {text}")

        print("\nProcessamento concluído com sucesso!")

    except Exception as e:
        print("Erro!", e)


if __name__ == "__main__":
    # Pasta com as imagens
    folder_path = r"C:\Users\Johny\Downloads\piso"
    main(folder_path)
