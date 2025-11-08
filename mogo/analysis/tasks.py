from celery import shared_task
from analysis.services import processar_acessibilidade_rota_em_ram
import os

@shared_task
def processar_rota_async(rota_id):
    """Task async para processar rota sem bloquear request"""
    from navigation.models import Rota
    
    rota = None  # Inicializar rota
    
    try:
        rota = Rota.objects.get(id=rota_id)
        
        # Marcar como processando
        rota.status_processamento = "processando"
        rota.save()
        
        # Processar
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        processar_acessibilidade_rota_em_ram(rota, api_key, save_debug=False)
        
        # Marcar como concluído
        rota.status_processamento = "concluido"
        rota.save()
        
        return {"status": "sucesso", "rota_id": str(rota_id)}
        
    except Rota.DoesNotExist:  # Catch específico
        return {"status": "erro", "message": f"Rota {rota_id} não encontrada"}
        
    except Exception as e:
        # Só atualiza se rota existir
        if rota:
            rota.status_processamento = "erro"
            rota.erro_mensagem = str(e)
            rota.save()
        
        return {"status": "erro", "message": str(e)}
