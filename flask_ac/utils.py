import functools
from flask import current_app


def roles_required(roles=[], failed_callback=None):
    """
    Roles control decorator.
    Allow the access for current resource when at lease 1 role included
    args:
        roles - list, Allow access roles
        failed_callback - func, handler when access failed
    """

    def _roles_required(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ac_manager = current_app.ac_manager
            if ac_manager.allow_access(roles=roles):
                return func(*args, **kwargs)
            return failed_callback()
        return wrapper
    return _roles_required


def permissions_required(permissions=[], failed_callback=None):
    """
    Permissions control decorator.
    Allow the access for current resource when at lease 1 permission included
    args:
        permissions - list, Allow access roles
        failed_callback - func, handler when access failed
    """

    def _permissions_required(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ac_manager = current_app.ac_manager
            if ac_manager.allow_access(permissions=permissions):
                return func(*args, **kwargs)
            return failed_callback()
        return wrapper
    return _permissions_required
