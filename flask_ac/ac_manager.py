'''
This module provide ACManager class

'''


from flask import g
from flask_ac import ptree


class ACManager(object):
    '''
    ACManager is defination of access control manager,
    which hold the loaders and other configs for access control.

    Instance of ACManager can bounded to several apps, by using init_app
    method in your application's factory.

    To initialize ACManager, the permissions object is required.
    This dict object provide all the permissions with name and key
    (name is the description of the permission, and key is generally a string
    represent the permission in data model). In each permission, there is also
    a list of dict which represent other permissions under this permission.
    This tree-like structure is called ptree in flask_ac, and it will generate
    the actual ptree object when init ACManager instance

    '''
    def __init__(self, permissions, app=None, roles_loader=None,
                 permissions_loader=None, default_error_handler=None):

        # TODO: support for cfg or other format permission
        self.ptree = self.build_ptree_from_obj(permissions)
        self.roles_loader = roles_loader
        self.permissions_loader = permissions_loader

        self.default_error_handler = default_error_handler

        # Bounded to the app if provided
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''
        Bound the ACManager instance so the flask or other application can
        access manager anywhere with context
        '''

        app.ac_manager = self

    def get_valid_permissions(self, permissions):
        '''
        Get all valid nodes by traversal top-down from root to leaf
        '''

        return ptree.get_nodes_in_path(self.ptree, permissions)

    def allow_access(self, roles=None, permissions=None):
        if roles:
            return self._allow_access_by_role(roles)
        valid_permissions = self.get_valid_permissions(permissions)
        return self._allow_access_by_permissions(valid_permissions)

    def _allow_access_by_role(self, roles):
        roles = set(roles)
        user_roles = set(self.get_user_roles())
        intersactions = self._get_intersection(roles, user_roles)
        return len(intersactions) > 0

    def _allow_access_by_permissions(self, permissions):
        permissions = set(permissions)
        user_permissions = set(self.get_user_permissions())
        intersactions = self._get_intersection(permissions, user_permissions)
        return len(intersactions) > 0

    def _get_intersection(self, set_1, set_2):
        return set_1.intersection(set_2)

    def get_user_roles(self):
        if self.permissions_loader:
            return self.roles_loader()
        return self._roles_loader()

    def get_user_permissions(self):
        if self.permissions_loader:
            return self.permissions_loader()
        return self._permissions_loader()

    def _roles_loader(self):
        '''
        Default roles loader

        By default, ac_manager will query user from flask global g.user
        To query from session or other place, provide the loader when
        initializing the ac_manager instance
        '''

        user = g.user
        roles = user.get('roles', [])
        return [role.get('name') for role in roles]

    def _permissions_loader(self):
        '''
        Default roles loader

        By default, ac_manager will query user from flask global g.user
        To query from session or other place, provide the loader when
        initializing the ac_manager instance
        '''

        user = g.user
        roles = user.get('roles')
        permissions = []
        for role in roles:
            permissions += role.get('permissions')
        return permissions

    def build_ptree_from_obj(self, obj):
        '''
        Build ptree from provider permission object
        '''

        return ptree.create_ptree_from_obj(obj)
