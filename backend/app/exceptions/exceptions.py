class UserDeletionConflictError(Exception):
    """Indica que o usuário não pode ser excluído devido a uma restrição do banco."""


class UserAlreadyExistsError(Exception):
    """Indica que o email já está cadastrado."""