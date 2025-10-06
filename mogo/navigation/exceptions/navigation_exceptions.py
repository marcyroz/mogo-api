from rest_framework.exceptions import APIException


class LocalNaoEncontradoError(APIException):
    status_code = 404
    default_detail = 'Local não encontrado'
    default_code = 'location_not_found'


class RotaValidationError(APIException):
    status_code = 400
    default_detail = 'Solicitação incorreta. Verifique um ou mais campos.'
    default_code = 'route_validation_error'


class RotaNaoEncontradaError(APIException):
    status_code = 404
    default_detail = 'Rota não encontrada'
    default_code = 'route_not_found'


class CoordenadaInvalidaError(APIException):
    status_code = 400
    default_detail = 'Coordenadas inválidas fornecidas'
    default_code = 'invalid_coordinates'
