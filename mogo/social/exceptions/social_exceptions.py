from rest_framework.exceptions import APIException


class AvaliacaoValidationError(APIException):
    status_code = 400
    default_detail = 'Solicitação incorreta. Verifique um ou mais campos.'
    default_code = 'validation_error'


class AvaliacaoJaExisteError(APIException):
    status_code = 409
    default_detail = 'Você já avaliou este local'
    default_code = 'review_exists'


class FavoritoValidationError(APIException):
    status_code = 400
    default_detail = 'Solicitação incorreta. Verifique um ou mais campos.'
    default_code = 'validation_error'


class FavoritoJaExisteError(APIException):
    status_code = 409
    default_detail = 'Local já está nos favoritos'
    default_code = 'favorite_exists'


class FavoritoNaoEncontradoError(APIException):
    status_code = 404
    default_detail = 'Favorito não encontrado'
    default_code = 'favorite_not_found'
