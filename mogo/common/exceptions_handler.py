from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from pydantic import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Handler global de exceptions."""

    # Chamar handler padrão do DRF
    response = exception_handler(exc, context)

    if response is not None:
        # Customizar para seguir seus padrões de resposta
        if isinstance(response.data, dict):
            message = response.data.get('detail', str(exc))
        else:
            # response.data pode ser None ou outro tipo; usar fallback para string da exceção
            try:
                message = str(
                    response.data) if response.data is not None else str(exc)
            except Exception:
                message = str(exc)
        custom_response_data = {
            'message': message
        }

        # Se é erro de validação (400), incluir campo 'campos'
        if response.status_code == 400:
            if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
                # Extrair campos com erro
                campos_com_erro = []
                if 'errors' in exc.detail:
                    for error in exc.detail['errors']:
                        if 'field' in error:
                            campos_com_erro.append(error['field'])

                if campos_com_erro:
                    custom_response_data['campos'] = campos_com_erro

        # Tratar erros de JWT
        if isinstance(exc, (InvalidToken, TokenError)):
            return Response({
                'status': 'error',
                'message': 'Token inválido ou expirado'
            }, status=401)

        # Incluir detalhes customizados se existirem
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            custom_response_data.update(exc.detail)

        response.data = custom_response_data

        # Log do erro
        logger.error(f"API Error: {exc.__class__.__name__} - {str(exc)}")

    else:
        # Erro não capturado pelo DRF (500)
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        response = Response(
            {'message': 'Erro inesperado.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
