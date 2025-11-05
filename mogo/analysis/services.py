import requests
from io import BytesIO
from PIL import Image
from analysis.dataSet.detectyolo import detect_plates_from_memory
from analysis.dataSet.extractpaddle import extract_text_from_pil


def baixar_streetview_em_ram(lat, lng, api_key):
    url = (
        f"https://maps.googleapis.com/maps/api/streetview"
        f"?size=640x640&location={lat},{lng}&key={api_key}"
    )
    resp = requests.get(url)
    if resp.status_code == 200:
        return Image.open(BytesIO(resp.content)).convert("RGB")
    return None


def processar_acessibilidade_rota_em_ram(rota, api_key):
    coords = list(rota.polyline_line.coords)
    conf_soma, total = 0, 0
    resultados = []

    for lng, lat in coords:
        pil_img = baixar_streetview_em_ram(lat, lng, api_key)
        if pil_img:
            objetos = detect_plates_from_memory(pil_img)
            for obj in objetos:
                text = ""  # OCR desabilitado
                conf_soma += obj["confidence"]
                total += 1
                resultados.append(
                    {
                        "posicao": (lat, lng),
                        "objeto_conf": obj["confidence"],
                        "ocr": text,
                    }
                )

    # NOVO CÁLCULO DE SCORE
    if total > 0:
        # Média de confiança
        conf_media = conf_soma / total

        # Quantidade por imagem (normalizado)
        num_imagens = len(set(r["posicao"] for r in resultados))
        deteccoes_por_imagem = total / num_imagens if num_imagens > 0 else 0

        # Score final: combina confiança e quantidade
        # Quanto MAIOR, MELHOR a acessibilidade
        score_acessibilidade = (conf_media * 0.6) + (
            min(deteccoes_por_imagem / 10, 1.0) * 0.4
        )
    else:
        score_acessibilidade = 0.0

    rota.score_acessibilidade = score_acessibilidade
    rota.save()

    return {
        "score_media_confianca": score_acessibilidade,
        "media_confianca": conf_media if total > 0 else 0,
        "total_deteccoes": total,
        "deteccoes_por_imagem": deteccoes_por_imagem if total > 0 else 0,
        "resultados": resultados,
    }
