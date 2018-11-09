class InvalidPermissionObjError(Exception):

    def __init__(self):
        self.msg = 'Permission Object is not a valid dict'
