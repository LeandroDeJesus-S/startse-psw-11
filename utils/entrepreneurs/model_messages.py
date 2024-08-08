class CompanyMessages:
    """All the constants with the messages to use when the model Company
    to raise a validation error
    """
    DUPLICATED_CNPJ = 'Este CNPJ não esta disponível.'
    DUPLICATED_NAME = 'Uma empresa com este nome já existe.'
    DUPLICATED_SITE = 'O endereço do site informado já esta registrado.'

    EMPTY_AREA = 'Informe a area de atuação da sua empresa.'
    EMPTY_CNPJ = 'O CPNJ não pode ficar vazio.'
    EMPTY_DESC = 'Por favor descreva a sua empresa para que os investidores possam conhece-la melhor.'
    EMPTY_FINAL_DATE_CAPITATION = 'Data final de capitação não fornecida.'
    EMPTY_LOGO = 'Por favor, insira uma logo.'
    EMPTY_NAME = 'Nome não pode ser vazio.'
    EMPTY_PERCENT_EQUITY = 'Percentual equity não pode ser vazio.'
    EMPTY_SITE = 'Por favor, informe o site da sua empresa.'
    EMPTY_STAGE = 'O estagio é obrigatório.'
    EMPTY_TARGET_AUDIENCE = 'Informe o publico alvo.'
    EMPTY_TIME_OF_EXISTENCE = 'Tempo de existência não fornecido.'
    EMPTY_USER = 'Usuário não pode ficar vazio.'
    EMPTY_VALUE = 'Por favor, insira o valor de capitação.'

    INVALID_AREA = 'a rea escolhida é inválida.'
    INVALID_CNPJ = 'CPNJ inválido ou incorreto.'
    INVALID_FINAL_DATE_CAPITATION = 'Data final de capitação inválida.'
    INVALID_LOGO = 'Logo inválida.'
    INVALID_NAME = 'Nome de empresa inválido.'
    INVALID_PERCENT_EQUITY = 'Percentual equity inválido.'
    INVALID_PITCH = 'Pitch deve ser um arquivo .wav ou .mp4'
    INVALID_SITE = 'A url do site é inválida.'
    INVALID_STAGE = 'O estagio selecionado é inválido.'
    INVALID_TARGET_AUDIENCE = 'publico alvo inválido.'
    INVALID_TIME_OF_EXISTENCE = 'Tempo de existência inválido.'
    INVALID_USER = 'Usuário inválido.'
    INVALID_VALUE = 'valor de capitação inválido.'

    INVALID_FILE_SIZE = '{field_name} deve ter tamanho máximo de {size}'


class DocumentMessages:
    EMPTY_COMPANY = 'Por favor, informe uma empresa.'
    EMPTY_FILE = 'O arquivo do documento não foi fornecido.'
    EMPTY_TITLE = 'O titulo não pode ser vazio.'
    
    INVALID_COMPANY = 'Por favor, informe uma empresa valida.'
    INVALID_FILE = 'Documento inválido'
    INVALID_TITLE = 'Título inválido.'

    MIN_TITLE_LENGTH = 'O título deve ter no mínimo {len} caracteres.'

    DOCUMENT_ALREADY_EXISTS = 'Documento já cadastrado.'
