import functools
from flask import current_app


__all__ = [
    'roles_required',
    'permissions_required',
    'get_child_permissions',
    'get_all_child_permissions_for_user'
]


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

            if ac_manager.default_error_handler:
                return ac_manager.default_error_handler()

            if failed_callback:
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

            if ac_manager.default_error_handler:
                return ac_manager.default_error_handler()

            if failed_callback:
                return failed_callback()
        return wrapper
    return _permissions_required


def get_child_permissions(permission_keys):
    """
    Get all valid child permissions by provided permission keys
    with Deep First Search

    return: list of Permission objects

    """

    ac_manager = current_app.ac_manager
    permissions = ac_manager.get_permissions_by_keys(permission_keys)
    valid = []
    for permission in permissions:
        valid += list(ac_manager.get_child_permissions(permission))

    return valid


def get_all_child_permissions_for_user():
    """
    Get all valid child Permission objects for current user

    return: list of Permission objects

    """

    ac_manager = current_app.ac_manager
    permission_keys = ac_manager.get_user_permissions()
    return get_child_permissions(permission_keys)
