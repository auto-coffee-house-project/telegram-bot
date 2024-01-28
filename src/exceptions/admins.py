class AdminDoesNotExistError(Exception):

    def __init__(self, admin_user_id: int):
        self.admin_user_id = admin_user_id
