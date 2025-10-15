from rest_framework.exceptions import APIException

class UsuarioValidationError(APIException):
    status_code = 400
    default_detail = 'Solicitação incorreta. Verifique um ou mais campos.'
    default_code = 'user_validation_error'

class UsuarioJaExisteError(APIException):
    status_code = 409
    default_detail = 'O email ou senha já pertencem a um usuário.'
    default_code = 'user_exists'

class UsuarioNaoEncontradoError(APIException):
    status_code = 404
    default_detail = 'Usuário não encontrado'
    default_code = 'user_not_found'

class ContaDesativadaError(APIException):
    status_code = 403
    default_detail = 'Esta conta foi desativada e não pode ser mais utilizada.'
    default_code = 'account_deactivated'

class AuthenticationRequiredError(APIException):
    status_code = 401
    default_detail = 'Autenticação necessária. Verifique se está logado.'
    default_code = 'authentication_required'

class TerceiroValidationError(Exception):
    """Erro de validação de terceiro"""
    pass

class TerceiroJaExisteError(Exception):
    """Erro quando terceiro já existe para um usuário"""
    pass
