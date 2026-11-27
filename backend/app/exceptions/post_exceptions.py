
class PostNotFoundError(Exception):
    pass


class PostPermissionError(Exception):
    pass


class PostRoleError(Exception):
    pass


class PostDeletionConflictError(Exception):
    pass

class MinBudgetExceedMaxBudget(Exception):
    pass
