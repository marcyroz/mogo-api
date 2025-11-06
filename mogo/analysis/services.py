import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from analysis.dataSet.detectyolo import detect_plates_from_memory
from analysis.dataSet.extractpaddle import extract_text_from_pil
import os


# def desenhar_deteccoes_na_imagem(
#     pil_img, objetos, lat, lng, debug_dir="debug_deteccoes"
# ):
#     """
#     Desenha os bounding boxes e confiança na imagem original.
#     """
#     # ✅ Criar pasta se não existir
#     if not os.path.exists(debug_dir):
#         os.makedirs(debug_dir)
#         print(f"   📁 Pasta criada: {debug_dir}/")

#     # Criar cópia para desenhar
#     img_debug = pil_img.copy()
#     draw = ImageDraw.Draw(img_debug)

#     # Fonte
#     try:
#         font = ImageFont.truetype("arial.ttf", 16)
#         font_pequena = ImageFont.truetype("arial.ttf", 12)
#     except:
#         font = ImageFont.load_default()
#         font_pequena = ImageFont.load_default()

#     # Cores para cada detecção
#     cores = [
#         (0, 255, 0),  # verde
#         (0, 255, 255),  # ciano
#         (255, 255, 0),  # amarelo
#         (255, 0, 255),  # magenta
#         (255, 165, 0),  # laranja
#     ]

#     # ✅ Desenhar cada detecção USANDO O BBOX CORRETO
#     for idx, obj in enumerate(objetos):
#         bbox = obj.get("bbox")  # (x_min, y_min, x_max, y_max)
#         confidence = obj["confidence"]

#         if bbox:
#             x_min, y_min, x_max, y_max = [int(x) for x in bbox]
#             cor = cores[idx % len(cores)]

#             # ✅ Desenhar retângulo MAIOR (não aquele 50px genérico)
#             draw.rectangle([x_min, y_min, x_max, y_max], outline=cor, width=4)

#             # Desenhar confiança no topo do retângulo
#             text_conf = f"{confidence:.1%}"
#             text_bbox = draw.textbbox((0, 0), text_conf, font=font)
#             text_width = text_bbox[2] - text_bbox[0]

#             # Fundo escuro para o texto
#             draw.rectangle(
#                 [x_min, y_min - 25, x_min + text_width + 10, y_min], fill=(0, 0, 0, 128)
#             )

#             # Texto em cima
#             draw.text((x_min + 5, y_min - 20), text_conf, fill=cor, font=font)

#     # Adicionar info geral no canto superior esquerdo com fundo
#     info_text = f"Lat: {lat:.4f}\nLng: {lng:.4f}\nDetecções: {len(objetos)}"

#     # Fundo para o info text
#     draw.rectangle([5, 5, 200, 70], fill=(0, 0, 0, 180))
#     draw.text((10, 10), info_text, fill=(255, 255, 255), font=font_pequena)

#     # Salvar com caminho absoluto
#     safe_filename = f"detec_{lat:.4f}_{lng:.4f}_({len(objetos)}det).png"
#     filepath = os.path.join(os.getcwd(), debug_dir, safe_filename)

#     img_debug.save(filepath)
#     print(f"   💾 Salvo: {filepath}")

#     return filepath


def baixar_streetview_em_ram(lat, lng, api_key, fov=120):
    """
    Baixa uma imagem do Google Street View diretamente em RAM.
    """
    url = (
        f"https://maps.googleapis.com/maps/api/streetview"
        f"?size=640x640&location={lat},{lng}"
        f"&fov={fov}&source=outdoor&key={api_key}"
    )
    resp = requests.get(url)
    if resp.status_code == 200:
        return Image.open(BytesIO(resp.content)).convert("RGB")
    return None


def interpolar_pontos_por_distancia(linestring, intervalo_metros=25):
    """
    Gera pontos ao longo da LineString com intervalo fixo em metros.
    """
    pontos = []

    comprimento_total_metros = linestring.length * 111000
    num_pontos = int(comprimento_total_metros / intervalo_metros)

    if num_pontos < 2:
        num_pontos = 2

    comprimento_total = linestring.length

    for i in range(num_pontos + 1):
        distancia = (i / num_pontos) * comprimento_total
        ponto_interpolado = linestring.interpolate(distancia)
        pontos.append((ponto_interpolado.y, ponto_interpolado.x))

    return pontos


def processar_acessibilidade_rota_em_ram(rota, api_key, save_debug=False):
    """
    Processa acessibilidade da rota baixando imagens do Street View.
    """
    pontos = interpolar_pontos_por_distancia(rota.polyline_line, intervalo_metros=25)

    conf_soma, total = 0, 0
    resultados = []
    image_urls = []
    images_skipped = 0
    totalDetectado = 0

    # print(f"🗺️ Processando {len(pontos)} pontos ao longo da rota (a cada ~25m)...")
    # print(f"📸 Filtrando apenas imagens oficiais do Google (outdoor)...")

    for lat, lng in pontos:
        url = (
            f"https://maps.googleapis.com/maps/api/streetview"
            f"?size=640x640&location={lat},{lng}&fov=120&source=outdoor&key={api_key}"
        )
        image_urls.append(url)

        pil_img = baixar_streetview_em_ram(lat, lng, api_key, fov=120)

        if pil_img is None:
            # print(f"⚠️ Ponto ({lat:.4f}, {lng:.4f}) - Sem imagem oficial Google")
            images_skipped += 1
            continue

        objetos = detect_plates_from_memory(pil_img)

        if objetos:
            # if save_debug:
            #     try:
            #         debug_path = desenhar_deteccoes_na_imagem(pil_img, objetos, lat, lng)
            #         debug_imagens_salvas += 1
            #     except Exception as e:
            #         pass

            for obj in objetos:
                text = ""
                conf_soma += obj["confidence"]
                total += 1
                resultados.append(
                    {
                        "posicao": (lat, lng),
                        "objeto_conf": obj["confidence"],
                        "ocr": text,
                    }
                )
            totalDetectado += 1
        # else:
        #     print(f"⊘ Ponto ({lat:.4f}, {lng:.4f}) - Nenhuma detecção")

    # Calcular score
    if total > 0:
        conf_media = conf_soma / total
        num_imagens_validas = len(pontos) - images_skipped
        deteccoes_por_imagem = (
            total / num_imagens_validas if num_imagens_validas > 0 else 0
        )

        score_acessibilidade = (conf_media * 0.6) + (
            min(deteccoes_por_imagem / 10, 1.0) * 0.4
        )
    else:
        conf_media = 0.0
        deteccoes_por_imagem = 0.0
        score_acessibilidade = 0.0

    rota.score_acessibilidade = score_acessibilidade
    rota.save()

    return {
        "score_media_confianca": round(score_acessibilidade, 4),
        "media_confianca": round(conf_media, 4),
        "total_deteccoes": total,
        "deteccoes_por_imagem": round(deteccoes_por_imagem, 2),
        "num_imagens_processadas": len(pontos),
        "num_imagens_validas": len(pontos) - images_skipped,
        "num_imagens_puladas": images_skipped,
    }
