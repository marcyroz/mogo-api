from celery import shared_task
from analysis.services import processar_acessibilidade_rota_em_ram
import os

@shared_task
def processar_rota_async(rota_id):
    """Task async para processar rota sem bloquear request"""
    from navigation.models import Rota
    
    try:
        rota = Rota.objects.get(id=rota_id)
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        processar_acessibilidade_rota_em_ram(rota, api_key, save_debug=False)
        return {"status": "sucesso", "rota_id": str(rota_id)}
    except Exception as e:
        return {"status": "erro", "message": str(e)}
